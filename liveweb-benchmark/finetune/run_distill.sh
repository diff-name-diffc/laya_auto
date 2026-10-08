#!/bin/bash
# Continue-train cklxx/laya-browser v17s on liveweb distillation data,
# using the official RLCD pipeline (this is exactly how v17s itself was made
# from v15s: a short continuation at low encoder LR).
#
#   bash finetune/run_distill.sh [epochs=1]
#
# Stages are idempotent; env knobs:
#   WORK=finetune/work    clone + uv env location
#   SMOKE=1               time only 64 items through the trainer (contract smoke)
#   DEVICE=mps            torch device patch (author trained on CUDA; we patch)
set -e
ROOT=$(cd "$(dirname "$0")/.." && pwd)
WORK=${WORK:-$ROOT/finetune/work}
EP=${1:-1}
CK=${CK:-laya-browser-v18d}

mkdir -p "$WORK"; cd "$WORK"

# 1) official repo + checkpoint (huggingface-cli pulls the 644MB safetensors)
if [ ! -d laya-browser/code ]; then
  hf download cklxx/laya-browser --local-dir laya-browser || \
  huggingface-cli download cklxx/laya-browser --local-dir laya-browser
fi
cd laya-browser/code
[ -d uv.lock ] || true
uv sync --extra data           # python 3.11-3.12, torch>=2.6, transformers, laya>=0.3.4

# 1b) jev-ultrafast: common_ft.py loads questions.py/model.py from a hardcoded
#     author path; clone the repo and point JEV_HOME at it (patched to env-var)
if [ ! -d "$WORK/jev-ultrafast" ]; then
  git clone --depth 1 https://github.com/browser-use/jev-ultrafast "$WORK/jev-ultrafast"
fi
export JEV_HOME="$WORK/jev-ultrafast/jev_ultrafast"
if ! grep -q 'JEV_HOME' finetune/common_ft.py; then
  python3 -c "p='finetune/common_ft.py'; s=open(p).read(); s=s.replace('JEV = \"/home/ckl/projects/S/jev-ultrafast/jev_ultrafast\"', 'import os as _os; JEV = _os.environ.get(\"JEV_HOME\", \"/home/ckl/projects/S/jev-ultrafast/jev_ultrafast\")'); open(p,'w').write(s)"
fi

# 2) device patch: train.py hardcodes CUDA (RTX 4070 Ti); macOS runs MPS
if ! grep -q 'DEVICE' finetune/train.py; then
  sed -i'.bak' 's|torch.device("cuda")|torch.device(os.environ.get("DEVICE","cuda"))|' finetune/train.py
fi

# 2b) class-balance patch (run3): run2 showed CLICK bleeding 2-3pp while
#     TYPE_TEXT saturated at 1.0 -- rebalance the op-level repeat sampling
if ! grep -q '"CLICK": 2' finetune/build_items.py; then
  sed -i'.bak' 's|{"DONE": 4, "TYPE_TEXT": 3, "SELECT": 3, "PRESS_ENTER": 4, "SCROLL_DOWN": 2}|{"DONE": 4, "TYPE_TEXT": 2, "SELECT": 3, "PRESS_ENTER": 3, "SCROLL_DOWN": 2, "CLICK": 2}|' finetune/build_items.py
fi

# 2c) single-option batch patch (run3): a page with ONE fill element yields a
#     width-1 type_text_target item; a micro-batch of four such items makes
#     kmax=1 and laya's topk(2) crashes. Pad the marker dim to >=2 (padding is
#     already masked to -1e4, so the softmax is unaffected).
if ! grep -q 'kmax = max(2,' finetune/train.py; then
  sed -i'.bak' 's|kmax = max(len(it\["markers"\]) for it in items)|kmax = max(2, max(len(it["markers"]) for it in items))|' finetune/train.py
fi

# 3) our distillation data -> official case schema
mkdir -p out
uv run python "$ROOT/finetune/convert_distill.py" "$ROOT/distill/dataset.jsonl" out/cases_liveweb.jsonl
: > out/pages.jsonl                       # our cases are self-contained (page_obj)

# 4) tokenize into training items (v17s contract: fmt v3, head 768, chunks 40)
#    signature is: build_items.py pages cases out [extra-cases...]
#    optional CLICK anchor: Mind2Web train shard-1 cases (shard 0 stays eval-only)
EXTRA_CASES=""
[ -s out/cases_m2w_click.jsonl ] && EXTRA_CASES="out/cases_m2w_click.jsonl"
LAYA_BASE=$PWD/../v17s LAYA_FMT=v3 LAYA_HEAD=768 MAX_TARGETS=40 FINAL_P=0.2 \
SKIP_SUITE=1 uv run python finetune/build_items.py out/pages.jsonl out/cases_liveweb.jsonl out/ $EXTRA_CASES

# 5) continue-train from v17s (RLCD; resumable via out/$CK/resume.pt)
LIMIT=$([ "${SMOKE:-0}" = "1" ] && echo 64 || echo 0) \
DEVICE=${DEVICE:-mps} LAYA_BASE=$PWD/../v17s LAYA_FMT=v3 LAYA_HEAD=768 CKPT=1 COMPILE=0 \
MICRO=${MICRO:-4} ACCUM=${ACCUM:-8} \
  uv run python finetune/train.py out/train_items.pt out/$CK $EP

if [ "${SMOKE:-0}" = "1" ]; then
  echo "SMOKE OK -- data contract + trainer both run end-to-end"; exit 0
fi

# 6) post-hoc temperature calibration (needs their pages/eval cases; on our
#    live-web eval cases the calibration set can be a held-out slice of the
#    distill data -- placeholder until the first full run)
echo "next: calibrate.py + eval (see finetune/README.md #evaluation)"
