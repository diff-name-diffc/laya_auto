# local-inference-server

A local, LAN-reachable HTTP backend for on-device model inference. It speaks the
**TypeSafe Jev `POST /v1/systemone`** decision protocol, so a browser agent or a
Jev SDK points its base URL here and works unchanged. Laya is the first backend;
the HTTP layer is model-agnostic, so further local models plug in as new
backends without touching the protocol.

```
inference-server/
├── start.sh                 # convenience launcher (venv bootstrap, LAN bind)
├── pyproject.toml
├── app/
│   ├── config.py            # env-driven settings + request caps
│   ├── server.py            # entrypoint: build runtime, serve, print LAN URLs
│   ├── protocol.py          # Jev-compatible FastAPI routes (the contract)
│   ├── runtime.py           # backend pool + worker threads
│   └── backends/
│       ├── base.py          # Backend contract + registry  ← extension point
│       └── laya_backend.py  # Laya (router mode | single-agent mode)
├── benchmark/               # browser-decision correctness benchmark
│   └── README.md            # datasets, metrics, measured results
└── tests/                   # protocol tests (no model) + real-model e2e
```

---

## Quick start

```bash
cd inference-server
./start.sh                       # LAN, port 8000, official Laya router mode
```

The script creates `.venv`, installs the server (and the Laya extra on first
run — this pulls PyTorch), then binds `0.0.0.0`. On startup it prints the URLs:

```
[inference-server] backend=laya device=mps mode=router pool=1 models=['english','multilingual','typed-decisions']
[inference-server] LAN: http://192.168.31.188:8000/v1/systemone
[inference-server] local: http://127.0.0.1:8000/v1/systemone
```

Interactive API docs are served at `/docs` (OpenAPI at `/openapi.json`).

### Common flags

| Flag | Effect |
|---|---|
| `--port 8791` | listen on another port |
| `--key secret` | require `Authorization: Bearer secret` |
| `--local` / `--lan` | bind loopback only / all interfaces |
| `--device mps` | pin the torch device (`cpu`, `mps`, `cuda`) |
| `--model <repo\|path>` | serve one checkpoint (switches to agent mode) |
| `--subfolder v10s` | which variant folder inside a multi-checkpoint repo |
| `--browser` | shortcut: serve the `cklxx/laya-browser` fine-tune (`v10s`) |
| `--pool 2` | N independent model instances (real parallelism on a multi-core CPU) |
| `--threads 8` | cap torch intra-op threads |
| `--no-preload` | load checkpoint(s) lazily on first request |
| `--recreate` | rebuild the virtualenv |

You can also skip the script and drive it entirely by environment:

```bash
INFER_PORT=8791 LAYA_DEVICE=mps python -m app.server
```

---

## Serving a custom / fine-tuned checkpoint

The official router only knows the three bundled checkpoints. To serve a
**fine-tune** (e.g. the browser-agent head) use agent mode with a local path or
a Hub repo, and the correct `subfolder`:

```bash
./start.sh --model /path/to/laya-browser --subfolder v10s --device mps
# or straight from the Hub:
./start.sh --browser
```

Agent mode also applies the checkpoint's trained head budget automatically
(`head_max_len = head_max_len_train`), which a browser fine-tune needs so every
candidate element stays distinct.

---

## API

### `POST /v1/systemone`

Answer typed questions about a state, in one forward pass.

**Request**

```json
{
  "model":   "optional string",     // honoured if the backend serves it; else auto-selected
  "state":   "any JSON",            // string, object, or list of messages
  "questions": {
    "<id>": {
      "type": "choice" | "score" | "noul",
      "instructions": "what to decide",
      "criteria": { "key": "description" }   // choice: map; score: list; noul: omit
    }
  }
}
```

* **`choice`** — pick one of `criteria` (a `{key: description}` map).
* **`score`** — an ordinal position over `criteria` (a list).
* **`noul`** — a yes/no question; returns the probability of "yes".

**Response** — `answers` is Laya's native, Jev-compatible shape:

```json
{
  "model": "laya-rl-agent",
  "answers": {
    "department": {
      "type": "choice",
      "choice": "billing",
      "probabilities": { "billing": 0.94, "technical": 0.04, "other": 0.02 },
      "confidence": 0.7589,
      "answer_confidence": 0.9603,
      "action": { "act_probability": 1.0 }
    },
    "churn": { "type": "noul", "noul": 0.9471, "confidence": 0.9471, "answer_confidence": 0.9471,
               "action": { "act_probability": 1.0 } },
    "urgency": { "type": "score", "score": 0.938,
                 "legend": { "0": "low", "1": "high" },
                 "probabilities": { "0": 0.062, "1": 0.938 },
                 "confidence": 0.6646, "answer_confidence": 0.938,
                 "action": { "act_probability": 1.0 } }
  },
  "usage": { "input_tokens": 121, "output_tokens": 0 },
  "routing": { "model": "english", "repo": "convaiinnovations/laya", "reason": "..." }
}
```

> With the stock checkpoints, `confidence` (task-model confidence) and
> `answer_confidence` (probability of the chosen answer) both appear. Upstream
> warns `action.act_probability` carries no usable signal yet — gate on
> `confidence`.

### `GET /health`

```json
{ "status": "ok", "loaded": true, "backend": "laya",
  "device": "mps", "mode": "router", "pool_size": 1,
  "models": ["english", "multilingual", "typed-decisions"] }
```

### `GET /v1/models`

```json
{ "object": "list", "data": [ { "id": "english", "object": "model", "owned_by": "laya" } ] }
```

### Status codes

| Code | Meaning |
|---|---|
| `200` | answered |
| `400` | malformed JSON, non-object body, or missing `questions` |
| `401` | invalid/missing bearer token (only when an API key is configured) |
| `413` | body > 2 MiB, > 64 questions, or state > 50 000 chars |
| `422` | model-side question validation error (the message names the question) |
| `500` | inference failed (no internal detail is leaked) |
| `503` | backend not available |

---

## Calling it

### curl

```bash
curl -s http://127.0.0.1:8000/v1/systemone \
  -H 'Content-Type: application/json' \
  -d '{
    "state": {"body": "We were billed twice in March. Refund the duplicate today or we cancel."},
    "questions": {
      "department": {"type": "choice", "instructions": "Which department should handle this?",
                     "criteria": {"billing": "invoices, payments, refunds",
                                  "technical": "bugs, outages", "other": "everything else"}},
      "churn": {"type": "noul", "instructions": "Does the user threaten to cancel?"}
    }
  }' | python3 -m json.tool
```

### Python

```python
import httpx

resp = httpx.post("http://127.0.0.1:8000/v1/systemone", json={
    "state": {"body": "Refund my duplicate charge."},
    "questions": {
        "department": {"type": "choice", "instructions": "Which department?",
                       "criteria": {"billing": "payments", "technical": "bugs"}},
        "churn": {"type": "noul", "instructions": "Cancel threat?"},
    },
}, timeout=120)
resp.raise_for_status()
answers = resp.json()["answers"]
print(answers["department"]["choice"], answers["department"]["confidence"])
print(answers["churn"]["noul"])
```

### Browser agent (jev-ultrafast)

The wire format is Jev's, so an existing Jev client only changes its base URL:

```bash
export TYPESAFE_BASE_URL=http://192.168.31.188:8000     # your Mac's LAN IP
export TYPESAFE_API_KEY=local-placeholder               # any value when no --key is set
uv run jev
```

### From another machine on the LAN

```bash
curl http://192.168.31.188:8000/health
```

The startup log lists the LAN address(es). Private `192.168.*` / `10.*` ranges
are listed first; VPN/CGNAT addresses (`198.18.*`, `100.*`) last.

---

## Performance notes (Apple M4)

Measured in this repo's earlier evaluation, serving the browser fine-tune on MPS:

| Path | Latency |
|---|---|
| Single-question short decision (MLX approach, for reference) | ~17 ms |
| Browser step, 3 question heads, 45 candidates (`laya-browser/v10s`, PyTorch-MPS) | ~350 ms forward, ~530 ms HTTP round trip |

Tuning knobs:

* **`--pool N`** — one model instance per slot. The default `1` is a serialised
  single-flight executor (one forward pass at a time), matching upstream
  `laya-serve`. Raise it on a multi-core CPU where per-request cost is CPU-bound.
* **`--threads N`** — cap torch intra-op threads; keep ≤ physical cores.
* **`--device mps`** — the Metal GPU. Laya auto-selects `cuda > mps > cpu`.
* **`--no-preload`** — start instantly, load on first request (first call is slow).

Inference always runs in worker threads, never on the event loop, so `/health`
stays responsive while a request is in flight.

---

## Benchmark

A decision-correctness benchmark for browser automation lives in
[`benchmark/`](benchmark/README.md): operation accuracy, target top-1, mean
normalized rank, end-to-end step accuracy, and calibration (ECE), scored against
Mind2Web's human annotations plus built-in Chinese scenarios with a rule-based
oracle.

```bash
python -m benchmark.download --split train --shards 0     # ~600 MB
python -m benchmark.run --dataset mind2web --max-cases 250 --base-url http://127.0.0.1:8811
python -m benchmark.run --dataset zh --base-url http://127.0.0.1:8811
```

On 250 real Mind2Web steps the browser fine-tune scores **0.892 operation
accuracy / 0.588 target top-1 / 0.532 step accuracy**, against 0.65 / 0.16 / 0.05
for the official multilingual checkpoint. Details and caveats in the
[benchmark README](benchmark/README.md).

## Adding another model

1. Subclass `Backend` in `app/backends/`, implement `load()`, `predict()`,
   `models()`, and call `register("mymodel", MyBackend)`.
2. Return a `DecisionResult` whose `payload` is `{model, answers, usage}`.
3. Start with `INFER_BACKEND=mymodel`.

The protocol, limits, auth, and runtime pool are reused unchanged. See
`app/backends/laya_backend.py` for a worked example and
`app/backends/base.py` for the contract.

---

## Tests

```bash
cd inference-server
.venv/bin/python -m pytest -q                              # protocol tests, no model
LAYA_E2E_MODEL=/path/to/checkpoint \
  .venv/bin/python -m pytest -q tests/test_e2e_laya.py      # real-model e2e
```

The protocol suite (13 tests) covers every status code, answer shape, the auth
path, and the non-ASCII-header hardening. The e2e suite loads a real checkpoint
and **skips** automatically when none is available.

---

## Security

* Binds `0.0.0.0` by default. Set `--key` (or `INFER_API_KEY`) to require a bearer
  token; the server warns at startup when it is LAN-exposed with no key.
* Request caps: 2 MiB body, 64 questions, 50 000-char state — enforced by
  streaming, so a client that omits `Content-Length` is still bounded.
* `500` responses never carry internal detail (paths, weights, OOM text).

## Env vars

| Var | Default | Meaning |
|---|---|---|
| `INFER_HOST` / `INFER_PORT` | `0.0.0.0` / `8000` | bind address / port |
| `INFER_API_KEY` | (none) | require `Authorization: Bearer <it>` |
| `INFER_BACKEND` | `laya` | which backend to serve |
| `INFER_WORKERS` | `1` | reserved |
| `INFER_LOG_LEVEL` | `info` | uvicorn log level |
| `LAYA_MODE` | `router` | `router` (official, auto-language) or `agent` (one checkpoint) |
| `LAYA_MODEL` | `convaiinnovations/laya` | checkpoint repo id or local path |
| `LAYA_SUBFOLDER` | (none) | variant folder inside the repo (e.g. `v10s`) |
| `LAYA_DEVICE` | (auto) | `cpu` / `mps` / `cuda` |
| `LAYA_PRELOAD` | `1` | preload at startup vs. lazy |
| `LAYA_MODELS` | (all) | comma list to preload in router mode |
| `LAYA_POOL` | `1` | independent model instances |
| `LAYA_THREADS` | (torch) | cap torch intra-op threads |
| `LAYA_AUTO_TASK` | `0` | auto-route to the typed-decisions checkpoint |
