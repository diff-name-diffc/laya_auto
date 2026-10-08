"""Protocol-layer tests. Run without a model: the fake backend stands in.

    cd inference-server && python -m pytest -q
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

import fake_backend  # noqa: E402,F401  (registers the fake backends)
from app.config import Settings  # noqa: E402
from app.protocol import create_app  # noqa: E402
from app.runtime import InferenceRuntime  # noqa: E402


def make_client(backend="fake", **overrides):
    settings = Settings.from_env()
    settings.backend = backend
    for k, v in overrides.items():
        setattr(settings, k, v)
    runtime = InferenceRuntime(settings)
    runtime.load_sync()
    return TestClient(create_app(runtime, settings))


EMAIL = {
    "state": {"body": "We were billed twice. Please refund today or we cancel."},
    "questions": {
        "department": {"type": "choice", "instructions": "Which dept?",
                       "criteria": {"billing": "payments", "tech": "bugs"}},
        "churn": {"type": "noul", "instructions": "Cancel threat?"},
        "urgency": {"type": "score", "instructions": "How urgent?",
                    "criteria": ["low", "high"]},
    },
}


def test_health_ok():
    with make_client() as c:
        r = c.get("/health")
        assert r.status_code == 200
        body = r.json()
        assert body["status"] == "ok"
        assert body["loaded"] is True
        assert body["backend"] == "fake"


def test_list_models():
    with make_client() as c:
        r = c.get("/v1/models")
        assert r.status_code == 200
        ids = [m["id"] for m in r.json()["data"]]
        assert ids == ["fake"]


def test_systemone_answer_shapes():
    with make_client() as c:
        r = c.post("/v1/systemone", json=EMAIL)
        assert r.status_code == 200, r.text
        body = r.json()
        assert set(body) >= {"model", "answers", "usage"}
        assert body["answers"]["department"]["type"] == "choice"
        assert body["answers"]["churn"]["type"] == "noul"
        assert body["answers"]["urgency"]["type"] == "score"
        assert body["usage"] == {"input_tokens": 0, "output_tokens": 0}
        assert body["routing"]["model"] == "fake"


def test_unknown_model_falls_back_to_auto():
    """A client hardcoding `jev-latest` must still be served (upstream parity)."""
    with make_client() as c:
        r = c.post("/v1/systemone", json={**EMAIL, "model": "jev-latest"})
        assert r.status_code == 200, r.text


def test_malformed_json_is_400():
    with make_client() as c:
        r = c.post("/v1/systemone", content=b"{not json",
                   headers={"content-type": "application/json"})
        assert r.status_code == 400
        assert "JSON" in r.json()["detail"]


def test_missing_questions_is_400():
    with make_client() as c:
        r = c.post("/v1/systemone", json={"state": "hi"})
        assert r.status_code == 400
        assert "questions" in r.json()["detail"]


def test_questions_not_object_is_400():
    with make_client() as c:
        r = c.post("/v1/systemone", json={"state": "hi", "questions": [1, 2]})
        assert r.status_code == 400


def test_too_many_questions_is_413():
    questions = {f"q{i}": {"type": "noul", "instructions": "x"} for i in range(100)}
    with make_client() as c:
        r = c.post("/v1/systemone", json={"state": "hi", "questions": questions})
        assert r.status_code == 413
        assert "too many questions" in r.json()["detail"]


def test_oversized_state_is_413():
    with make_client() as c:
        r = c.post("/v1/systemone", json={"state": "x" * 60_000, "questions": {}})
        assert r.status_code == 413
        assert "state too large" in r.json()["detail"]


def test_body_over_cap_is_413():
    with make_client() as c:
        big = b'{"state":"' + b"a" * (3 * 1024 * 1024) + b'","questions":{}}'
        r = c.post("/v1/systemone", content=big,
                   headers={"content-type": "application/json"})
        assert r.status_code == 413


def test_backend_error_is_422():
    with make_client(backend="error") as c:
        r = c.post("/v1/systemone", json=EMAIL)
        assert r.status_code == 422
        assert "head_max_len" in r.json()["detail"]


def test_auth_required_when_key_set():
    with make_client(api_key="s3cret") as c:
        assert c.post("/v1/systemone", json=EMAIL).status_code == 401
        ok = c.post("/v1/systemone", json=EMAIL,
                    headers={"Authorization": "Bearer s3cret"})
        assert ok.status_code == 200
        bad = c.post("/v1/systemone", json=EMAIL,
                     headers={"Authorization": "Bearer nope"})
        assert bad.status_code == 401


def test_non_ascii_bearer_does_not_500():
    """A legal-on-the-wire non-ASCII header must answer 401, not crash.

    Sent as raw latin-1 bytes: httpx refuses to encode a non-ASCII *str* header,
    but such a header is legal on the wire and Starlette decodes it as latin-1.
    Upstream hardened exactly this path (hmac.compare_digest raises TypeError on
    a non-ASCII str), so it is worth pinning.
    """
    with make_client(api_key="s3cret") as c:
        r = c.post("/v1/systemone", json=EMAIL,
                   headers={"Authorization": "Bearer s\u00e9cret".encode("latin-1")})
        assert r.status_code == 401
