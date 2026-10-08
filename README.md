# laya_auto

Evaluating and improving the **Laya 322M "System 1" browser-decision model**
(`cklxx/laya-browser`, a fine-tune of `convaiinnovations/laya` — mmBERT-base
322M, one bidirectional forward pass answers typed `choice` / `score` / `noul`
questions with calibrated probabilities) as the decision head of a real
live-web agent.

Everything here is measured on real websites, not synthetic pages: the model
observes a page's interactive elements, and must pick the operation
(`CLICK` / `TYPE_TEXT` / `SELECT` / `PRESS_ENTER` / `SCROLL` / `DONE`) and its
target element at each step.

## Layout

| path | what it is |
|---|---|
| **`liveweb-benchmark/`** | The main work: an independent live-web end-to-end benchmark plus a distillation flywheel (VLM rescue → training data → RLCD fine-tune → re-evaluate). See its [README](liveweb-benchmark/README.md). |
| **`laya-browser-agent/`** | Reference harness and integration spec (`AGENT_INTEGRATION_PROMPT.md`): the `/v1/systemone` protocol, the Mind2Web / Chinese / parallel decision benchmarks, and the local inference server. |
| **`docs/`** | A recorded `/v1/systemone` request example. |

## The flywheel (in `liveweb-benchmark/`)

1. **Run** real tasks (Google IT/coding search-research + GitHub) against the
   decision model over `/v1/systemone`.
2. **Rescue**: when the fast model stalls (rejected DONE, repeat loop,
   no-progress), a System-2 VLM picks the corrective action on that exact
   observation.
3. **Distill**: every rescue and every step of a verified-successful run becomes
   a fine-tuning case (`distill/dataset.jsonl`, failure-primary policy).
4. **Fine-tune**: continue-train the official checkpoint with the upstream RLCD
   recipe (noisy-logit policy gradient + soft CE), plus temperature calibration.
5. **Measure**: static regression (Mind2Web), pure-model A/B on hard tasks, and
   the full 34-task cascade.

### Measured so far (Apple M4, MPS)

Continue-training `v17s` on this project's live-web distillation data:

| checkpoint | Mind2Web op / CLICK op / step | 34-task cascade | pure-model A/B |
|---|---|---|---|
| `v17s` (upstream baseline) | 0.812 / 0.796 / 0.500 | 12/20 (shared-20) | 0/6 |
| `v18d-run2` | 0.796 / 0.771 / 0.480 | 8/20 (shared-20) | 1/6 |
| **`v18d-run3`** | **0.888 / 0.920 / 0.520** | **17/34 · 11/20** | 0/6 |

`run3` is the best composite checkpoint: CLICK-anchor data plus operation
rebalancing fixed the run2 CLICK regression and beat the upstream baseline on
static selection. The one unsolved failure is the GitHub-trending "click a
sidebar nav item instead of a repo entry" shortcut (see the run3 notes in
`liveweb-benchmark/README.md`).

> Upstream note: the author has since published **v19s** (input format v5, adds
> the WebChain real-site trajectories); this project's checkpoints are on the
> v3 format and are **not** directly comparable. Not yet migrated.

## Quickstart

```bash
# the benchmark itself
cd liveweb-benchmark && python -m venv .venv && .venv/bin/pip install -e .
.venv/bin/python -m pytest -q                    # 101 tests, no browser/network needed
.venv/bin/python -m agentbench.runner --list-tasks

# the reference decision benchmarks
cd ../laya-browser-agent
python -m benchmark.download --split train --shards 0     # Mind2Web (not committed; 600 MB)
python -m benchmark.run --dataset mind2web --max-cases 250 --base-url http://127.0.0.1:8811
```

## Not in the repository

Model weights (~614 MB per checkpoint), the Mind2Web raw shards (587/599 MB, over
GitHub's per-file limit — fetch with `benchmark.download`), and the fine-tune
working area (cloned upstream repo + uv env) are gitignored. Our own
distillation dataset and the experiment reports **are** committed.
