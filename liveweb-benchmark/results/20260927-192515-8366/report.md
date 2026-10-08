# liveweb-benchmark report

- generated: `2026-09-27T19:31:25+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **1/8** (12%) — DONE **and** independently verified
- independently verified **1/8** (12%)
- found-but-never-stopped: **0**
- mean steps 5.9, mean duration 16.9s, decision p50/p95 590.1/708.5 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 12% | 12% | 5.9 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-49183aeb45abb216` | bot-challenge | ❌ | ❌ | 6 | 31 | bot_challenge |
| `gen-20dec75efdb570a5` | done | ❌ | ❌ | 5 | 6 | url lacks 'q=quantization' |
| `gen-05304a0ba48723b0` | done | ❌ | ❌ | 9 | 16 | url lacks 'q=testing' |
| `gen-b0c3ae02bbeecbaa` | done | ✅ | ✅ | 19 | 24 |  |
| `gen-3987257774d580f3` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-8f9c5224a2978f5e` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-7693bbc71381bda7` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-c17e96687f2e5542` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 33 (70%)
- `stale`: 6 (13%)
- `done-rejected`: 3 (6%)
- `done`: 3 (6%)
- `refused-empty-enter`: 1 (2%)
- `page changed since the decision (url or marker mismatch)`: 1 (2%)

low-confidence decisions (< τ): 11
