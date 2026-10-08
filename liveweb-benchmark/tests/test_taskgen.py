"""run3 additions: the github-trending archetype and the --gen-mix presets."""

from __future__ import annotations

import random

from agentbench import taskgen
from agentbench.taskgen import (
    MIX_PRESETS, _sample_github_trending, _sample_one, _goal_key,
)
from agentbench.verify import verify


def test_trending_sampler_shapes_and_verification_data():
    rng = random.Random(11)
    seen_shapes = set()
    for _ in range(200):
        t = _sample_github_trending(rng)
        assert t.source == "github"
        assert t.start_url.startswith("https://github.com/trending")
        assert t.queries == []
        # the verify() contract: every task must carry usable evidence
        assert t.require_any and all(t.require_any)
        if t.expect_url_contains:
            assert "/trending/" in t.expect_url_contains  # language-filter shape
            seen_shapes.add("lang-filter")
        else:
            assert t.expect_url_not_contains == ["/trending", "/search"]
            assert t.require_any == [["star", "stars"], ["fork", "forks"]]
            seen_shapes.add("open-repo")
    assert seen_shapes == {"lang-filter", "open-repo"}


def test_trending_goals_unique_across_space():
    """The registry keys goal|start_url -- the trending space must be wide."""
    rng = random.Random(3)
    keys = {_goal_key(_sample_github_trending(rng)) for _ in range(400)}
    # 57 topics x 4 templates + 11 langs + 11 first-repo variants > 150
    assert len(keys) >= 150


def test_mix_preset_biases_sampling():
    rng = random.Random(5)
    weights = MIX_PRESETS["trending"]
    sample = [_sample_one(rng, weights) for _ in range(300)]
    trending = [t for t in sample if t.start_url.startswith("https://github.com/trending")]
    assert len(trending) >= 200          # 80% nominal, huge margin over default 10%
    # default mix stays far lower
    rng2 = random.Random(5)
    sample2 = [_sample_one(rng2) for _ in range(300)]
    trending2 = [t for t in sample2 if t.start_url.startswith("https://github.com/trending")]
    assert len(trending2) < 60


def test_generated_trending_task_passes_verifier_on_repo_page():
    """The open-repo shape verifies on any repo page and fails on the feed."""
    rng = random.Random(11)
    for _ in range(50):
        t = _sample_github_trending(rng)
        if t.expect_url_contains:
            continue
        repo_page = {"url": "https://github.com/foo/bar", "title": "foo/bar",
                     "text": "1.2k stars 300 forks README"}
        verdict = verify(t, repo_page)
        assert verdict["passed"], (t.goal, verdict)
        feed_page = {"url": "https://github.com/trending", "title": "Trending",
                     "text": "stars today built by"}
        assert not verify(t, feed_page)["passed"]


def test_mix_preset_weights_sum_to_one():
    for name, weights in MIX_PRESETS.items():
        defaults = {fn.__name__: w for fn, w in taskgen._ARCHETYPES}
        defaults.update(weights)
        assert 0.99 <= sum(defaults.values()) <= 1.01, name
