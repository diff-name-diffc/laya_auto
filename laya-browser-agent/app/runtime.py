"""Inference runtime: a pool of independent backend instances.

Laya's ``Agent.system_one`` is deliberately unguarded so concurrent calls can
share a checkpoint on a GPU, but its internal buffers are not documented as
re-entrant for MPS/CPU, and Python's GIL bounds true parallelism for CPU work
anyway. The safe, high-throughput arrangement on a Mac is:

* one backend instance per pool slot,
* each slot pinned to its own worker thread,
* a bounded queue in front of the pool.

With ``LAYA_POOL=1`` (the default) this is a serialised single-flight executor,
which is exactly what upstream ``laya-serve`` does. Raising it gives real
parallelism on a multi-core CPU when the per-request cost is CPU-bound.
"""

from __future__ import annotations

import asyncio
import queue
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, Optional

from .backends.base import Backend, BackendError, BackendUnavailable, DecisionResult, create_backend


class InferenceRuntime:
    def __init__(self, settings) -> None:
        self.settings = settings
        self._pool_size = max(1, int(settings.laya_pool)) if settings.backend == "laya" else 1
        self._backends: list[Backend] = []
        # One thread per slot, each owning exactly one backend instance.
        self._executor: Optional[ThreadPoolExecutor] = None
        # Round-robin dispatch of requests onto slots.
        self._slots: "queue.Queue[int]" = queue.Queue()
        self._primary: Optional[Backend] = None

    # -- lifecycle ---------------------------------------------------------
    def load_sync(self) -> None:
        """Build every backend instance. Called once before serving."""
        self._backends = [create_backend(self.settings.backend, self.settings)
                          for _ in range(self._pool_size)]
        # Load sequentially: concurrent first-time weight loads race the HF cache
        # and multiply peak memory.
        for b in self._backends:
            b.load()
        self._primary = self._backends[0]
        for i in range(self._pool_size):
            self._slots.put(i)
        self._executor = ThreadPoolExecutor(
            max_workers=self._pool_size, thread_name_prefix="infer"
        )

    def close(self) -> None:
        if self._executor is not None:
            self._executor.shutdown(wait=True, cancel_futures=True)
            self._executor = None
        for b in self._backends:
            try:
                b.close()
            except Exception:  # noqa: BLE001
                pass
        self._backends = []

    # -- serving -----------------------------------------------------------
    async def predict(
        self, state: Any, questions: Dict[str, Any], model: Optional[str] = None
    ) -> DecisionResult:
        """Run one decision off the event loop, on a pool slot."""
        if not self._backends or self._executor is None:
            raise BackendUnavailable("inference runtime is not loaded")

        loop = asyncio.get_running_loop()
        # Reserve a slot so each backend instance serves one request at a time.
        slot = await loop.run_in_executor(None, self._slots.get)
        backend = self._backends[slot]

        def _run() -> DecisionResult:
            try:
                return backend.predict(state, questions, model=model)
            finally:
                self._slots.put(slot)

        return await loop.run_in_executor(self._executor, _run)

    # -- introspection -----------------------------------------------------
    @property
    def loaded(self) -> bool:
        return bool(self._backends) and all(b.loaded for b in self._backends)

    @property
    def backend_name(self) -> str:
        return self.settings.backend

    def models(self) -> list[str]:
        out: list[str] = []
        for b in self._backends:
            for m in b.models():
                if m not in out:
                    out.append(m)
        return out

    def info(self) -> Dict[str, Any]:
        info: Dict[str, Any] = {
            "backend": self.backend_name,
            "loaded": self.loaded,
            "pool_size": len(self._backends),
        }
        if self._primary is not None:
            info.update(self._primary.info())
        return info
