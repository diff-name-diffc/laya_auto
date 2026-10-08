# liveweb-benchmark report

- generated: `2026-09-27T15:30:59+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **5/12** (42%) — DONE **and** independently verified
- independently verified **5/12** (42%)
- found-but-never-stopped: **0**
- mean steps 8.2, mean duration 32.9s, decision p50/p95 496.3/635.5 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 4 | 25% | 25% | 10.2 |
| google | 8 | 50% | 50% | 7.1 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-6b955361397b6b26` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-cf7a3a3e680e9d49` | done | ❌ | ❌ | 10 | 21 | missing evidence: [['svelte']] |
| `gen-f0f7d3752e9ad135` | done | ❌ | ❌ | 8 | 37 | url lacks 'q=ruby' |
| `gen-41d67c2bb76e0db7` | repeat-loop | ❌ | ❌ | 13 | 70 | missing evidence: [['generation', 'retrieval']] |
| `gen-beefa8fa1fa0d2e9` | done | ✅ | ✅ | 11 | 50 |  |
| `gen-30f5dd4880bd6488` | done | ✅ | ✅ | 8 | 18 |  |
| `gen-6850d535c4875e98` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-80c875cb9b34d19b` | repeat-loop | ❌ | ❌ | 10 | 57 | missing evidence: [['langchain']] |
| `gen-7a3624ecaf152b06` | done | ✅ | ✅ | 10 | 34 |  |
| `gen-c095d7cff826fff7` | done | ❌ | ❌ | 9 | 24 | url lacks 'github.com/search' |
| `gen-ca53a58b4f25ccce` | done | ✅ | ✅ | 3 | 7 |  |
| `gen-566ed840e858f93b` | done | ❌ | ❌ | 11 | 59 | url lacks 'github.com/search' |

## Step outcomes

- `executed`: 59 (60%)
- `done-rejected`: 15 (15%)
- `done`: 9 (9%)
- `stale`: 8 (8%)
- `page changed since the decision (url or marker mismatch)`: 4 (4%)
- `refused-empty-enter`: 3 (3%)

low-confidence decisions (< τ): 7
