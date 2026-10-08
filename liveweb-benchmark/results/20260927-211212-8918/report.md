# liveweb-benchmark report

- generated: `2026-09-27T21:20:36+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **0/8** (0%) — DONE **and** independently verified
- independently verified **0/8** (0%)
- found-but-never-stopped: **0**
- mean steps 4.2, mean duration 27.8s, decision p50/p95 521.9/708.2 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 1 | 0% | 0% | 15.0 |
| google | 7 | 0% | 0% | 2.7 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-a2aa323944444b25` | done | ❌ | ❌ | 7 | 23 | url lacks 'q=transformers' |
| `gen-318ba691fe525eac` | done | ❌ | ❌ | 15 | 112 | url lacks 'github.com/search' |
| `gen-3aa5ce8897c0a89d` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-4cb288ae7756618b` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-f6ea7efcd3c60c98` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-768d8efeaf61091f` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-e11efdd385f4936b` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-87279657be739c96` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 26 (76%)
- `done-rejected`: 4 (12%)
- `done`: 2 (6%)
- `stale`: 1 (3%)
- `refused-empty-enter`: 1 (3%)

low-confidence decisions (< τ): 0
