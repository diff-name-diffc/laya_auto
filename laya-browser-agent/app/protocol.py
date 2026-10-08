"""Protocol layer: the Jev-compatible ``POST /v1/systemone`` surface.

The wire contract is upstream ``laya-serve``'s, byte-for-byte where it matters,
so any existing Jev client works by pointing its base URL here. Semantics kept
identical to upstream:

* ``POST /v1/systemone`` -> ``{model, answers, usage, routing?}``
* ``401`` invalid/missing bearer token (only when an API key is configured)
* ``400`` malformed JSON, or a non-object body / missing ``questions``
* ``413`` body / question-count / state-size over the caps
* ``422`` model-side question validation error (the message names the question)
* ``500`` any other inference failure, with no internal detail leaked

Additions that do not change the contract: ``GET /v1/models`` and a richer
``GET /health``.
"""

from __future__ import annotations

import hmac
import json
import os
from contextlib import asynccontextmanager
from typing import Any, Dict, Optional

from fastapi import FastAPI, Header, HTTPException, Request

from .config import (
    MAX_BODY_BYTES,
    MAX_QUESTIONS,
    MAX_STATE_CHARS,
    Settings,
    settings as default_settings,
)
from .backends.base import BackendError, BackendUnavailable
from .runtime import InferenceRuntime


def _check_request_limits(state: Any, questions: Any) -> None:
    """Reject oversized inference requests before tokenization (413)."""
    if not isinstance(questions, dict):
        raise HTTPException(status_code=400, detail="'questions' must be an object")
    if len(questions) > MAX_QUESTIONS:
        raise HTTPException(
            status_code=413,
            detail="too many questions (%d > %d)" % (len(questions), MAX_QUESTIONS),
        )
    try:
        state_len = len(state) if isinstance(state, str) else len(str(state))
    except Exception:  # noqa: BLE001
        state_len = MAX_STATE_CHARS + 1
    if state_len > MAX_STATE_CHARS:
        raise HTTPException(
            status_code=413,
            detail="state too large (%d > %d chars)" % (state_len, MAX_STATE_CHARS),
        )


async def _read_body_capped(request: Request) -> bytes:
    """Stream the body, abandoning it once it exceeds the cap.

    ``Content-Length`` is client-chosen and absent under chunked encoding, so
    the streaming cap is what actually enforces the limit for every framing.
    """
    total = 0
    chunks: list[bytes] = []
    async for chunk in request.stream():
        if not chunk:
            continue
        total += len(chunk)
        if total > MAX_BODY_BYTES:
            raise HTTPException(status_code=413, detail="request body too large")
        chunks.append(chunk)
    return b"".join(chunks)


def create_app(runtime: InferenceRuntime, settings: Optional[Settings] = None) -> FastAPI:
    settings = settings or default_settings
    api_key = settings.api_key
    # Encode both sides as bytes: hmac.compare_digest raises TypeError on a str
    # operand holding a non-ASCII char, and Starlette decodes headers as latin-1.
    expected_auth = ("Bearer " + api_key).encode("utf-8", "surrogateescape") if api_key else b""

    def _check_auth(authorization: Optional[str]) -> None:
        if api_key is None:
            return
        supplied = (authorization or "").encode("utf-8", "surrogateescape")
        if not hmac.compare_digest(supplied, expected_auth):
            raise HTTPException(status_code=401, detail="invalid or missing bearer token")

    @asynccontextmanager
    async def lifespan(_app: FastAPI):
        # The runtime is built by the entrypoint (so a load failure fails fast
        # and loudly); the app only tears it down.
        try:
            yield
        finally:
            runtime.close()

    app = FastAPI(
        title="local-inference-server",
        summary="Local decision/LLM inference over the TypeSafe Jev /v1/systemone protocol",
        version="0.1.0",
        lifespan=lifespan,
    )

    # -- routes ------------------------------------------------------------
    @app.get("/health", tags=["ops"])
    def health() -> Dict[str, Any]:
        info = runtime.info()
        return {
            "status": "ok" if runtime.loaded else "loading",
            "loaded": runtime.loaded,
            "backend": info.get("backend"),
            "device": info.get("device"),
            "mode": info.get("mode"),
            "pool_size": info.get("pool_size"),
            "models": runtime.models(),
        }

    @app.get("/v1/models", tags=["protocol"])
    def list_models() -> Dict[str, Any]:
        return {
            "object": "list",
            "data": [
                {"id": name, "object": "model", "owned_by": runtime.backend_name}
                for name in runtime.models()
            ],
        }

    @app.post("/v1/systemone", tags=["protocol"])
    async def systemone(
        request: Request, authorization: Optional[str] = Header(default=None)
    ) -> Dict[str, Any]:
        _check_auth(authorization)

        # A declared length over the cap is rejected before anything is read.
        declared = request.headers.get("content-length")
        if declared:
            try:
                if int(declared) > MAX_BODY_BYTES:
                    raise HTTPException(status_code=413, detail="request body too large")
            except ValueError:
                pass

        raw = await _read_body_capped(request)
        try:
            body = json.loads(raw)
        except ValueError:
            raise HTTPException(status_code=400, detail="request body must be valid JSON")

        if not isinstance(body, dict) or "questions" not in body:
            raise HTTPException(
                status_code=400,
                detail="request body must be an object with a 'questions' field",
            )

        state = body.get("state")
        questions = body["questions"]
        _check_request_limits(state, questions)
        model = _resolve_model(body.get("model"), runtime)

        try:
            result = await runtime.predict(state, questions, model=model)
        except BackendError as exc:
            # Model-side validation: the message names the question and the fix.
            raise HTTPException(status_code=422, detail=str(exc))
        except BackendUnavailable as exc:
            raise HTTPException(status_code=503, detail=str(exc))
        except HTTPException:
            raise
        except Exception:  # noqa: BLE001 -- never leak paths/weights/OOM text
            raise HTTPException(status_code=500, detail="inference failed")

        payload = dict(result.payload)
        # Preserve upstream's passthrough shape; add latency as a trailer field
        # only when the backend has not already placed it.
        payload.setdefault("usage", {"input_tokens": 0, "output_tokens": 0})
        return payload

    return app


def _resolve_model(model: Optional[str], runtime: InferenceRuntime) -> Optional[str]:
    """Pass through a model id the backend recognises; otherwise auto-select.

    Mirrors upstream ``laya-serve``: a client's ``model`` is honoured when it
    names something the backend serves, and ignored otherwise (the Router then
    auto-selects), so a caller that hardcodes ``jev-latest`` still works.
    """
    if not model or not isinstance(model, str):
        return None
    known = set(runtime.models())
    if model in known:
        return model
    return None
