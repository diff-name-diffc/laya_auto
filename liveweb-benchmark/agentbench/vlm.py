"""The VLM side path, stage 1: the DONE gate (spec §2, L3-style in-loop check).

Why this insertion point: measured live-web failures are dominated by
**premature DONE at high confidence** (5 of 9), which element-relabeling (the
classic L2) cannot touch -- the labels were already fine. Gating the *terminal*
choice with one bounded VLM judgment turns the spec's post-hoc independent
verifier (§6) into an in-loop correction: a rejected DONE feeds back
"still missing: X" and the loop re-decides.

Main path stays DOM-only forever (invariant 6): without a configured endpoint
the gate is absent and every check passes as before.

The client speaks any OpenAI-compatible vision endpoint (GLM-4V family,
Qwen-VL, vLLM serving, ...):
    POST {base_url}/chat/completions  with  image_url: data:image/png;base64,...
"""

from __future__ import annotations

import base64
import json
import re
import time
import urllib.error
import urllib.request
from typing import Any, Callable, Dict, Optional


class VisionJudge:
    """Minimal OpenAI-compatible vision chat client (stdlib only)."""

    def __init__(self, base_url: str, model: str, api_key: Optional[str] = None,
                 timeout: float = 120.0, max_tokens: int = 8000):
        # generous max_tokens: reasoning models spend budget on thinking before
        # the visible answer, and a length-capped reply has empty content
        # (measured: 4000 still ran out on the element-table rescue prompt)
        self.url = base_url.rstrip("/") + "/chat/completions"
        self.model = model
        self.api_key = api_key
        self.timeout = timeout
        self.max_tokens = max_tokens

    def ask(self, image_b64: str, prompt: str) -> str:
        body = json.dumps({
            "model": self.model,
            "temperature": 0,
            "max_tokens": self.max_tokens,
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url",
                     "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
                ],
            }],
        }).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        def _post():
            req = urllib.request.Request(self.url, data=body, headers=headers, method="POST")
            return urllib.request.urlopen(req, timeout=self.timeout)

        try:
            with _post() as resp:
                payload = json.load(resp)
        except urllib.error.HTTPError as exc:
            if exc.code >= 500:
                time.sleep(2.0)   # transient gateway: one retry
                with _post() as resp:
                    payload = json.load(resp)
            else:
                raise
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            # timeouts cluster when the endpoint is loaded; thinking is
            # stochastic so a retry often completes (measured top failure)
            time.sleep(3.0)
            try:
                with _post() as resp:
                    payload = json.load(resp)
            except (urllib.error.URLError, TimeoutError, OSError) as exc2:
                raise ValueError(f"vision endpoint unreachable twice: {exc} / {exc2}") from exc2
        message = payload["choices"][0]["message"]
        content = message.get("content") or ""
        if not content.strip():
            # a length-capped thinking pass leaves content empty; one retry
            # often lands (thinking is stochastic)
            time.sleep(1.0)
            req = urllib.request.Request(self.url, data=body, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                payload = json.load(resp)
            content = payload["choices"][0]["message"].get("content") or ""
            if not content.strip():
                raise ValueError("empty content from vision model after retry "
                                 f"(finish={payload['choices'][0].get('finish_reason')})")
        return content


def extract_json(text: str) -> Dict[str, Any]:
    """Pull the first JSON object out of a model reply (models love prose)."""
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        raise ValueError(f"no JSON object in reply: {text[:120]!r}")
    return json.loads(match.group(0))


def make_done_gate(judge: VisionJudge) -> Callable[[Any, str, Dict[str, Any]], Dict[str, Any]]:
    """Build the gate: (page, goal, obs) -> {"satisfied": bool, "missing": [..]}.

    Bounded by the judge's own HTTP timeout; any raise propagates and the loop
    fails OPEN (a broken VLM must never wedge the run -- invariant 6).
    """

    def gate(page, goal: str, obs: Dict[str, Any]) -> Dict[str, Any]:
        shot = page.screenshot(full_page=False, type="jpeg", quality=70)
        image_b64 = base64.b64encode(shot).decode("ascii")
        prompt = (
            "You are the independent verifier of a web-automation agent.\n"
            f"GOAL: {goal}\n"
            f"PAGE URL: {obs.get('url', '')}\n"
            f"PAGE TEXT (excerpt): {(obs.get('text') or '')[:1500]}\n\n"
            "Look at the screenshot. Are ALL requirements of the goal visibly "
            "satisfied on THIS page right now?\n"
            "Interpret the goal literally, no more no less: 'search for X and "
            "open/show/view the results' is satisfied by a search-results page "
            "listing results for X; only a goal that says to OPEN a specific "
            "result, article, or repository requires navigating into one.\n"
            "For multi-step goals ('first A, then B'), judge the page against "
            "the LAST requirement only: earlier steps are expected to be done "
            "and gone, and their evidence is NOT required to still be visible.\n"
            "Be strict about evidence: a link that might lead to the answer is "
            "NOT satisfaction; a search box is NOT results.\n"
            'Reply with STRICT JSON only: {"satisfied": true, "missing": []} '
            'or {"satisfied": false, "missing": ["short missing item", ...]}'
        )
        reply = judge.ask(image_b64, prompt)
        verdict = extract_json(reply)
        if not isinstance(verdict.get("satisfied"), bool):
            raise ValueError(f"satisfied is not a bool: {reply[:120]!r}")
        verdict.setdefault("missing", [])
        return verdict

    return gate


def make_rescue(judge: VisionJudge) -> Callable[[Any, str, Dict[str, Any], str], Optional[Dict[str, Any]]]:
    """Build the rescue actor: (page, goal, obs, problem) -> {"id", "text"?}.

    When the fast model is stuck (a rejected DONE, a repeat loop, an empty-field
    submit storm), System-2 picks ONE next action from the observed table. The
    loop validates the returned id against the table -- the VLM can never name
    an element that was not observed (spec §2.6 invariant 1).
    """

    def rescue(page, goal: str, obs: Dict[str, Any], problem: str) -> Optional[Dict[str, Any]]:
        shot = page.screenshot(full_page=False, type="jpeg", quality=70)
        image_b64 = base64.b64encode(shot).decode("ascii")
        rows = []
        for a in obs.get("actions", []):
            cur = f" | now={str(a.get('current_value') or '')[:30]!r}" if a.get("current_value") else ""
            rows.append(f"  {a['id']} | {a['kind']} | {str(a.get('label') or '')[:60]}{cur}")
        prompt = (
            "You are the corrective actor in a web-automation loop. The fast "
            "decision model got stuck; you choose exactly ONE next action.\n"
            f"GOAL: {goal}\n"
            f"PROBLEM: {problem}\n"
            f"PAGE URL: {obs.get('url', '')}\n"
            f"PAGE TEXT (excerpt): {(obs.get('text') or '')[:1000]}\n\n"
            "Screenshot + the observed action table (id | kind | label):\n"
            + "\n".join(rows[:80])
            + "\n\nPick the single action that best advances the goal. Prefer "
              "the most direct progress over exploration. If the page has an empty "
              "search/query field and the goal needs a search or navigation to a "
              "specific page, CHOOSE THE FILL action for that field and give the "
              "exact text to type (derive it from the goal).\n"
              "On list or feed pages (GitHub trending, search results, topic "
              "feeds), pick the CONTENT-ITEM entry link that matches the goal "
              "(an 'owner / repo' repository row, a result headline) -- never "
              "sidebar navigation, filter dropdowns ('Language: Any'), or utility "
              "controls. If the goal asks to OPEN an item that is already listed "
              "on the page, click its entry link directly; do NOT open a search "
              "box or type instead. If no listed item matches the goal's topic, "
              "click the FIRST (topmost) content entry -- opening a listed item "
              "always beats searching when the goal just needs a repository or "
              "article opened.\n"
              "The id MUST be copied EXACTLY from the table's id column (it looks "
              "like 'click:25', 'fill:8', 'press_enter', 'scroll_down'). You may "
              'also add "label" to disambiguate.\n'
              'Reply STRICT JSON only: {"id": "<exact id>", "label": "<optional>"} '
              'or for a fill {"id": "<fill id>", "text": "..."}'
        )
        reply = judge.ask(image_b64, prompt)
        choice = extract_json(reply)
        if not isinstance(choice.get("id"), str):
            raise ValueError(f"no action id in reply: {reply[:120]!r}")
        return choice

    return rescue
