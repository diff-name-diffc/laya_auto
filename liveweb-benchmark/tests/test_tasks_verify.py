"""Task-suite well-formedness + independent-verifier behaviour (spec §6)."""

from agentbench.tasks import TASKS, get
from agentbench.verify import verify


class TestSuiteShape:
    def test_ids_unique(self):
        ids = [t.task_id for t in TASKS]
        assert len(ids) == len(set(ids))

    def test_sources_and_counts(self):
        assert len([t for t in TASKS if t.source == "google"]) == 24
        assert len([t for t in TASKS if t.source == "github"]) == 10

    def test_typing_tasks_have_queries(self):
        # any task whose flow requires typing must supply literal queries
        for t in TASKS:
            if "search" in t.goal.lower() and t.start_url.rstrip("/").endswith((".com", ".com/")):
                pass  # start pages; typing inferred per-task below
        for tid in ("google-ai-openai", "github-search-llm"):
            assert get(tid).queries, f"{tid} must supply queries for the text helper"

    def test_every_task_has_evidence(self):
        for t in TASKS:
            assert t.require_any, f"{t.task_id} has no verification evidence"
            for group in t.require_any:
                assert group, f"{t.task_id} has an empty evidence group"
            assert t.goal and t.start_url.startswith("https://")


def _page(url, text, title=""):
    return {"url": url, "title": title, "text": text}


GOOD_RESULTS = _page("https://www.google.com/search?q=openai+latest+news",
                     "OpenAI latest news - all the announcements", "openai - Google Search")
BOT_WALL = _page("https://www.google.com/sorry/index",
                 "Our systems have detected unusual traffic from your computer")
TRENDING = _page("https://github.com/trending",
                 "Trending repositories today · 1,234 stars today · built by the community")
REPO = _page("https://github.com/owner/llm-toolkit",
             "llm-toolkit · 3.2k stars · 210 forks · README an LLM utility toolkit")
GITHUB_HOME = _page("https://github.com/", "Where the world builds software")


class TestVerifier:
    def test_google_task_passes_on_real_results(self):
        v = verify(get("google-ai-openai"), GOOD_RESULTS)
        assert v["passed"], v

    def test_google_task_fails_on_homepage_done_early(self):
        v = verify(get("google-ai-openai"), GITHUB_HOME)
        assert not v["passed"]

    def test_bot_wall_fails_every_task(self):
        for t in TASKS:
            v = verify(t, BOT_WALL)
            assert not v["passed"] and v["reason"] == "bot_challenge", t.task_id

    def test_trending_view_passes_on_trending(self):
        assert verify(get("github-trending-view"), TRENDING)["passed"]

    def test_trending_view_fails_on_repo_page(self):
        v = verify(get("github-trending-view"), REPO)
        assert not v["passed"]  # url no longer contains /trending

    def test_ai_repo_task_requires_repo_url(self):
        assert verify(get("github-trending-ai-repo"), REPO)["passed"]
        # all evidence present but still on /trending -> the URL check must fail it
        on_trending = _page("https://github.com/trending",
                            "Trending · repo-with-stars-and-forks stars forks readme")
        v = verify(get("github-trending-ai-repo"), on_trending)
        assert not v["passed"] and "trending" in v["reason"]
        # trending text without repo evidence -> evidence check fails it
        v2 = verify(get("github-trending-ai-repo"), TRENDING)
        assert not v2["passed"] and "missing evidence" in v2["reason"]

    def test_github_search_requires_search_url(self):
        ok = verify(get("github-search-llm"),
                    _page("https://github.com/search?q=llm+agent&type=repositories",
                          "llm agent repositories"))
        assert ok["passed"]
        bad = verify(get("github-search-llm"), REPO)
        assert not bad["passed"]  # never left the repo page / wrong url

    def test_wikipedia_task_evidence(self):
        wiki = _page("https://en.wikipedia.org/wiki/Python_(programming_language)",
                     "Python is a high-level programming language", "Python - Wikipedia")
        assert verify(get("google-wikipedia"), wiki)["passed"]
        assert not verify(get("google-wikipedia"), GOOD_RESULTS)["passed"]  # still on google

    def test_missing_evidence_reason_names_the_group(self):
        v = verify(get("google-ai-openai"),
                   _page("https://www.google.com/search?q=cats", "cat videos"))
        assert not v["passed"] and "missing evidence" in v["reason"]


class TestTaskGen:
    def test_generated_tasks_are_fresh_and_valid(self, tmp_path):
        from agentbench import taskgen
        reg = tmp_path / "used.json"
        a = taskgen.generate(5, seed=1, used_path=reg)
        b = taskgen.generate(5, seed=1, used_path=reg)   # same seed, registry blocks reuse
        assert len(a) == 5 and len(b) == 5
        assert not ({t.task_id for t in a} & {t.task_id for t in b})
        for t in a + b:
            assert t.goal and t.start_url.startswith("https://")
            assert t.queries and t.require_any and t.require_any[0]
            assert t.expect_url_contains
        goals = {t.goal for t in a + b}
        assert len(goals) == 10     # all distinct tasks

    def test_generator_space_is_large(self, tmp_path):
        from agentbench import taskgen
        reg = tmp_path / "used.json"
        batch = taskgen.generate(40, used_path=reg)
        assert len(batch) == 40
        assert len({t.task_id for t in batch}) == 40
