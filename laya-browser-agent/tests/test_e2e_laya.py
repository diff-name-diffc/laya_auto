"""End-to-end test with the real Laya model over HTTP.

Skips automatically when ``laya`` is not installed or a checkpoint is not
available locally, so the default test run stays fast. Set
``LAYA_E2E_MODEL`` to a local checkpoint directory (or leave it to use the
downloaded HF cache) to opt in.

    LAYA_E2E_MODEL=convaiinnovations/laya python -m pytest -q tests/test_e2e_laya.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

pytest.importorskip("laya", reason="the laya package is not installed")

from app.config import Settings  # noqa: E402
from app.protocol import create_app  # noqa: E402
from app.runtime import InferenceRuntime  # noqa: E402


@pytest.fixture(scope="module")
def client():
    settings = Settings.from_env()
    settings.backend = "laya"
    settings.laya_mode = "agent"
    settings.laya_model = os.environ.get("LAYA_E2E_MODEL", "convaiinnovations/laya")
    settings.laya_subfolder = os.environ.get("LAYA_SUBFOLDER") or None
    settings.laya_device = os.environ.get("LAYA_DEVICE") or None
    runtime = InferenceRuntime(settings)
    try:
        runtime.load_sync()
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"could not load Laya checkpoint: {exc}")
    with TestClient(create_app(runtime, settings)) as c:
        yield c


def test_health_reports_laya(client):
    body = client.get("/health").json()
    assert body["loaded"] is True
    assert body["backend"] == "laya"


def test_choice_answer(client):
    r = client.post("/v1/systemone", json={
        "state": {"body": "We were billed twice for March. Refund today or we cancel."},
        "questions": {"department": {
            "type": "choice", "instructions": "Which department should handle this?",
            "criteria": {"billing": "invoices, payments, refunds",
                         "technical": "bugs, outages", "other": "everything else"}}},
    })
    assert r.status_code == 200, r.text
    ans = r.json()["answers"]["department"]
    assert ans["type"] == "choice"
    assert ans["choice"] in {"billing", "technical", "other"}
    assert abs(sum(ans["probabilities"].values()) - 1.0) < 0.02


def test_noul_and_score(client):
    r = client.post("/v1/systemone", json={
        "state": {"body": "Please cancel my subscription immediately."},
        "questions": {
            "churn": {"type": "noul", "instructions": "Does the user threaten to cancel?"},
            "urgency": {"type": "score", "instructions": "How urgent?",
                        "criteria": ["low", "medium", "high"]},
        },
    })
    assert r.status_code == 200, r.text
    answers = r.json()["answers"]
    assert 0.0 <= answers["churn"]["noul"] <= 1.0
    assert answers["urgency"]["legend"] == {"0": "low", "1": "medium", "2": "high"}


def test_invalid_question_type_is_422(client):
    r = client.post("/v1/systemone", json={
        "state": "hello",
        "questions": {"bad": {"type": "not-a-type", "instructions": "x"}},
    })
    assert r.status_code == 422
