"""The text helper that supplies the characters to type (spec §0/§4).

It plays the role of jev-ultrafast's small LLM text helper: it supplies only the
characters, chosen from the task's ``queries``. It never chooses the operation
or the element -- those stay the decision model's job. It refuses anything that
is not an allowed query, so a run cannot cheat by inventing text.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List


def text_provider_for(queries: List[str]) -> Callable[[Dict[str, Any]], str]:
    """Bind a provider to a task's allowed literal query strings."""
    if not queries:
        raise ValueError("task has no queries; a fill step cannot be typed")

    def provider(context: Dict[str, Any]) -> str:
        field = (context.get("field") or {})
        label = (field.get("label") or "").lower()
        page_text = (context.get("page") or {}).get("text", "").lower()
        # pick the query whose tokens best match the field label / page text
        best, best_score = queries[0], -1.0
        for q in queries:
            toks = [t for t in q.lower().split() if len(t) > 2]
            score = (sum(1 for t in toks if t in label) * 2
                     + sum(1 for t in toks if t in page_text) * 0.1)
            if score > best_score:
                best, best_score = q, score
        return best

    return provider
