#!/usr/bin/env python3
"""Deterministic loopback-only UDP forwarding/capture training fixture.

Two local UDP hops: source -> simulated relay -> local collector.
All sockets bind 127.0.0.1 on automatically assigned ephemeral ports.
No network device, Parser Studio server, or Stellar Cyber runtime is contacted.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import socket
import tempfile

HERE = Path(__file__).resolve().parent
PREFIXES = (
    "<134>Oct 31 11:30:00 relay01 forwarder: ",
    "<134>Oct 31 11:31:05 relay01 forwarder: ",
)


def main() -> None:
    source = (HERE / "05-relay-original.log").read_text(encoding="utf-8").splitlines()
    assert len(source) == len(PREFIXES) == 2, "training fixture mismatch"
    received = []

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as producer,          socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as relay,          socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as collector:
        relay.bind(("127.0.0.1", 0))
        collector.bind(("127.0.0.1", 0))
        relay.settimeout(3)
        collector.settimeout(3)
        for index, raw in enumerate(source):
            # Simulate the product sending its original unwrapped event.
            producer.sendto(raw.encode("utf-8"), relay.getsockname())
            payload, _ = relay.recvfrom(65535)
            # Simulated relay adds its *own* RFC3164 Syslog envelope.
            wrapped = PREFIXES[index].encode("ascii") + payload
            relay.sendto(wrapped, collector.getsockname())
            captured, _ = collector.recvfrom(65535)
            assert captured == wrapped, "UDP capture bytes changed"
            received.append(captured.decode("utf-8"))

    output = ("\n".join(received) + "\n").encode("utf-8")
    expected = (HERE / "05-relay-forwarded.log").read_bytes()
    assert output == expected, "relay result does not match the downloadable fixture"
    target = Path(tempfile.gettempdir()) / "parser-studio-relay-captured.log"
    target.write_bytes(output)
    digest = hashlib.sha256(output).hexdigest()
    print(f"PASS: 2/2 source events forwarded and captured over 127.0.0.1 UDP")
    print(f"Captured: {target} ({len(output)} bytes; SHA-256 {digest})")
    print("Paste the captured file into Parser Studio as post-relay source records.")


if __name__ == "__main__":
    main()
