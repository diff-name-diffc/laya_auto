# liveweb-benchmark report

- generated: `2026-09-27T20:44:42+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **0/8** (0%) — DONE **and** independently verified
- independently verified **0/8** (0%)
- found-but-never-stopped: **0**
- mean steps 4.6, mean duration 22.4s, decision p50/p95 501.3/631.0 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 0% | 0% | 4.6 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-74d4d37db829bff1` | done | ❌ | ❌ | 7 | 17 | missing evidence: [['rust']] |
| `gen-fb25826eebae4a98` | done | ❌ | ❌ | 10 | 57 | missing evidence: [['django']] |
| `gen-350354c9f5bf2aa6` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-2ad2352b802dd091` | bot-challenge | ❌ | ❌ | 6 | 23 | bot_challenge |
| `gen-8dbcae60dd6a845d` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-4a3afd58076af32c` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-a5cecce11862ef4e` | bot-challenge | ❌ | ❌ | 6 | 24 | bot_challenge |
| `gen-5e64acf8671af038` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 21 (57%)
- `done-rejected`: 8 (22%)
- `refused-empty-enter`: 3 (8%)
- `stale`: 2 (5%)
- `done`: 2 (5%)
- `page changed since the decision (url or marker mismatch)`: 1 (3%)

low-confidence decisions (< τ): 2
