"""HTTP client for ``POST /v1/systemone`` with the spec's status semantics (§1.4).

Improvements over the reference ``HttpModel``:

* local pre-flight ``validate_request`` so a bad request fails before a round
  trip (spec §5.1);
* status-code handling: 400/401/422 are contract/config bugs -> fail fast, no
  retry; 413 maps to ``RequestTooLarge`` so the loop can trim and resend (§3.2);
  500 is retried once with backoff; 503 waits and retries; network errors retry
  once;
* a ``health()`` probe used by the runner before any task starts.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from typing import Any, Dict, Optional

from .validators import RequestTooLarge, validate_request


class ProtocolError(Exception):
    """400/401/422 -- a harness or contract bug, or bad credentials. No retry."""


class InferenceError(Exception):
    """The backend failed persistently (500 after retry, 503 after waits, network)."""


class DecisionClient:
    """Laya client over a running /v1/systemone server."""

    def __init__(self, base_url: str, api_key: Optional[str] = None, timeout: int = 120):
        self.base_url = base_url.rstrip("/")
        self.url = self.base_url + "/v1/systemone"
        self.key = api_key
        self.timeout = timeout

    # -- readiness ------------------------------------------------------------

    def health(self, timeout: int = 10) -> Dict[str, Any]:
        """GET /health. Returns the payload; raises on unreachable/not-ok."""
        req = urllib.request.Request(self.base_url + "/health")
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                payload = json.load(resp)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise InferenceError(f"backend unreachable at {self.base_url}: {exc}") from exc
        # two health dialects: our app.server uses {"status": "ok"}, the
        # official systemone_server uses {"ok": true}
        if payload.get("status") != "ok" and payload.get("ok") is not True:
            raise InferenceError(f"backend not ok: {payload}")
        return payload

    # -- decisions ------------------------------------------------------------

    def predict(self, state: Any, questions: Dict[str, Any]) -> Dict[str, Any]:
        """Validate, send, and return ``answers``. Retry semantics per §1.4."""
        validate_request(state, questions)  # RequestTooLarge propagates to the loop
        body = json.dumps({"state": state, "questions": questions}, ensure_ascii=False).encode("utf-8")

        sent_500_retry = False
        sent_net_retry = False
        waits_503 = 0
        while True:
            try:
                return self._send(body)
            except _Retry500 as exc:
                if sent_500_retry:
                    raise InferenceError(f"inference failed after one retry: {exc}") from exc
                sent_500_retry = True
                time.sleep(2.0)
            except _NetworkError as exc:
                if sent_net_retry:
                    raise InferenceError(f"network error persisted: {exc}") from exc
                sent_net_retry = True
                time.sleep(2.0)
            except _Wait503 as exc:
                if waits_503 >= 3:
                    raise InferenceError(f"backend still unavailable: {exc}") from exc
                time.sleep((5.0, 10.0, 20.0)[waits_503])
                waits_503 += 1

    # -- internals ------------------------------------------------------------

    def _send(self, body: bytes) -> Dict[str, Any]:
        headers = {"Content-Type": "application/json; charset=utf-8"}
        if self.key:
            headers["Authorization"] = f"Bearer {self.key}"
        req = urllib.request.Request(self.url, data=body, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                payload = json.load(resp)
        except urllib.error.HTTPError as exc:
            code = exc.code
            try:
                detail = exc.read().decode("utf-8", "replace")[:200]
            except Exception:  # noqa: BLE001
                detail = ""
            if code in (400, 401, 422):
                raise ProtocolError(f"HTTP {code}: {detail}") from exc
            if code == 413:
                raise RequestTooLarge(f"HTTP 413: {detail}") from exc
            if code == 500:
                raise _Retry500(detail) from exc
            if code == 503:
                raise _Wait503(detail) from exc
            raise InferenceError(f"HTTP {code}: {detail}") from exc
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise _NetworkError(str(exc)) from exc
        answers = payload.get("answers")
        if not isinstance(answers, dict):
            raise ProtocolError(f"response has no answers object: {str(payload)[:200]}")
        return answers


class _Retry500(Exception):
    pass


class _Wait503(Exception):
    pass


class _NetworkError(Exception):
    pass
