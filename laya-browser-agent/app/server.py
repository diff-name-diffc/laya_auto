"""Entrypoint: build the runtime, then serve over HTTP.

    python -m app.server            # honours INFER_* / LAYA_* env vars
    ./start.sh                      # the convenience wrapper at the repo root

Loading the model *before* binding the socket means a broken checkpoint fails
fast and loudly, instead of the port being open while every request 503s.
"""

from __future__ import annotations

import socket
import sys

from .config import settings
from .protocol import create_app
from .runtime import InferenceRuntime


def _lan_addresses() -> list[str]:
    """Best-effort list of this host's LAN IPv4 addresses.

    The UDP-connect trick alone picks the *default route* interface, which on a
    Mac with a VPN is often a utun tunnel (e.g. 198.18.0.0/15) rather than the
    Wi-Fi/Ethernet address a phone on the same LAN would use. So enumerate every
    interface and rank by how likely it is to be reachable on a local network.
    """
    candidates: set[str] = set()

    # Prefer psutil (all interfaces, excludes loopback) when present.
    try:
        import psutil  # type: ignore

        for name, addrs in psutil.net_if_addrs().items():
            if name in ("lo0", "lo"):
                continue
            for a in addrs:
                if a.family == socket.AF_INET and a.address and not a.address.startswith("127."):
                    candidates.add(a.address)
    except Exception:  # noqa: BLE001
        candidates.update(_lan_addresses_from_ifconfig())

    # The default-route address, as a last resort.
    if not candidates:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.connect(("8.8.8.8", 80))
                candidates.add(s.getsockname()[0])
            finally:
                s.close()
        except OSError:
            pass

    def rank(ip: str) -> tuple:
        # Real private LAN ranges first; CGNAT/VPN ranges last.
        if ip.startswith("192.168.") or ip.startswith("10."):
            return (0, ip)
        if ip.startswith("172.") and 16 <= int(ip.split(".")[1]) <= 31:
            return (0, ip)
        if ip.startswith("198.18.") or ip.startswith("198.19.") or ip.startswith("100."):
            return (2, ip)  # CGNAT/VPN, rarely reachable from a phone
        return (1, ip)

    return sorted(candidates, key=rank)


def _lan_addresses_from_ifconfig() -> list[str]:
    """Parse ``ifconfig`` for IPv4 addresses (macOS/Linux fallback, no psutil)."""
    import re
    import subprocess

    out: list[str] = []
    try:
        text = subprocess.run(
            ["ifconfig"], capture_output=True, text=True, timeout=5
        ).stdout
    except Exception:  # noqa: BLE001
        return out
    for match in re.finditer(r"\binet (?:addr:)?(\d+\.\d+\.\d+\.\d+)", text):
        ip = match.group(1)
        if not ip.startswith("127."):
            out.append(ip)
    return out


def main() -> int:
    import uvicorn

    runtime = InferenceRuntime(settings)
    try:
        runtime.load_sync()
    except Exception as exc:  # noqa: BLE001
        print(f"[inference-server] failed to load backend {settings.backend!r}: {exc}",
              file=sys.stderr)
        return 1

    app = create_app(runtime, settings)
    info = runtime.info()
    print(f"[inference-server] backend={info.get('backend')} "
          f"device={info.get('device')} mode={info.get('mode')} "
          f"pool={info.get('pool_size')} models={runtime.models()}", flush=True)
    if settings.host == "0.0.0.0":
        for ip in _lan_addresses():
            print(f"[inference-server] LAN: http://{ip}:{settings.port}/v1/systemone", flush=True)
    print(f"[inference-server] local: http://127.0.0.1:{settings.port}/v1/systemone", flush=True)
    if not settings.api_key and settings.host not in ("127.0.0.1", "localhost"):
        print("[inference-server] warning: listening on the LAN with no API key set "
              "(set INFER_API_KEY to require a bearer token)", file=sys.stderr, flush=True)

    try:
        uvicorn.run(
            app,
            host=settings.host,
            port=settings.port,
            log_level=settings.log_level,
            backlog=settings.backlog,
            timeout_keep_alive=settings.timeout_keep_alive,
            limit_concurrency=settings.limit_concurrency,
        )
    finally:
        runtime.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
