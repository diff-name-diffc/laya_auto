# liveweb-benchmark report

- generated: `2026-09-28T13:22:50+0800`
- backend: `http://127.0.0.1:8812`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **0/6** (0%) — DONE **and** independently verified
- independently verified **1/6** (17%)
- found-but-never-stopped: **1**
- VLM rescues: **5** (~0.8/task)
- mean steps 4.3, mean duration 21.7s, decision p50/p95 191.5/310.0 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 5 | 0% | 20% | 4.8 |
| google | 1 | 0% | 0% | 2.0 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-3c01a3c70781f9e3` | bot-challenge | ❌ | ❌ | 2 | 14 | bot_challenge |
| `gen-61d1a782b44d10f2` | repeat-loop | ✅ | ❌ | 15 | 95 | SCROLL_DOWN on the same target repeats without progress; sto |
| `gen-022194f32796c77f` | done | ❌ | ❌ | 8 | 15 | missing evidence: [['fork', 'forks']] |
| `gen-662559bde8c3a14d` | incomplete | ❌ | ❌ | 1 | 3 | missing evidence: [['fork', 'forks']] |
| `gen-12fa07c74634bdd7` | incomplete | ❌ | ❌ | 0 | 2 | missing evidence: [['fork', 'forks']] |
| `gen-1fd281eada2e5058` | incomplete | ❌ | ❌ | 0 | 2 | missing evidence: [['fork', 'forks']] |

## Step outcomes

- `executed`: 16 (62%)
- `refused-empty-enter`: 4 (15%)
- `stale`: 2 (8%)
- `page changed since the decision (url or marker mismatch)`: 2 (8%)
- `done-rejected`: 1 (4%)
- `done`: 1 (4%)

low-confidence decisions (< τ): 3
