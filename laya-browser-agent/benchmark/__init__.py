"""Browser-agent benchmark for Laya decision correctness.

Ground truth comes from two objective sources:

1. **Mind2Web** (``osunlp/Mind2Web``) -- human-annotated operation + target
   element for real websites. This is the same corpus the official browser
   fine-tune (`cklxx/laya-browser`) trained on, so evaluate on the *test* split
   to stay honest.
2. **A built-in Chinese scenario set** with a rule-based oracle derived from
   jev-ultrafast's own published next-action rules, so the "correct" answer is
   reproducible rather than subjectively labelled.

Metrics mirror the official fine-tune eval (``code/finetune/eval.py``):
operation accuracy, target top-1 given the gold operation, mean normalized
rank, plus expected calibration error over the answers' probabilities.
"""

from .browser_request import (
    build_request,
    action_space,
    NEXT_ACTION,
    TARGET,
)

__all__ = ["build_request", "action_space", "NEXT_ACTION", "TARGET"]
