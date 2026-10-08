# liveweb-benchmark report

- generated: `2026-09-27T18:47:46+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **1/8** (12%) — DONE **and** independently verified
- independently verified **1/8** (12%)
- found-but-never-stopped: **0**
- mean steps 5.6, mean duration 14.9s, decision p50/p95 569.3/924.5 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 12% | 12% | 5.6 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-0eb232af20f63f58` | bot-challenge | ❌ | ❌ | 6 | 25 | bot_challenge |
| `gen-aed9b28e6c7ab591` | done | ❌ | ❌ | 11 | 20 | url lacks 'google.com/search' |
| `gen-cedac3a1ea4c4e39` | done | ✅ | ✅ | 4 | 10 |  |
| `gen-7175d54d2e7556c1` | done | ❌ | ❌ | 3 | 6 | url lacks 'q=concurrency' |
| `gen-63d74f6ecf10b2c4` | done | ❌ | ❌ | 8 | 14 | missing evidence: [['concurrency']] |
| `gen-96bb5cacd82a69f9` | bot-challenge | ❌ | ❌ | 6 | 24 | bot_challenge |
| `gen-8382328143db0b83` | bot-challenge | ❌ | ❌ | 4 | 16 | bot_challenge |
| `gen-b830322ad20d9ee2` | done | ❌ | ❌ | 3 | 6 | url lacks 'q=debugging' |

## Step outcomes

- `executed`: 23 (51%)
- `done-rejected`: 9 (20%)
- `done`: 5 (11%)
- `stale`: 3 (7%)
- `refused-empty-enter`: 3 (7%)
- `page changed since the decision (url or marker mismatch)`: 2 (4%)

low-confidence decisions (< τ): 7
