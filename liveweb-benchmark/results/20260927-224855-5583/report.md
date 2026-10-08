# liveweb-benchmark report

- generated: `2026-09-27T22:53:19+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **5/8** (62%) — DONE **and** independently verified
- independently verified **5/8** (62%)
- found-but-never-stopped: **0**
- mean steps 7.0, mean duration 14.8s, decision p50/p95 583.6/630.1 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 62% | 62% | 7.0 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-61390215608d5c14` | done | ✅ | ✅ | 12 | 26 |  |
| `gen-6843b499798ae06b` | done | ✅ | ✅ | 3 | 5 |  |
| `gen-cc3495846f74b5e9` | done | ✅ | ✅ | 11 | 18 |  |
| `gen-bf6162e23a2a2793` | done | ✅ | ✅ | 3 | 5 |  |
| `gen-17aafc296b373c28` | bot-challenge | ❌ | ❌ | 5 | 20 | missing evidence: [['generation', 'retrieval']] |
| `gen-1ada4e005ba13f07` | unstable-page | ❌ | ❌ | 6 | 4 | missing evidence: [['embeddings', 'vector']] |
| `gen-5c6206f3ed272b6b` | bot-challenge | ❌ | ❌ | 4 | 17 | missing evidence: [['refactoring']] |
| `gen-b560375388739ca5` | done | ✅ | ✅ | 12 | 25 |  |

## Step outcomes

- `executed`: 38 (68%)
- `stale`: 8 (14%)
- `done`: 5 (9%)
- `page changed since the decision (url or marker mismatch)`: 3 (5%)
- `done-rejected`: 2 (4%)

low-confidence decisions (< τ): 6
