"""Laya backend: the System-1 decision model.

Two modes, chosen with ``LAYA_MODE``:

* ``router`` (default) -- upstream's recommended production path. A ``Router``
  holds the official checkpoints and auto-selects one per request from the
  state's script/language. Use this for the stock English / multilingual /
  typed-decisions models.
* ``agent`` -- a single ``Agent`` loaded from one checkpoint, including a local
  directory or a community fine-tune. Use this for a bespoke head such as
  ``cklxx/laya-browser`` (set ``LAYA_MODEL`` to the repo/path and
  ``LAYA_SUBFOLDER`` to the variant folder).

Laya's ``predict()`` already returns the Jev ``{model, answers, usage,
routing?}`` shape, so the payload is passed through untouched.
"""

from __future__ import annotations

import os
import threading
import time
from typing import Any, Dict, List, Optional

from .base import Backend, BackendError, BackendUnavailable, DecisionResult, register


class LayaBackend(Backend):
    name = "laya"

    def __init__(self, settings) -> None:
        super().__init__(settings)
        self._mode = settings.laya_mode
        self._lock = threading.Lock()
        self._router = None
        self._agent = None
        self._model_ids: List[str] = []

    # -- lifecycle ---------------------------------------------------------
    def load(self) -> None:
        # Laya probes for TensorFlow at import and can deadlock when TF's abseil
        # runtime is present; upstream documents USE_TF=0 as the fix.
        os.environ.setdefault("USE_TF", "0")

        if self.settings.laya_threads:
            try:
                import torch

                torch.set_num_threads(int(self.settings.laya_threads))
            except Exception:  # noqa: BLE001 -- a thread cap must never block startup
                pass

        try:
            if self._mode == "agent":
                self._load_agent()
            else:
                self._load_router()
        except BackendUnavailable:
            raise
        except Exception as exc:  # noqa: BLE001
            raise BackendUnavailable(f"failed to load Laya: {exc}") from exc
        self._loaded = True

    def _load_router(self) -> None:
        from laya.router import Router

        router = Router(
            device=self.settings.laya_device or None,
            auto_task_detection=self.settings.laya_auto_task,
        )
        if self.settings.laya_preload:
            names = None
            if self.settings.laya_models:
                names = [m.strip() for m in self.settings.laya_models.split(",") if m.strip()]
            router.preload(names)
        self._router = router
        self._model_ids = list(getattr(router, "loaded", None) or
                               ("english", "multilingual", "typed-decisions"))

    def _load_agent(self) -> None:
        import laya

        kwargs: Dict[str, Any] = {"device": self.settings.laya_device or None}
        if self.settings.laya_subfolder:
            kwargs["subfolder"] = self.settings.laya_subfolder
        agent = laya.load(self.settings.laya_model, **kwargs)

        # Fine-tuned checkpoints record the head budget they were trained with;
        # a browser fine-tune needs the wider head to keep every candidate
        # element distinct (upstream's own guidance).
        cfg = getattr(agent, "cfg", {}) or {}
        if cfg.get("head_max_len_train"):
            cfg["head_max_len"] = cfg["head_max_len_train"]
        self._agent = agent
        label = self.settings.laya_model
        if self.settings.laya_subfolder:
            label = f"{label}/{self.settings.laya_subfolder}"
        self._model_ids = [label]

    def close(self) -> None:
        for obj in (self._router, self._agent):
            unload = getattr(obj, "unload", None)
            if callable(unload):
                try:
                    unload()
                except Exception:  # noqa: BLE001
                    pass
        self._router = self._agent = None
        self._loaded = False

    # -- serving -----------------------------------------------------------
    def predict(self, state, questions, model: Optional[str] = None) -> DecisionResult:
        started = time.perf_counter()
        try:
            with self._lock:
                if self._router is not None:
                    # Upstream's Router ignores unknown model ids and auto-selects.
                    out = self._router.predict(state, questions, model=model)
                else:
                    out = self._agent.predict(state, questions)
        except ValueError as exc:
            # Question/answer validation errors name what to fix: safe to return.
            raise BackendError(str(exc)) from exc

        latency_ms = (time.perf_counter() - started) * 1000.0
        payload = dict(out)
        routing = payload.get("routing")
        return DecisionResult(
            payload=payload,
            latency_ms=round(latency_ms, 3),
            backend=self.name,
            meta={"routing": routing} if routing else {},
        )

    # -- introspection -----------------------------------------------------
    def models(self) -> List[str]:
        return list(self._model_ids)

    def info(self) -> Dict[str, Any]:
        info = super().info()
        info.update({
            "mode": self._mode,
            "model": self.settings.laya_model,
            "device": self._resolve_device(),
        })
        return info

    def _resolve_device(self) -> str:
        if self.settings.laya_device:
            return self.settings.laya_device
        try:
            import torch

            if torch.cuda.is_available():
                return "cuda"
            if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
                return "mps"
        except Exception:  # noqa: BLE001
            pass
        return "cpu"


register("laya", LayaBackend)
