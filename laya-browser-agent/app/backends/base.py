"""Backend contract + registry.

A backend owns a local model and answers decision requests. The HTTP layer is
model-agnostic: it hands a backend ``(state, questions, model)`` and serialises
whatever ``DecisionResult`` comes back. Adding a new local model means writing
one backend subclass and registering it -- no changes to the protocol layer.
"""

from __future__ import annotations

import abc
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class DecisionResult:
    """The model's answer, already in the Jev ``/v1/systemone`` shape.

    ``payload`` is what goes on the wire: ``{model, answers, usage, routing?}``.
    Keeping it a plain dict means a backend that is already Jev-shaped (Laya)
    passes its output through untouched, and a future backend maps its own
    output into this shape.
    """

    payload: Dict[str, Any]
    latency_ms: float = 0.0
    backend: str = ""
    meta: Dict[str, Any] = field(default_factory=dict)


class BackendError(RuntimeError):
    """Raised by a backend for client-correctable problems (-> HTTP 422)."""


class BackendUnavailable(RuntimeError):
    """Raised when a backend cannot serve a request (-> HTTP 503)."""


class Backend(abc.ABC):
    """Base class for every local-inference backend."""

    #: short identifier, also the value of ``INFER_BACKEND``
    name: str = "base"

    def __init__(self, settings) -> None:
        self.settings = settings
        self._loaded = False

    # -- lifecycle ---------------------------------------------------------
    @abc.abstractmethod
    def load(self) -> None:
        """Load weights / build the runtime. Called once at startup."""

    def close(self) -> None:
        """Release resources. Best-effort; must not raise."""

    # -- serving -----------------------------------------------------------
    @abc.abstractmethod
    def predict(
        self,
        state: Any,
        questions: Dict[str, Any],
        model: Optional[str] = None,
    ) -> DecisionResult:
        """Answer ``questions`` about ``state``.

        Implementations are synchronous and blocking; the HTTP layer runs them
        in a thread pool so the event loop stays responsive.
        """

    # -- introspection -----------------------------------------------------
    @property
    def loaded(self) -> bool:
        return self._loaded

    def models(self) -> List[str]:
        """Model identifiers this backend can serve (for ``GET /v1/models``)."""
        return []

    def info(self) -> Dict[str, Any]:
        return {"backend": self.name, "loaded": self._loaded}


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

_FACTORIES: Dict[str, Callable[[Any], Backend]] = {}


def register(name: str, factory: Callable[[Any], Backend]) -> None:
    _FACTORIES[name] = factory


def create_backend(name: str, settings) -> Backend:
    """Instantiate a backend by name, importing built-ins lazily."""
    if name not in _FACTORIES:
        _load_builtin(name)
    if name not in _FACTORIES:
        known = ", ".join(sorted(_FACTORIES)) or "(none)"
        raise BackendUnavailable(f"unknown backend {name!r}; known: {known}")
    return _FACTORIES[name](settings)


def _load_builtin(name: str) -> None:
    """Import built-in backend modules so they can self-register."""
    if name == "laya":
        from . import laya_backend  # noqa: F401
