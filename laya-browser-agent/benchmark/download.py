"""Download Mind2Web task files into ``benchmark/data``.

Mind2Web is public (CC-BY-4.0) for its **train** split. Its **test** split ships
as an encrypted zip to prevent leaderboard overfitting -- the password is not
public (see benchmark/README.md). So this fetches the train shards, which is what
the benchmark uses for a reproducible, real-HTML scale check.

    python -m benchmark.download --split train          # downloads all 10 shards (~6 GB)
    python -m benchmark.download --split train --shards 0   # just train_0.json (~600 MB)
"""

from __future__ import annotations

import argparse
import json
import urllib.request
from pathlib import Path

BASE = "https://huggingface.co/datasets/osunlp/Mind2Web/resolve/main"


def _get(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"downloading {url}\n     -> {dest}", flush=True)
    with urllib.request.urlopen(url, timeout=300) as resp, open(dest, "wb") as f:
        total = 0
        while True:
            chunk = resp.read(1 << 20)
            if not chunk:
                break
            f.write(chunk)
            total += len(chunk)
            if total % (100 << 20) < (1 << 20):
                print(f"     {total / 1e6:.0f} MB", flush=True)
    print(f"     done, {total / 1e6:.1f} MB", flush=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=["train"], default="train",
                    help="Mind2Web's test split is encrypted and cannot be fetched here")
    ap.add_argument("--shards", nargs="*", type=int, default=list(range(10)),
                    help="which train shards to fetch (default: all 0..9)")
    ap.add_argument("--data-dir", default="benchmark/data")
    args = ap.parse_args()

    root = Path(args.data_dir) / "train"
    root.mkdir(parents=True, exist_ok=True)
    for i in args.shards:
        dest = root / f"train_{i}.json"
        if dest.exists() and dest.stat().st_size > 100_000_000:
            print(f"have {dest.name}", flush=True)
            continue
        _get(f"{BASE}/data/train/train_{i}.json", dest)

    files = sorted(root.glob("*.json"))
    if files:
        tasks = json.loads(files[0].read_text())
        print(f"OK: {files[0].name} has {len(tasks)} tasks; "
              f"first: {tasks[0].get('confirmed_task', '?')[:70]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
