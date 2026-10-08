# End-to-end browser evaluation

Drives a **real Chrome** through a real search engine, lets the Laya checkpoint
decide every step, and verifies the outcome **independently of the model's DONE
choice**. This is the layer the offline benchmark cannot cover: no fixtures, no
stubbed pages — actual navigation, actual latency, actual failure modes.

```
e2e/
├── observer.py    # page -> element table (the Laya request vocabulary)
├── executor.py    # perform a chosen action, with freshness + visibility guards
├── agent.py       # observe -> decide -> execute loop
├── tasks.py       # Google research tasks + objective verifiers
└── run.py         # CLI
```

## Why this is different from the offline benchmark

| | offline benchmark | this |
|---|---|---|
| pages | Mind2Web snapshots / synthetic | live Google / Bing |
| decision | one step, scored in isolation | full loop to DONE or budget |
| success | argmax vs annotated gold | **an independent check of the final page** |
| failure modes | wrong element | wrong element, no-progress loops, bot walls, context destruction |

## Usage

```bash
# 1. serve the browser fine-tune
./start.sh --browser --device mps &

# 2. run the suite (headed is required -- see the bot-wall note)
python -m e2e.run --base-url http://127.0.0.1:8811 --engine bing --headed

# isolate result selection from the search-box step
python -m e2e.run --base-url http://127.0.0.1:8811 --engine bing --headed --start-at-results

# one task, with screenshots
python -m e2e.run --base-url http://127.0.0.1:8811 --task nasa-mars --headed --shots shots/
```

Flags: `--engine google|bing|duckduckgo`, `--headed`, `--start-at-results`,
`--start-url`, `--max-steps`, `--task <id>` (repeatable), `--shots DIR`,
`--out report.json`.

## Tasks and objective verification

Six Google-research tasks (`tasks.py`). Each carries:

* a natural-language `goal` — the only thing the agent sees;
* `queries` — the literal strings the text helper may type (an offline stand-in
  for jev-ultrafast's small LLM: it supplies characters, it does **not** choose
  the operation or the element);
* a **verifier** that inspects the final URL, title and text and requires
  evidence only present if the research happened — "Canberra" on the page, a
  `wikipedia.org` URL, a `nasa.gov` URL, and so on.

The verifier **first** rejects a bot-challenge page, so a challenge can never be
mistaken for success. `success` requires both that the agent reached DONE *and*
that the verifier passed; `independently_verified` reports the verifier alone
(the agent found the right page, whether or not it stopped).

## Environment constraints found while building this

These are real, reproducible, and worth knowing before trusting any number.

1. **Google serves a bot challenge to automated Chrome.** From this machine every
   automated request to Google is redirected to
   `google.com/sorry/index?continue=...` ("Our systems have detected unusual
   traffic"). Headless is blocked immediately; headed with
   `--disable-blink-features=AutomationControlled` and `navigator.webdriver`
   hidden passed **once** in manual testing, then the IP was rate-limited and
   every subsequent request was challenged. `--engine bing` is the fallback that
   works reliably; the Google tasks remain in the suite and will run once the IP
   is not flagged.

2. **Headless is not viable for search.** Headless Chrome gets an empty results
   page from Bing (94 chars of chrome, no results) and a challenge from Google.
   `--headed` is required for real evaluation.

3. **Clicking navigates away and destroys the JS context.** `page.evaluate` then
   raises "Execution context was destroyed". `observer.observe` retries through
   this rather than failing the run.

## Measured results (M4, MPS, Bing, headed)

### Starting at the engine home page — end-to-end

| | value |
|---|---:|
| tasks | 6 |
| success (reached DONE **and** verified) | **0 / 6** |
| steps per task | 4–16 (mostly hitting the no-progress guard) |

The dominant failure is a **repeated-action loop**: the model types the query
correctly, then clicks Bing's "Copilot" / "Open search box" promotions over and
over instead of the Search button. The homepage's promotional furniture (Copilot
panels, image-of-the-day, news feed) dominates the candidate list, and the
fine-tune was trained on jev-style pages that do not have it.

### Starting at the results page — isolates result selection

| task | agent stopped? | final page verified? |
|---|---|---|
| wiki-open-article | no | — |
| site-specific-docs | DONE at step 2 | **no** (stopped too early) |
| fact-capital | no (max-steps) | **yes** — reached an Australia page |
| nasa-mars | no (no-progress) | **no** |
| news-free-not-empty | no (no-progress) | **yes** — reached a World-Cup page |
| fact-wikipedia-height | no | — |
| **totals** | 0 / 6 success | **3 / 6 independently verified** |

The split is the informative part:

* **Target selection works**: the model correctly picked `nasa.gov` and
  `Australia | History, Cities, Population…` from real results pages, with
  confidence ~0.95.
* **Stopping does not**: on 3 tasks the final page genuinely contained the answer
  (independent verification passed) but the model kept clicking rather than
  choosing DONE. On one task it chose DONE two steps in, before the evidence
  existed.
* **It repeats itself**: clicking a link that navigates away, then re-selecting
  the same label (now a different element), is the single most common pattern.

This matches the offline findings: operation accuracy is high, target top-1 is
the weak point, and the failure is *sequencing/termination*, not reading the
goal.

## What the loop guarantees (and what it does not)

Guaranteed:

* every decision is the model's — the harness never auto-submits a search,
  never picks a target, never hard-codes a click;
* the action space is dynamic and per-page; the model can only choose an element
  that was actually observed;
* freshness and visibility are rechecked immediately before input, so a decision
  made against a stale page is refused rather than executed;
* DONE is never taken as proof — an independent check decides success.

Not guaranteed / known gaps:

* the text helper is an offline stand-in, not a live LLM;
* no captcha solving, so a flagged IP cannot be evaluated;
* the model has no cross-step memory beyond `recent_actions`, which is why it
  repeats actions.
