# liveweb-benchmark report

- generated: `2026-09-27T14:13:58+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **1/6** (17%) — DONE **and** independently verified
- independently verified **1/6** (17%)
- found-but-never-stopped: **0**
- mean steps 14.5, mean duration 28.5s, decision p50/p95 522.1/660.9 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 1 | 0% | 0% | 30.0 |
| google | 5 | 20% | 20% | 11.4 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `google-multi-python-rust` | done | ❌ | ❌ | 14 | 38 | missing evidence: [['rust']] |
| `google-multi-frameworks` | bot-challenge | ❌ | ❌ | 13 | 24 | bot_challenge |
| `google-multi-pytorch-tensorflow` | done | ❌ | ❌ | 6 | 9 | missing evidence: [['tensorflow']] |
| `google-multi-k8s-docker` | done | ❌ | ❌ | 13 | 28 | missing evidence: [['docker', 'compose']] |
| `google-multi-cpp-go` | done | ✅ | ✅ | 11 | 20 |  |
| `github-multi-search` | max-steps | ❌ | ❌ | 30 | 52 | missing evidence: [['rate']] |

## Step outcomes

- `executed`: 58 (67%)
- `done-rejected`: 10 (11%)
- `refused-empty-enter`: 7 (8%)
- `stale`: 5 (6%)
- `done`: 4 (5%)
- `page changed since the decision (url or marker mismatch)`: 3 (3%)

low-confidence decisions (< τ): 14
