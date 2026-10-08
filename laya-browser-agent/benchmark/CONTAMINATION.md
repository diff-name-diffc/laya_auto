# Overfitting / contamination analysis

Question: are the benchmark numbers real, and could they be inflated by
memorisation? Short answer: **the Mind2Web split used here is contaminated, so
its numbers are an upper bound -- but the model demonstrably decides from the
goal rather than recalling a page.** Both halves are shown below.

## 1. The contamination is real and confirmed

The official browser fine-tune (`cklxx/laya-browser`) trains on **Mind2Web train**:

* `code/finetune/run_v10.sh` passes `m2w_cases.jsonl` into `build_items.py`.
* Its model card lists training data as *"Mind2Web train (7.3k steps) plus 5.1k
  steps re-labelled..."*.

`benchmark/run.py --dataset mind2web` reads the **train shards** (the only public
ones -- the test split ships as an encrypted zip, see `benchmark/README.md`).
So cases overlap the training set, and the reported 0.892 / 0.588 / 0.532 are an
**upper bound, not a generalisation estimate.** The official checkpoint's own
honest held-out figure (*"Held-out decisions (6,268: live pages, Mind2Web unseen
websites, NNetNav): operation 0.761 / target top-1 0.606"*) is the number to quote
for generalisation, and it is lower than what a train-split run shows.

What the train-split run **is** still good for: comparing checkpoints on identical
data, and catching regressions. Not for claiming real-world accuracy.

## 2. But the model reasons from the goal -- three probes

If the high score came from recall ("this page -> click element 17"), it would
break when the goal is changed but the page is not. It does not.

### Probe A -- goal swap (`probe_memorisation.py`)

Same page, goal rewritten to name a *different* element (40 real Mind2Web cases):

| Outcome | rate |
|---|---:|
| picked the newly named element (follows the goal) | **0.65** |
| kept the original annotated gold (memorised) | **0.07** |
| other / no clear element | 0.28 |

### Probe B -- label swap (`probe_label_swap.py`)

Swap the *labels* of the gold element and a distractor, leaving every index and
role untouched. A memoriser keeps the old index; a reasoner follows the label to
its new index (40 cases; 30 restricted to meaningful text labels):

| Outcome | all 40 | meaningful labels |
|---|---:|---:|
| followed the label to its new index | 0.30 | 0.33 |
| **kept the original index (memorisation)** | **0.03** | **0.00** |
| other | 0.68 | 0.67 |

The decisive cell is "kept the original index": **0.00-0.03**. The model is not
keying on element position.

### Probe C -- impossible goal

Goal names an element that is not on the page. A memoriser still returns the
original gold; a reasoner stops.

| Model | still picked original gold | moved elsewhere |
|---|---:|---:|
| browser fine-tune v10s | **0.20** | 0.80 |
| official multilingual | 0.00 | 1.00 |

The fine-tune's gold-picking drops from ~0.59 (normal goal) to **0.20** when the
goal is impossible -- it is reading the goal. (The official baseline's 0.00 is
uninformative here: it never picked the gold even with a valid goal.)

## 3. What each dataset actually is

| Dataset | Real or synthetic | Clean of training? | Use it for |
|---|---|---|---|
| Mind2Web **train** (this repo's default) | real sites, human-annotated | **no** -- in the fine-tune's training data | checkpoint comparison, regression |
| Mind2Web **test** | real sites, human-annotated | yes | gold standard -- but **encrypted**, not public |
| Official **Suite B** (18 unseen sites) | real sites | yes (author-checked against a domain list) | the author's own held-out claim: 100% (54/54) |
| Official **held-out decisions** (6,268) | real + synthetic | yes | the author's generalisation claim: 0.761 / 0.606 |
| `zh` / `parallel` (this repo) | **synthetic pages I authored**, rule-based oracle | n/a (not real tasks) | Chinese coverage and EN/ZH comparison as a *diagnostic*, not a real-world score |

So: the `zh`/`parallel` sets are **not real tasks** -- they are constructed pages
with a rule-derived answer key. They exercise goal-following and Chinese handling
and are reproducible, but they cannot support an accuracy claim about real
websites. Only the Mind2Web-based runs are on real tasks, and those are the
contaminated ones.

## 4. Recommendations

* Treat **0.588 target top-1 / 0.532 step accuracy** as an upper bound.
* For a generalisation figure, quote the author's held-out **0.761 / 0.606**.
* To measure this checkpoint honestly on unseen sites: obtain the Mind2Web test
  password (via the official repo) and point `--data-dir` at the extracted
  `test_task.json`, or collect fresh pages with `--dump-cases` + a real browser.
* The probes are the standing defence against a future checkpoint that *does*
  memorise: run them alongside any accuracy run.
