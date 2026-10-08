"""liveweb-benchmark: a self-contained live-web e2e benchmark.

Implements the AGENT_INTEGRATION_PROMPT.md design (five validation layers,
DOM-main-path observer, guarded decision loop, independent verifier) against a
remote ``POST /v1/systemone`` Laya decision service, driving a CloakBrowser
(free pinned build) instead of vanilla Playwright.
"""
