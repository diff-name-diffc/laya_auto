# liveweb-benchmark report

- generated: `2026-09-27T14:16:33+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **1/3** (33%) — DONE **and** independently verified
- independently verified **1/3** (33%)
- found-but-never-stopped: **0**
- mean steps 9.3, mean duration 32.0s, decision p50/p95 510.3/627.0 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 3 | 33% | 33% | 9.3 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `google-multi-k8s-docker` | done | ❌ | ❌ | 12 | 68 | missing evidence: [['docker', 'compose']] |
| `google-multi-pytorch-tensorflow` | done | ✅ | ✅ | 7 | 13 |  |
| `google-multi-python-rust` | done | ❌ | ❌ | 9 | 15 | url lacks 'q=rust' |

## Step outcomes

- `executed`: 14 (50%)
- `stale`: 5 (18%)
- `done-rejected`: 4 (14%)
- `done`: 3 (11%)
- `refused-empty-enter`: 2 (7%)

low-confidence decisions (< τ): 5
