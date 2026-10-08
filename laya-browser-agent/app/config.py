"""Central configuration.

Everything is environment-driven so the same entrypoint serves a laptop dev run
and a long-lived LAN service. Names mirror upstream ``laya-serve`` where a
variable means the same thing, so operators can reuse muscle memory.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Optional

# Guardrails for unauthenticated remote input (mirrors upstream laya.serve).
MAX_QUESTIONS = 64
MAX_STATE_CHARS = 50_000
MAX_BODY_BYTES = 2 * 1024 * 1024


def _env_str(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.environ.get(name)
    return value if value not in (None, "") else default


def _env_int(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _env_bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None or raw == "":
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


@dataclass
class Settings:
    """Resolved server settings."""

    # --- HTTP surface -----------------------------------------------------
    host: str = "0.0.0.0"          # LAN by default; the whole point of start.sh
    port: int = 8000
    api_key: Optional[str] = None  # when set, require Authorization: Bearer
    log_level: str = "info"
    # Public base URL used only in the docs/OpenAPI description.
    public_base_url: Optional[str] = None

    # --- Runtime ----------------------------------------------------------
    backend: str = "laya"
    # Thread pool size for *synchronous* inference. Laya inference is blocking
    # torch; it must never run on the event loop.
    workers: int = 1
    # uvicorn tuning for LAN throughput.
    limit_concurrency: Optional[int] = None
    backlog: int = 2048
    timeout_keep_alive: int = 30

    # --- Laya backend -----------------------------------------------------
    laya_mode: str = "router"              # router | agent
    laya_model: str = "convaiinnovations/laya"
    laya_subfolder: Optional[str] = None
    laya_models: Optional[str] = None      # comma list to preload (router mode)
    laya_preload: bool = True
    laya_device: Optional[str] = None      # None -> auto (cuda > mps > cpu)
    laya_auto_task: bool = False
    laya_threads: Optional[int] = None
    laya_pool: int = 1                     # independent Agent instances (real parallelism)

    extra: dict = field(default_factory=dict)

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            host=_env_str("INFER_HOST", _env_str("LAYA_HOST", "0.0.0.0")),
            port=_env_int("INFER_PORT", _env_int("LAYA_PORT", 8000)),
            api_key=_env_str("INFER_API_KEY", _env_str("LAYA_API_KEY")),
            log_level=_env_str("INFER_LOG_LEVEL", _env_str("LAYA_LOG_LEVEL", "info")),
            public_base_url=_env_str("INFER_PUBLIC_BASE_URL"),
            backend=_env_str("INFER_BACKEND", "laya"),
            workers=max(1, _env_int("INFER_WORKERS", 1)),
            limit_concurrency=(_env_int("INFER_LIMIT_CONCURRENCY", 0) or None),
            backlog=_env_int("INFER_BACKLOG", 2048),
            timeout_keep_alive=_env_int("INFER_KEEP_ALIVE", 30),
            laya_mode=_env_str("LAYA_MODE", "router"),
            laya_model=_env_str("LAYA_MODEL", "convaiinnovations/laya"),
            laya_subfolder=_env_str("LAYA_SUBFOLDER"),
            laya_models=_env_str("LAYA_MODELS"),
            laya_preload=_env_bool("LAYA_PRELOAD", True),
            laya_device=_env_str("LAYA_DEVICE"),
            laya_auto_task=_env_bool("LAYA_AUTO_TASK", False),
            laya_threads=_env_int("LAYA_THREADS", 0) or None,
            laya_pool=max(1, _env_int("LAYA_POOL", 1)),
        )


settings = Settings.from_env()
