# Browser-agent benchmark for Laya

Measures whether a Laya checkpoint makes the **correct next-step decision** in a
browser-automation loop: which operation (`CLICK` / `TYPE_TEXT` / `SELECT` /
`DONE`) and which target element.

Everything is wired to the same `/v1/systemone` request the running agent sends,
so a score here reflects the deployed path, not a lab harness.

---

## What "correct" means (the ground truth)

Two objective sources. No hand-scoring, so a result is reproducible.

### 1. Mind2Web — human-annotated, real websites

[`osunlp/Mind2Web`](https://huggingface.co/datasets/osunlp/Mind2Web) labels, for
each step of 2 000+ real tasks on 137 sites, the gold operation and the gold
element. The converter is a port of the official browser fine-tune's
`convert_mind2web.py`: same element rendering, same gold semantics, so a case's
correct answer is whatever the human annotator clicked.

> **Important caveat.** Mind2Web's **test** split ships as an *encrypted* zip
> (password not public) precisely to stop leaderboard overfitting, so this
> harness can only fetch the **train** shards. Those overlap the official
> checkpoint's training data -- its `run_v10.sh` feeds `m2w_cases.jsonl` into the
> trainer -- so an absolute number on them is an **upper bound**, not a
> generalisation estimate. It is still valid for **relative** comparison (same
> data, different checkpoints) and for catching regressions. `test.zip` failing
> to extract with "password required" is expected, not a bug. See
> [`CONTAMINATION.md`](CONTAMINATION.md) for the full analysis and the
> memorisation probes that show the model decides from the goal rather than
> recalling the page.

```bash
python -m benchmark.download --split train --shards 0     # one shard, ~600 MB
python -m benchmark.run --dataset mind2web --max-cases 250 --base-url http://127.0.0.1:8811
```

### 2. Built-in Chinese scenarios — rule-based oracle

Mind2Web is English-only, so the built-in set covers Chinese. Each case fixes one
page state and one goal; the correct answer follows from jev-ultrafast's own
published rules (`NEXT_ACTION`): *fill required fields before submitting*,
*submit populated search fields before opening a result*, *do not toggle a
control already in the requested state*, and so on. The rationale is recorded on
every case.

> These are **constructed pages, not real tasks**. The oracle is reproducible and
> exercises goal-following plus Chinese handling, but it cannot support a claim
> about real-world accuracy -- treat it as a diagnostic.

```bash
python -m benchmark.run --dataset zh --base-url http://127.0.0.1:8811
```

### 3. Parallel EN/ZH — isolates the language variable

The Chinese-only set cannot tell "bad at browser decisions" from "bad at
Chinese". `parallel` renders the same six scenarios in English and Chinese with
identical structure, identical option count, and the **same correct index**.
Score both and the difference is the language penalty.

```bash
python -m benchmark.run --dataset parallel --base-url http://127.0.0.1:8811
```

---

## Metrics

The first four match the official fine-tune eval (`code/finetune/eval.py`) so the
numbers are comparable to the published ones.

| Metric | Meaning |
|---|---|
| **operation accuracy** | top-1 of the `operation` question |
| **target top-1** | top-1 of the `<op>_target` question, *given the gold operation* — isolates target choice from operation choice, as upstream reports it |
| **mean normalized rank** | where the gold target lands ÷ option count; 0 best, ~0.5 = chance |
| **step accuracy** | operation right **and** target top-1 — the quantity that matters for a running agent |
| **ECE** | expected calibration error of the reported probabilities; Laya's central claim is calibrated confidence, so this is checked, not assumed |
| **per-operation / per-source** | breakdown so a single failing operation or domain is visible |

---

## Usage

```bash
cd inference-server

# start a server (browser fine-tune) and score it over HTTP
./start.sh --browser --device mps &
python -m benchmark.run --dataset mind2web --max-cases 250 \
    --base-url http://127.0.0.1:8811 --out results/v10s-m2w.json

# or load a checkpoint in-process (faster, no server)
python -m benchmark.run --dataset zh --model /path/to/checkpoint --subfolder v10s

# compare official checkpoints through the router
./start.sh --device mps &                        # router mode
python -m benchmark.run --dataset zh --base-url http://127.0.0.1:8000 --model-name multilingual

# inspect the resolved cases without running a model
python -m benchmark.run --dataset zh --dump-cases cases_zh.jsonl
```

### Validate the harness itself

```bash
python -m pytest -q tests/test_benchmark.py       # 6 tests, no model needed
```

These pin the request format's v3 invariants (elements out of `state`, label and
page-text caps), the gold derivation, and the metric math against scripted
oracles — so a wrong harness is caught before it is used to judge a model.

---

## Measured results (Apple M4, MPS)

### Mind2Web train, 250 cases — the real-HTML scale check

> **Contaminated split -- these are upper bounds, not generalisation.** Mind2Web
> train is in the fine-tune's training data. For an honest generalisation figure
> use the author's held-out number (0.761 operation / 0.606 target). See
> [`CONTAMINATION.md`](CONTAMINATION.md).

| Model | op acc | target top-1 | mean norm rank | step acc | op ECE | latency p50 |
|---|---:|---:|---:|---:|---:|---:|
| **browser fine-tune v10s** | **0.892** | **0.588** | **0.215** | **0.532** | 0.070 | 381 ms |
| official `multilingual` | 0.650 | 0.160 | 0.529 | 0.050 | 0.144 | — |
| official `english` | 0.300 | 0.120 | 0.505 | 0.000 | 0.138 | — |

The fine-tune is **~4× better at target selection** (0.588 vs 0.12–0.16) and
**~10× at end-to-end steps** (0.532 vs 0.00–0.05), and it is the only one that is
calibrated (ECE 0.07 vs 0.14). Per operation, v10s: `TYPE_TEXT` top-1 **1.00**,
`SELECT` 0.80, `CLICK` 0.51 — target selection among many near-identical clickables
is where it is weakest, matching the official write-up.

### Built-in Chinese set (10 cases)

| Model | op acc | target top-1 | step acc |
|---|---:|---:|---:|
| browser fine-tune v10s | **0.80** | **0.89** | **0.80** |
| official `multilingual` | 0.20 | 0.56 | 0.00 |
| official `english` | 0.00 | 0.67 | 0.00 |

The official checkpoints are near chance on browser decisions (they were never
trained for them). Note this measures *training*, not *language*.

### Parallel EN/ZH (12 cases, 6 scenarios × 2 languages)

| Model | EN op acc | ZH op acc | EN target | ZH target |
|---|---:|---:|---:|---:|
| browser fine-tune v10s | 0.833 | 0.833 | 0.667 | 0.833 |

At this small size the Chinese rendering is **not** worse — the remaining errors
are semantic near-misses (e.g. "下一页 / Next page" vs "第2页 / Page 2"), in both
languages. Treat the Chinese set as a diagnostic, not a statistical claim; the
250-case Mind2Web run is where the reliable number lives.

---

## Layout

```
benchmark/
├── browser_request.py   # the /v1/systemone request builder (v3 format)
├── mind2web.py          # Mind2Web -> cases converter
├── zh_cases.py          # built-in Chinese scenarios + rule oracle
├── parallel_cases.py    # EN/ZH twins that share a gold index
├── metrics.py           # operation/target/rank/step/ECE
├── run.py               # CLI runner (HTTP or in-process)
├── download.py          # Mind2Web train fetcher
└── data/                # downloaded task files (gitignored)
```

## Extending it

* **More languages** — add rows to `parallel_cases.SPECS` (one entry yields both
  the EN and ZH case).
* **A new domain** — add cases to `zh_cases.cases()` with a `rationale`; the
  oracle just needs the gold operation and element id.
* **A new model** — point `--base-url` at any server speaking `/v1/systemone`;
  nothing in the harness is Laya-specific.
* **Statistical power** — fetch more train shards (`--shards 0 1 2 ...`) and
  raise `--max-cases`.
