"""Live-web task suite: Google AI-news searches + GitHub trending research.

Every task is designed so that **success is not the model's DONE choice**. After
each run, an independent verifier (``verify.py``) inspects the final page's URL,
title and text for evidence that only exists if the task actually happened.

Design constraints for live-web evidence:

* evidence tokens are **daily-stable** (query echoes, structural page markers),
  never date- or rank-dependent (trending #1 changes hourly);
* Google tasks start on the homepage so the agent must find the search box,
  type (text supplied by ``text_model`` from ``queries``), submit, and stop on
  the results page -- the full loop the fine-tune was trained for;
* GitHub tasks use structural repo-page evidence ("star"/"fork"/"readme") since
  repo names cannot be pinned ahead of time;
* one Chinese-goal probe (``google-ai-zh``) measures the multilingual claim.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

GOOGLE_HOME = "https://www.google.com/?hl=en&gl=us"   # pin English UI: kills the
# locale-following "Open 搜索" homepage variant that measurably broke the
# type-then-submit chain (hl is a benign cookie-level preference)
GITHUB_HOME = "https://github.com/"
GITHUB_TRENDING = "https://github.com/trending"


@dataclass
class Task:
    task_id: str
    source: str                      # "google" | "github" -- for by-source reporting
    goal: str
    start_url: str
    queries: List[str] = field(default_factory=list)   # literal strings the text helper may type
    require_any: List[List[str]] = field(default_factory=list)  # any-of groups; every group must hit
    forbid: List[str] = field(default_factory=list)
    expect_url_contains: Optional[str] = None
    expect_url_not_contains: List[str] = field(default_factory=list)
    note: str = ""


TASKS: List[Task] = [
    # --- Google AI-news searches (agent drives the full search flow) ---------
    Task(
        task_id="google-ai-openai",
        source="google",
        goal="Search Google for the latest OpenAI news and open the results.",
        start_url=GOOGLE_HOME,
        queries=["OpenAI latest news"],
        require_any=[["openai"]],
        expect_url_contains="google.com/search",
        note="query echo + results URL prove the search happened",
    ),
    Task(
        task_id="google-ai-anthropic",
        source="google",
        goal="Search Google for recent Anthropic Claude announcements and open the results.",
        start_url=GOOGLE_HOME,
        queries=["Anthropic Claude news"],
        require_any=[["anthropic", "claude"]],
        expect_url_contains="google.com/search",
    ),
    Task(
        task_id="google-ai-deepmind",
        source="google",
        goal="Search Google for Google DeepMind news and open the results.",
        start_url=GOOGLE_HOME,
        queries=["Google DeepMind news"],
        require_any=[["deepmind"]],
        expect_url_contains="google.com/search",
    ),
    Task(
        task_id="google-ai-llm",
        source="google",
        goal="Search Google for the latest large language model news and open the results.",
        start_url=GOOGLE_HOME,
        queries=["large language model news"],
        require_any=[["language model", "llm"]],
        expect_url_contains="google.com/search",
    ),
    Task(
        task_id="google-ai-agents",
        source="google",
        goal="Search Google for AI agent frameworks and open the results.",
        start_url=GOOGLE_HOME,
        queries=["AI agent frameworks"],
        require_any=[["agent"]],
        expect_url_contains="google.com/search",
    ),
    Task(
        task_id="google-ai-papers",
        source="google",
        goal="Search Google for recent AI research papers and open the results.",
        start_url=GOOGLE_HOME,
        queries=["AI research papers arxiv"],
        require_any=[["arxiv", "paper"]],
        expect_url_contains="google.com/search",
    ),
    Task(
        task_id="google-ai-zh",
        source="google",
        goal="在 Google 上搜索最新的中国大模型资讯并查看搜索结果。",
        start_url=GOOGLE_HOME,
        queries=["中国大模型 最新资讯"],
        require_any=[["大模型", "llm"]],
        expect_url_contains="google.com/search",
        note="Chinese-goal probe: measures the multilingual fine-tune claim",
    ),
    Task(
        task_id="google-ai-opensource",
        source="google",
        goal="Search Google for open source AI model releases and open the results.",
        start_url=GOOGLE_HOME,
        queries=["open source AI models release"],
        require_any=[["open source", "开源"]],
        expect_url_contains="google.com/search",
    ),
    # --- GitHub trending / search research ------------------------------------
    Task(
        task_id="github-trending-view",
        source="github",
        goal="Open GitHub's trending page and review today's trending repositories.",
        start_url=GITHUB_TRENDING,
        queries=[],
        require_any=[["trending", "stars today", "built by"]],
        expect_url_contains="github.com/trending",
        note="pure DONE-discipline task: the page starts satisfied; only well-calibrated stopping passes",
    ),
    Task(
        task_id="github-trending-ai-repo",
        source="github",
        goal="From GitHub trending, open a repository about AI, LLMs, or machine learning, and view its README.",
        start_url=GITHUB_TRENDING,
        queries=[],
        require_any=[["star", "stars"], ["fork", "forks"]],
        expect_url_not_contains=["/trending", "/search"],
        note="requires selecting an AI-related repo link out of ~25 candidates",
    ),
    Task(
        task_id="github-search-llm",
        source="github",
        goal="Search GitHub for 'LLM agent' repositories and open the search results.",
        start_url=GITHUB_HOME,
        queries=["LLM agent"],
        require_any=[["llm"]],
        expect_url_contains="github.com/search",
    ),
    Task(
        task_id="github-trending-first-repo",
        source="github",
        goal="Open the first repository in GitHub's trending list and view its details page.",
        start_url=GITHUB_TRENDING,
        queries=[],
        require_any=[["star", "stars"], ["fork", "forks"]],
        expect_url_not_contains=["/trending", "/search"],
        note="first-result selection; structural repo-page evidence",
    ),
    # --- Strength probes informed by the official per-operation breakdown -----
    # (Mind2Web 250: TYPE_TEXT top-1 1.00, SELECT 0.80, CLICK 0.51; ZH == EN.
    # The extra tasks lean on typing flows and low-ambiguity clicks, and probe
    # the known CLICK weakness with high-candidate selection.)
    Task(
        task_id="google-news-tab",
        source="google",
        goal="Search Google for OpenAI news and switch to the News results tab.",
        start_url=GOOGLE_HOME,
        queries=["OpenAI news"],
        require_any=[["openai"]],
        expect_url_contains="tbm=nws",
        note="typing flow + a distinct low-ambiguity tab click",
    ),
    Task(
        task_id="google-images-tab",
        source="google",
        goal="Search Google for 'transformer architecture' and view the Images results.",
        start_url=GOOGLE_HOME,
        queries=["transformer architecture"],
        require_any=[["transformer"]],
        expect_url_contains="tbm=isch",
        note="typing flow + tab navigation",
    ),
    Task(
        task_id="google-page2",
        source="google",
        goal="Search Google for 'large language model' and open the second page of results.",
        start_url=GOOGLE_HOME,
        queries=["large language model"],
        require_any=[["language model", "llm"]],
        expect_url_contains="start=10",
        note="typing flow + pagination click (a zh-cases strong category)",
    ),
    Task(
        task_id="google-wikipedia",
        source="google",
        goal="Search Google for the Wikipedia article on the Python programming language and open it.",
        start_url=GOOGLE_HOME,
        queries=["Python programming language wikipedia"],
        require_any=[["python"], ["programming"]],
        expect_url_contains="wikipedia.org",
        note="classic jev-style search + first-result selection (CLICK-weak probe)",
    ),
    Task(
        task_id="github-trending-python",
        source="github",
        goal="On GitHub trending, show only the Python language repositories.",
        start_url=GITHUB_TRENDING,
        queries=[],
        require_any=[["python"]],
        expect_url_contains="github.com/trending/python",
        note="menu navigation + language filter (SELECT-strong analogue)",
    ),
    Task(
        task_id="github-topic-llm",
        source="github",
        goal="Open GitHub's LLM topic page and review the listed repositories.",
        start_url="https://github.com/topics/llm",
        queries=[],
        require_any=[["llm", "large language model"], ["star", "stars"]],
        expect_url_contains="github.com/topics/llm",
        note="pure DONE-discipline on a satisfied page (calibration probe)",
    ),
    Task(
        task_id="github-open-pytorch",
        source="github",
        goal="Open the PyTorch repository on GitHub and view its page.",
        start_url="https://github.com/pytorch/pytorch",
        queries=[],
        require_any=[["star", "stars"], ["fork", "forks"]],
        expect_url_contains="pytorch/pytorch",
        note="direct-URL DONE-discipline (calibration probe)",
    ),
    Task(
        task_id="github-search-first",
        source="github",
        goal="Search GitHub for 'llm' and open the first repository in the results.",
        start_url=GITHUB_HOME,
        queries=["llm"],
        require_any=[["star", "stars"], ["fork", "forks"]],
        expect_url_not_contains=["/search", "/trending"],
        note="search flow + first-result click (combined weak-weak probe)",
    ),
    # --- IT / coding research suite (diversification: search-research focused) --
    Task(
        task_id="google-it-asyncio",
        source="google",
        goal="Search Google for a Python asyncio tutorial and open the results.",
        start_url=GOOGLE_HOME,
        queries=["python asyncio tutorial"],
        require_any=[["asyncio"]],
        expect_url_contains="google.com/search",
        note="IT search flow (TYPE_TEXT strong category)",
    ),
    Task(
        task_id="google-it-rust-go",
        source="google",
        goal="Search Google for Rust vs Go performance comparisons and open the results.",
        start_url=GOOGLE_HOME,
        queries=["rust vs go performance"],
        require_any=[["rust"]],
        expect_url_contains="google.com/search",
        note="tech-comparison research",
    ),
    Task(
        task_id="google-it-k8s",
        source="google",
        goal="Search Google for Kubernetes deployment best practices and open the results.",
        start_url=GOOGLE_HOME,
        queries=["kubernetes deployment best practices"],
        require_any=[["kubernetes", "k8s"]],
        expect_url_contains="google.com/search",
        note="infra research",
    ),
    Task(
        task_id="google-it-pydantic",
        source="google",
        goal="Search Google for the Pydantic v2 migration guide and open the results.",
        start_url=GOOGLE_HOME,
        queries=["pydantic v2 migration guide"],
        require_any=[["pydantic"]],
        expect_url_contains="google.com/search",
        note="library-migration research",
    ),
    Task(
        task_id="google-it-stackoverflow",
        source="google",
        goal="Search Google for how to debug Python memory leaks on Stack Overflow and open a Stack Overflow question.",
        start_url=GOOGLE_HOME,
        queries=["python memory leak site:stackoverflow.com"],
        require_any=[["memory leak"]],
        expect_url_contains="stackoverflow.com/questions",
        note="multi-hop: search -> open an SO result (third-step probe on an IT topic)",
    ),
    Task(
        task_id="google-it-mdn",
        source="google",
        goal="Search Google for JavaScript Array methods on MDN and open the MDN page.",
        start_url=GOOGLE_HOME,
        queries=["javascript array methods mdn"],
        require_any=[["array"]],
        expect_url_contains="developer.mozilla.org",
        note="multi-hop: search -> open official docs (third-step probe)",
    ),
    Task(
        task_id="google-it-fastapi-docs",
        source="google",
        goal="Search Google for the FastAPI documentation and open the official documentation site.",
        start_url=GOOGLE_HOME,
        queries=["fastapi documentation"],
        require_any=[["fastapi"]],
        expect_url_contains="fastapi.tiangolo.com",
        note="multi-hop: search -> open official docs",
    ),
    Task(
        task_id="github-it-http-server",
        source="github",
        goal="Search GitHub for 'http server' repositories and open the search results.",
        start_url=GITHUB_HOME,
        queries=["http server"],
        require_any=[["http"]],
        expect_url_contains="github.com/search",
        note="IT-topic GitHub search probe",
    ),
    # --- multi-search chains (research flows: query A, then query B) -----------
    # Verification anchors on the FINAL search (the chain's last hop), so the
    # agent must complete A then land B -- premature DONE after the first search
    # fails the url evidence.
    Task(
        task_id="google-multi-python-rust",
        source="google",
        goal="First search Google for the latest stable Python version, then search Google for the latest stable Rust version.",
        start_url=GOOGLE_HOME,
        queries=["latest stable python version", "latest stable rust version"],
        require_any=[["rust"]],
        expect_url_contains="q=rust",
        note="two-hop search chain",
    ),
    Task(
        task_id="google-multi-frameworks",
        source="google",
        goal="First search Google for FastAPI vs Flask performance, then search Google for Django vs Flask comparison.",
        start_url=GOOGLE_HOME,
        queries=["fastapi vs flask performance", "django vs flask comparison"],
        require_any=[["django", "flask"]],
        expect_url_contains="q=django",
        note="two-hop tech-comparison chain",
    ),
    Task(
        task_id="google-multi-pytorch-tensorflow",
        source="google",
        goal="First search Google for PyTorch latest release notes, then search Google for TensorFlow latest release.",
        start_url=GOOGLE_HOME,
        queries=["pytorch latest release notes", "tensorflow latest release"],
        require_any=[["tensorflow"]],
        expect_url_contains="q=tensorflow",
        note="two-hop release-research chain",
    ),
    Task(
        task_id="google-multi-k8s-docker",
        source="google",
        goal="First search Google for Kubernetes ingress tutorial, then search Google for Docker compose networking.",
        start_url=GOOGLE_HOME,
        queries=["kubernetes ingress tutorial", "docker compose networking"],
        require_any=[["docker", "compose"]],
        expect_url_contains="q=docker",
        note="two-hop infra chain",
    ),
    Task(
        task_id="google-multi-cpp-go",
        source="google",
        goal="First search Google for C++ smart pointer tutorial, then search Google for Go garbage collection explained.",
        start_url=GOOGLE_HOME,
        queries=["c++ smart pointer tutorial", "go garbage collection explained"],
        require_any=[["garbage", "go "]],
        expect_url_contains="q=go+garbage",
        note="two-hop languages chain",
    ),
    Task(
        task_id="github-multi-search",
        source="github",
        goal="First search GitHub for 'web crawler' repositories, then search GitHub for 'rate limit' repositories.",
        start_url=GITHUB_HOME,
        queries=["web crawler", "rate limit"],
        require_any=[["rate"]],
        expect_url_contains="q=rate",
        note="two-hop GitHub search chain",
    ),
]


def get(task_id: str) -> Task:
    for t in TASKS:
        if t.task_id == task_id:
            return t
    raise KeyError(task_id)


def by_source(source: str) -> List[Task]:
    return [t for t in TASKS if t.source == source]
