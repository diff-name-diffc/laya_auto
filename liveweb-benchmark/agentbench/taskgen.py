"""Batch task generator: fresh search-research tasks, never repeated.

Composes IT/coding search tasks from topic pools x intent templates x
archetypes, and keeps a persistent registry (``distill/used_tasks.json``) of
every task hash ever generated -- two runs can never see the same case, per the
production requirement. The combinatorial space is thousands of tasks, so the
registry practically never binds.

Archetypes (weighted):

* google plain search (40%)  -- type -> submit -> stop on results
* github repository search (15%) -- dialog typing flow
* google two-query chain (25%) -- search A then search B (anchored on B)
* doc-site open (10%) -- search and open a known official docs domain
* github trending browse (10%) -- click a repo entry row off the trending feed

Verification is auto-derived from the query text: the longest distinctive
token becomes the evidence any-of group; chains anchor on ``q=<token>`` of the
second query. Everything the static suite hand-encodes, the generator derives.
"""

from __future__ import annotations

import hashlib
import json
import random
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from .tasks import GITHUB_HOME, GITHUB_TRENDING, GOOGLE_HOME, Task

DEFAULT_USED = Path("distill/used_tasks.json")

POOLS = {
    "languages": ["python", "rust", "golang", "typescript", "kotlin", "swift",
                  "c++", "java", "ruby", "elixir", "zig", "scala"],
    "frameworks": ["fastapi", "django", "flask", "spring boot", "react",
                   "vue", "svelte", "next.js", "laravel", "express", "angular"],
    "infra": ["kubernetes", "docker", "terraform", "nginx", "redis", "kafka",
              "rabbitmq", "prometheus", "grafana", "postgresql", "mysql",
              "mongodb", "elasticsearch"],
    "ai": ["pytorch", "tensorflow", "huggingface transformers", "langchain",
           "vllm", "llama.cpp", "retrieval augmented generation", "llm fine-tuning",
           "vector embeddings", "model quantization"],
    "practices": ["unit testing", "ci/cd pipelines", "code review", "refactoring",
                  "design patterns", "memory leak debugging", "concurrency",
                  "async programming", "logging best practices", "profiling"],
}

# (topic, search query, expected domain) -- the doc-open archetype
DOC_TARGETS = [
    ("python", "python official documentation", "python.org"),
    ("fastapi", "fastapi documentation", "fastapi.tiangolo.com"),
    ("react", "react documentation", "react.dev"),
    ("kubernetes", "kubernetes documentation", "kubernetes.io"),
    ("rust", "rust programming language documentation", "rust-lang.org"),
    ("nodejs", "node.js documentation", "nodejs.org"),
    ("typescript", "typescript documentation", "typescriptlang.org"),
    ("django", "django documentation", "djangoproject.com"),
    ("golang", "go documentation", "go.dev"),
    ("pytorch", "pytorch documentation", "pytorch.org"),
]

_PLAIN_INTENTS = [
    "{t} tutorial",
    "{t} best practices",
    "{t} migration guide",
    "{t} cheat sheet",
    "{t} release notes",
    "how to debug {t}",
    "{t} performance optimization",
    "{t} security vulnerabilities",
    "{t} interview questions",
    "{t} open source alternatives",
]

_STOP = {"best", "practices", "tutorial", "guide", "how", "debug", "notes",
         "cheat", "sheet", "release", "performance", "optimization",
         "security", "vulnerabilities", "interview", "questions", "open",
         "source", "alternatives", "official", "documentation", "migration"}

# trending-language slugs as GitHub spells them in /trending/<slug> URLs
# (golang -> go; c++ excluded -- the URL-encoded form breaks url-contains checks)
_TREND_LANGS = ["python", "rust", "go", "typescript", "kotlin", "swift",
                "java", "ruby", "elixir", "zig", "scala"]

_REPO_TEMPLATES = [
    "From GitHub trending, open a repository related to {t} and view its README.",
    "Open a {t} repository from GitHub trending and check its README.",
    "Browse GitHub trending and open one repository about {t}.",
    "From today's GitHub trending list, open a {t} project and view its details.",
    "Find a {t} repository on GitHub trending and open it to read its README.",
    "Open one {t} project from the GitHub trending feed and view its page.",
]

# any-row-matching goals: every listed entry satisfies them, so the corrective
# signal (click a content row, never the nav) is guaranteed on every run
_ANY_REPO_TEMPLATES = [
    "Open the first repository in today's GitHub trending list and view its details.",
    "Open the top repository on GitHub trending and read its README.",
    "From GitHub trending, open the very first repository shown and view its page.",
    "Open any repository from GitHub trending and view its README.",
    "Pick one repository from GitHub trending and open its details page.",
]

_TREND_ANY_LANG = [
    "Open the first repository in GitHub's trending {lang} section and view its details.",
    "From GitHub's trending {lang} feed, open the top repository and read its README.",
    "Open the first repository shown in GitHub's trending {lang} list.",
    "From GitHub's trending {lang} section, pick the first repository and open its page.",
    "Open the leading repository in GitHub's trending {lang} feed and view its details.",
]


def _topics() -> List[str]:
    return [t for pool in POOLS.values() for t in pool]


def _distinctive_tokens(query: str, limit: int = 2) -> List[str]:
    toks = [t for t in query.lower().replace("+", " ").split()
            if len(t) >= 4 and t not in _STOP]
    toks.sort(key=len, reverse=True)
    return toks[:limit] or [query.split()[0].lower()]


def _goal_key(task: Task) -> str:
    return hashlib.sha1(f"{task.goal}|{task.start_url}".encode()).hexdigest()[:16]


def _load_used(path: Path) -> set:
    if not path.exists():
        return set()
    try:
        return set(json.loads(path.read_text()).get("keys", []))
    except Exception:  # noqa: BLE001 -- corrupt registry -> start fresh
        return set()


def _save_used(path: Path, used: set) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"keys": sorted(used)}))


def _sample_google_plain(rng: random.Random) -> Task:
    query = rng.choice(_PLAIN_INTENTS).format(t=rng.choice(_topics()))
    toks = _distinctive_tokens(query)
    return Task(
        task_id="gen", source="google",
        goal=f"Search Google for {query} and open the results.",
        start_url=GOOGLE_HOME, queries=[query],
        require_any=[toks], expect_url_contains="google.com/search",
        note="generated: plain search",
    )


def _sample_github_search(rng: random.Random) -> Task:
    query = rng.choice(_topics())
    toks = _distinctive_tokens(query)
    return Task(
        task_id="gen", source="github",
        goal=f"Search GitHub for '{query}' repositories and open the search results.",
        start_url=GITHUB_HOME, queries=[query],
        require_any=[toks], expect_url_contains="github.com/search",
        note="generated: github search",
    )


def _sample_chain(rng: random.Random) -> Task:
    topics = rng.sample(_topics(), 2)
    q1 = rng.choice(_PLAIN_INTENTS).format(t=topics[0])
    q2 = rng.choice(_PLAIN_INTENTS).format(t=topics[1])
    anchor = _distinctive_tokens(q2)[0]
    return Task(
        task_id="gen", source="google",
        goal=(f"First search Google for {q1}, then search Google for {q2}."),
        start_url=GOOGLE_HOME, queries=[q1, q2],
        require_any=[_distinctive_tokens(q2)], expect_url_contains=f"q={anchor}",
        note="generated: two-query chain",
    )


def _sample_doc_open(rng: random.Random) -> Task:
    topic, query, domain = rng.choice(DOC_TARGETS)
    return Task(
        task_id="gen", source="google",
        goal=f"Search Google for {query} and open the official site.",
        start_url=GOOGLE_HOME, queries=[query],
        require_any=[[topic]], expect_url_contains=domain,
        note="generated: doc-open",
    )


def _sample_github_trending(rng: random.Random) -> Task:
    """The repo-entry-click skill: pick a content row off the trending feed,
    never the sidebar nav. Sub-shapes diversify page state and goal."""
    shape = rng.random()
    if shape < 0.40:      # open a topic-related repo from the main feed
        topic = rng.choice(_topics())
        goal = rng.choice(_REPO_TEMPLATES).format(t=topic)
        return Task(
            task_id="gen", source="github", goal=goal,
            start_url=GITHUB_TRENDING, queries=[],
            require_any=[["star", "stars"], ["fork", "forks"]],
            expect_url_not_contains=["/trending", "/search"],
            note="generated: trending open-repo",
        )
    if shape < 0.65:      # any-row goal -- the entry-click corrective signal
        lang = rng.choice(_TREND_LANGS)
        if rng.random() < 0.7:   # language feed (varied start page)
            goal = rng.choice(_TREND_ANY_LANG).format(lang=lang)
            start = f"{GITHUB_TRENDING}/{lang}"
        else:
            goal = rng.choice(_ANY_REPO_TEMPLATES)
            start = GITHUB_TRENDING
        return Task(
            task_id="gen", source="github", goal=goal,
            start_url=start, queries=[],
            require_any=[["star", "stars"], ["fork", "forks"]],
            expect_url_not_contains=["/trending", "/search"],
            note="generated: trending any-repo",
        )
    if shape < 0.85:      # topic x language feed: open a repo about {topic}
        topic = rng.choice(_topics())
        lang = rng.choice(_TREND_LANGS)
        return Task(
            task_id="gen", source="github",
            goal=(f"From GitHub's trending {lang} feed, open a repository "
                  f"about {topic} and view its README."),
            start_url=f"{GITHUB_TRENDING}/{lang}", queries=[],
            require_any=[["star", "stars"], ["fork", "forks"]],
            expect_url_not_contains=["/trending", "/search"],
            note="generated: trending open-repo (language feed)",
        )
    # apply the language filter (menu navigation)
    lang = rng.choice(_TREND_LANGS)
    return Task(
        task_id="gen", source="github",
        goal=f"On GitHub trending, show only the {lang} language repositories.",
        start_url=GITHUB_TRENDING, queries=[],
        require_any=[[lang]], expect_url_contains=f"github.com/trending/{lang}",
        note="generated: trending language-filter",
    )


_ARCHETYPES = [
    (_sample_google_plain, 0.40),
    (_sample_github_search, 0.15),
    (_sample_chain, 0.25),
    (_sample_doc_open, 0.10),
    (_sample_github_trending, 0.10),
]

# per-sampler weight overrides for farm waves (--gen-mix). Keys are the
# sampler function names; unspecified samplers keep their _ARCHETYPES weight.
MIX_PRESETS: Dict[str, Dict[str, float]] = {
    "trending": {
        "_sample_google_plain": 0.10,
        "_sample_github_search": 0.05,
        "_sample_chain": 0.05,
        "_sample_doc_open": 0.0,
        "_sample_github_trending": 0.80,
    },
}


def _sample_one(rng: random.Random, weights: Optional[Dict[str, float]] = None) -> Task:
    table = _ARCHETYPES
    if weights:
        merged = {fn.__name__: w for fn, w in _ARCHETYPES}
        merged.update(weights)
        table = [(fn, merged.get(fn.__name__, 0.0)) for fn, _ in _ARCHETYPES]
    pick = rng.random() * sum(w for _, w in table)
    acc = 0.0
    for fn, weight in table:
        acc += weight
        if pick <= acc:
            task = fn(rng)
            key = _goal_key(task)
            return Task(**{**task.__dict__, "task_id": f"gen-{key}"})
    task = _sample_google_plain(rng)
    key = _goal_key(task)
    return Task(**{**task.__dict__, "task_id": f"gen-{key}"})


def generate(n: int, *, seed: Optional[int] = None,
             used_path: Path = DEFAULT_USED,
             mix: Optional[str] = None) -> List[Task]:
    """Generate n NEVER-BEFORE-USED tasks; registers them as used immediately.

    The registry update is file-locked: concurrent runner processes sample
    disjoint tasks even when started simultaneously. ``mix`` names a
    MIX_PRESETS entry to bias the archetype mix (farm waves use "trending").
    """
    import contextlib
    import fcntl

    weights = MIX_PRESETS.get(mix) if mix else None
    rng = random.Random(seed if seed is not None else time.time_ns())
    tasks: List[Task] = []
    used_path.parent.mkdir(parents=True, exist_ok=True)
    with contextlib.closing(open(used_path.with_suffix(".lock"), "w")) as lock_fh:
        fcntl.flock(lock_fh, fcntl.LOCK_EX)
        used = _load_used(used_path)
        tries = 0
        while len(tasks) < n and tries < max(200, n * 80):
            tries += 1
            task = _sample_one(rng, weights)
            if task.task_id in used:      # gen-<hash> encodes goal+start
                continue
            used.add(task.task_id)
            tasks.append(task)
        if tasks:
            _save_used(used_path, used)
    return tasks


def remaining_space(used_path: Path = DEFAULT_USED) -> Dict[str, Any]:
    used = _load_used(used_path)
    return {"used_tasks": len(used), "registry": str(used_path)}


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Fresh search-research task generator")
    ap.add_argument("n", nargs="?", type=int, default=5)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--mix", default=None, choices=list(MIX_PRESETS),
                    help="archetype-mix preset (farm waves use 'trending')")
    ap.add_argument("--dry", action="store_true", help="don't register as used")
    args = ap.parse_args()
    weights = MIX_PRESETS.get(args.mix)
    if args.dry:
        rng = random.Random(args.seed if args.seed is not None else time.time_ns())
        sample = [_sample_one(rng, weights) for _ in range(args.n)]
    else:
        sample = generate(args.n, seed=args.seed, mix=args.mix)
    for t in sample:
        print(f"{t.task_id}  {t.goal}")
    print(json.dumps(remaining_space()))
