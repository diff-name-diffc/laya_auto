"""Mind2Web -> benchmark cases.

Port of the official browser fine-tune's ``convert_mind2web.py`` so the cases use
the same element rendering and gold semantics. Two deliberate differences:

* **test split, not train.** The official converter reads ``data/train/`` and the
  published checkpoint trained on it. Evaluating on that split would measure
  memorisation; ``--split test`` (the default here) uses Mind2Web's held-out
  Cross-Task / Cross-Website / Cross-Domain tasks.

* **no value leakage.** The gold is only the operation and the target element;
  the text to type is not part of the decision being scored.

Each Mind2Web action becomes one case: goal = ``confirmed_task``, history = the
preceding ``action_reprs``, gold = the positive candidate.
"""

from __future__ import annotations

import json
import random
import re
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

ROLE = {
    "a": "link", "button": "button", "input": "textbox", "textarea": "textbox",
    "select": "combobox", "option": "option", "img": "img", "li": "listitem",
    "label": "label", "span": "generic", "div": "generic", "svg": "img",
    "h1": "heading", "h2": "heading", "h3": "heading", "p": "text",
    "td": "cell", "th": "columnheader", "tr": "row", "ul": "list",
}
MAX_NEG = 44
OPS = {"CLICK": "click", "TYPE": "fill", "SELECT": "select"}


def _require_bs4():
    try:
        from bs4 import BeautifulSoup  # noqa: F401
    except ImportError as exc:  # pragma: no cover
        raise SystemExit(
            "Mind2Web conversion needs beautifulsoup4 and lxml: "
            "pip install beautifulsoup4 lxml"
        ) from exc


def label_of(el) -> str:
    attrs = el.attrs
    for k in ("aria-label", "placeholder", "alt", "title"):
        v = attrs.get(k)
        if isinstance(v, list):
            v = " ".join(v)
        if v and str(v).strip():
            return str(v).strip()
    txt = " ".join(el.get_text(" ", strip=True).split())
    if txt:
        return txt[:80]
    v = attrs.get("value")
    if v:
        return str(v).strip()[:80]
    return str(attrs.get("name") or attrs.get("id") or el.name or "")[:60]


def kind_of(el) -> str:
    t = el.name
    typ = (el.attrs.get("type") or "").lower()
    if t == "select":
        return "select"
    if t in ("textarea",) or (t == "input" and typ in ("", "text", "search", "email", "password", "number", "tel", "url")) \
            or el.attrs.get("contenteditable"):
        return "fill"
    return "click"


def action_to_case(task: Dict[str, Any], ai: int, action: Dict[str, Any], rng: random.Random) -> Optional[Dict[str, Any]]:
    """Convert one annotated action into a benchmark case (or None if unusable)."""
    from bs4 import BeautifulSoup

    if not action.get("cleaned_html"):
        return None
    soup = BeautifulSoup(action["cleaned_html"], "lxml")
    by_id = {el.attrs["backend_node_id"]: el for el in soup.find_all(attrs={"backend_node_id": True})}

    pos = action.get("pos_candidates") or []
    if not pos:
        return None
    gold_el = by_id.get(pos[0]["backend_node_id"])
    if gold_el is None:
        return None

    negs = [c for c in (action.get("neg_candidates") or []) if c["backend_node_id"] in by_id]
    rng.shuffle(negs)
    cands = [pos[0]] + negs[:MAX_NEG]
    rng.shuffle(cands)

    op = (action.get("operation") or {}).get("op")
    if op not in OPS:
        return None

    # Values typed/selected earlier: a field that already holds its value shows it.
    filled: Dict[str, str] = {}
    for r in task["action_reprs"][:ai]:
        m = re.match(r"\[(\w+)\]\s+(.*?)\s+->\s+(TYPE|SELECT):\s*(.*)$", r)
        if m:
            filled[" ".join(m.group(2).split()).lower()] = m.group(4).strip()

    actions: List[Dict[str, Any]] = []
    gold_id: Optional[str] = None
    node = 0
    for c in cands:
        el = by_id[c["backend_node_id"]]
        lab = label_of(el)
        if not lab:
            continue
        node += 1
        is_gold = c["backend_node_id"] == pos[0]["backend_node_id"]
        kind = OPS[op] if is_gold else kind_of(el)
        role = ROLE.get(el.name, "generic")
        base = {"node": node, "label": lab, "role": role}
        if kind == "select":
            opts = [o.get_text(" ", strip=True) for o in el.find_all("option")][:8] or [action["operation"].get("value") or "option"]
            for oi, o in enumerate(opts):
                a = {**base, "id": f"select:{node}:{oi}", "kind": "select", "value": o,
                     "label": f"{lab} → {o}", "current_value": ""}
                actions.append(a)
                if is_gold and (o == action["operation"].get("value") or (oi == 0 and not action["operation"].get("value"))):
                    gold_id = a["id"]
            continue
        a = {**base, "id": f"{kind}:{node}", "kind": kind}
        if kind == "fill":
            a["value"] = filled.get(lab.lower(), "")
            a["current_value"] = a["value"]
        actions.append(a)
        if is_gold:
            gold_id = a["id"]

    if gold_id is None:
        return None

    for k, lab in (("wait", "Wait for the page to update"),
                   ("scroll_down", "Scroll down"), ("scroll_up", "Scroll up")):
        actions.append({"id": k, "kind": "wait" if k == "wait" else "scroll",
                        "label": lab, "node": None, "delta": 600 if k == "scroll_down" else -600})

    text = " ".join(soup.get_text(" ", strip=True).split())[:6000]
    history = []
    for r in task["action_reprs"][:ai]:
        lab_, _, opv = r.rpartition(" -> ")
        history.append({"action": lab_ or r, "kind": opv.lower() or "click", "text": None, "page_changed": True})

    return {
        "case_id": f"m2w-{task.get('annotation_id', ai)}-{ai}",
        "source": f"mind2web:{task.get('domain', 'unknown')}",
        "goal": task["confirmed_task"],
        "page": {
            "url": (task.get("website") or "") + "/" + str(task.get("subdomain") or ""),
            "title": task.get("domain") or "page",
            "text": text,
            "actions": actions,
        },
        "history": history,
        "gold_op": {"CLICK": "CLICK", "TYPE": "TYPE_TEXT", "SELECT": "SELECT"}[op],
        "gold_id": gold_id,
    }


def iter_cases(task_files: List[Path], max_cases: int = 0, seed: int = 11) -> Iterator[Dict[str, Any]]:
    """Yield cases from Mind2Web task JSON files."""
    rng = random.Random(seed)
    emitted = 0
    for path in task_files:
        try:
            tasks = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        for task in tasks:
            for ai in range(len(task.get("actions", []))):
                case = action_to_case(task, ai, task["actions"][ai], rng)
                if case is None:
                    continue
                yield case
                emitted += 1
                if max_cases and emitted >= max_cases:
                    return
