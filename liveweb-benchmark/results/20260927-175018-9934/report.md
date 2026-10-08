# liveweb-benchmark report

- generated: `2026-09-27T17:54:24+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **2/8** (25%) — DONE **and** independently verified
- independently verified **2/8** (25%)
- found-but-never-stopped: **0**
- mean steps 8.0, mean duration 18.1s, decision p50/p95 508.3/754.4 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 2 | 0% | 0% | 10.5 |
| google | 6 | 33% | 33% | 7.2 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-da67c2a253a071ed` | bot-challenge | ❌ | ❌ | 5 | 18 | bot_challenge |
| `gen-b7a39be0e8623108` | done | ✅ | ✅ | 11 | 16 |  |
| `gen-2d8af5aa24f4228a` | done | ❌ | ❌ | 3 | 19 | url lacks 'q=django' |
| `gen-a2b4d81752d843f9` | done | ❌ | ❌ | 8 | 15 | missing evidence: [['fastapi']] |
| `gen-ca6f3932cc0a1280` | done | ❌ | ❌ | 12 | 18 | url lacks 'q=transformers' |
| `gen-948530f74b8bbdb4` | done | ✅ | ✅ | 5 | 9 |  |
| `gen-f367df5c7b1b7f8d` | done | ❌ | ❌ | 13 | 18 | missing evidence: [['concurrency']] |
| `gen-d796fc8d2a2e71d9` | done | ❌ | ❌ | 7 | 33 | url lacks 'google.com/search' |

## Step outcomes

- `executed`: 40 (62%)
- `stale`: 7 (11%)
- `done`: 7 (11%)
- `done-rejected`: 7 (11%)
- `refused-empty-enter`: 2 (3%)
- `page changed since the decision (url or marker mismatch)`: 1 (2%)

low-confidence decisions (< τ): 1
