# liveweb-benchmark report

- generated: `2026-09-27T22:38:39+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **0/8** (0%) — DONE **and** independently verified
- independently verified **0/8** (0%)
- found-but-never-stopped: **0**
- mean steps 9.1, mean duration 25.0s, decision p50/p95 478.7/694.7 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 0% | 0% | 9.1 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-573213fad255eca6` | repeat-loop | ❌ | ❌ | 24 | 42 | missing evidence: [['transformers', 'huggingface']] |
| `gen-fc1ae21099f8057d` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-e6ff85a7977eca6c` | bot-challenge | ❌ | ❌ | 6 | 23 | bot_challenge |
| `gen-4ee234b066d86c10` | max-steps | ❌ | ❌ | 26 | 44 | missing evidence: [['patterns', 'design']] |
| `gen-bdbf75d7073acac9` | bot-challenge | ❌ | ❌ | 5 | 21 | bot_challenge |
| `gen-06f6e100c4b99ef8` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-753ff26510b9da9d` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-86c197b6d351f7b8` | bot-challenge | ❌ | ❌ | 6 | 26 | bot_challenge |

## Step outcomes

- `executed`: 54 (74%)
- `stale`: 9 (12%)
- `done-rejected`: 5 (7%)
- `refused-empty-enter`: 4 (5%)
- `failed`: 1 (1%)

low-confidence decisions (< τ): 4
