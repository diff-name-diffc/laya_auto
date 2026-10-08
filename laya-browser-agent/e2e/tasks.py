"""Google research tasks with independent, objective verification.

The point of this suite is that **success is not the model's DONE choice**. After
each run, a verifier inspects the final page — its URL, title and text — and
checks for evidence that is only present if the research actually happened. A
model that declares DONE on the search box fails.

Each task supplies:

* ``goal``    -- the natural-language instruction the agent receives;
* ``queries`` -- literal strings the text helper may type (an offline stand-in
  for the LLM text helper; it does not decide *what* to do, only supplies the
  characters, exactly as jev-ultrafast outsources text generation);
* ``expect``  -- the verifier: a set of conditions on the final page. All must
  hold. Conditions are checked against url + title + lowercased text.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Task:
    task_id: str
    goal: str
    queries: List[str]
    # verification: any_of groups; every group must have >=1 hit, and none of `forbid` may appear
    require_any: List[List[str]] = field(default_factory=list)
    forbid: List[str] = field(default_factory=list)
    expect_url_contains: Optional[str] = None
    note: str = ""

    def verify(self, page: Dict[str, Any]) -> Dict[str, Any]:
        """Independently check the final page. Returns {passed, checks}."""
        text = (page.get("text") or "").lower()
        title = (page.get("title") or "").lower()
        url = (page.get("url") or "").lower()
        haystack = f"{url}\n{title}\n{text}"

        checks: Dict[str, Any] = {"url": url[:120]}
        # A bot challenge is a failed run, not a satisfied goal -- check first.
        blocked = (("sorry/index" in url) or ("unusual traffic" in text)
                   or ("complete the following challenge" in text) or ("not a robot" in text))
        checks["bot_challenge"] = blocked
        if blocked:
            return {"passed": False, "checks": checks}

        groups_ok = True
        for i, group in enumerate(self.require_any):
            hit = [g for g in group if g.lower() in haystack]
            checks[f"group{i}"] = hit
            if not hit:
                groups_ok = False
        checks["forbidden_found"] = [f for f in self.forbid if f.lower() in haystack]
        url_ok = (self.expect_url_contains is None) or (self.expect_url_contains.lower() in url)
        checks["url_ok"] = url_ok

        passed = groups_ok and not checks["forbidden_found"] and url_ok
        return {"passed": passed, "checks": checks}


def search_urls(engine: str, query: str) -> str:
    """A search-results URL for the given engine (so the start page is configurable)."""
    q = query.replace(" ", "+")
    if engine == "google":
        return f"https://www.google.com/search?q={q}&hl=en&num=10"
    if engine == "bing":
        return f"https://www.bing.com/search?q={q}&setlang=en"
    if engine == "duckduckgo":
        return f"https://duckduckgo.com/?q={q}&kl=us-en"
    raise KeyError(engine)


TASKS: List[Task] = [
    Task(
        task_id="fact-wikipedia-height",
        goal="Find the height of the Eiffel Tower in metres. Only report a number once you see it in the page text.",
        queries=["Eiffel Tower height metres", "Eiffel Tower"],
        require_any=[["eiffel tower"]],
        note="success = the Eiffel Tower page/result is actually open",
    ),
    Task(
        task_id="wiki-open-article",
        goal="Search for the Wikipedia article about the Python programming language and open it.",
        queries=["Python programming language wikipedia", "Python programming language"],
        require_any=[["python"], ["programming", "programming language"]],
        expect_url_contains="wikipedia.org",
        note="success = URL is a wikipedia.org page about Python",
    ),
    Task(
        task_id="site-specific-docs",
        goal="Find the official Python documentation website and open its main page.",
        queries=["Python official documentation", "site:python.org documentation", "Python docs"],
        require_any=[["python"], ["documentation", "docs"]],
        expect_url_contains="python.org",
        note="success = URL is on python.org",
    ),
    Task(
        task_id="fact-capital",
        goal="Find out which city is the capital of Australia. Open a page that states it.",
        queries=["capital of Australia", "Australia capital city"],
        require_any=[["canberra"]],
        note="success = the text Canberra appears on the final page",
    ),
    Task(
        task_id="nasa-mars",
        goal="Find the official NASA page about Mars and open it.",
        queries=["NASA Mars", "site:nasa.gov Mars"],
        require_any=[["mars"], ["nasa"]],
        expect_url_contains="nasa.gov",
        note="success = URL is on nasa.gov",
    ),
    Task(
        task_id="news-free-not-empty",
        goal="Use Google Search to find who won the FIFA World Cup in 2022, then open a page confirming it.",
        queries=["2022 FIFA World Cup winner", "World Cup 2022 final result"],
        require_any=[["argentina"]],
        note="success = Argentina appears on the final page",
    ),
]


def get(task_id: str) -> Task:
    for t in TASKS:
        if t.task_id == task_id:
            return t
    raise KeyError(task_id)


def text_provider_for(task: Task):
    """Return a text helper bound to a task's allowed literal strings.

    This plays the role of jev-ultrafast's small LLM text helper: it supplies the
    characters to type, chosen from the task's ``queries``. It does not choose the
    operation or the element -- those stay the model's decision. It refuses
    anything that is not an allowed query, so a run cannot cheat by inventing text.
    """
    allowed = [q.lower() for q in task.queries]

    def provider(context: Dict[str, Any]) -> str:
        field = (context.get("field") or {})
        label = (field.get("label") or "").lower()
        page_text = (context.get("page") or {}).get("text", "").lower()
        # pick the query whose tokens best match the field label / goal
        best, best_score = task.queries[0], -1
        for q in task.queries:
            toks = [t for t in q.lower().split() if len(t) > 2]
            score = sum(1 for t in toks if t in label) * 2 + sum(1 for t in toks if t in page_text) * 0.1
            if score > best_score:
                best, best_score = q, score
        return best

    return provider
