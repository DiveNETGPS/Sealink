#!/usr/bin/env python3
"""Sealink OEM console scaffold.

This is a non-breaking scaffold for future console-first workflows.
Current release tooling remains unchanged while this module evolves.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass


@dataclass
class ConsoleResult:
    ok: bool
    command: str
    message: str


def _print_result(result: ConsoleResult, as_json: bool) -> int:
    if as_json:
        print(json.dumps(asdict(result), indent=2))
    else:
        status = "OK" if result.ok else "ERROR"
        print(f"[{status}] {result.command}: {result.message}")
    return 0 if result.ok else 1


def cmd_link(args: argparse.Namespace) -> ConsoleResult:
    return ConsoleResult(
        ok=True,
        command="link",
        message=(
            "Scaffold only. Implement serial link handshake using "
            f"port={args.port} baud={args.baud}."
        ),
    )


def cmd_device_info(args: argparse.Namespace) -> ConsoleResult:
    return ConsoleResult(
        ok=True,
        command="device-info",
        message="Scaffold only. Implement device information query.",
    )


def cmd_ping(args: argparse.Namespace) -> ConsoleResult:
    return ConsoleResult(
        ok=True,
        command="ping",
        message=(
            "Scaffold only. Implement remote ping using "
            f"tx={args.tx} rx={args.rx}."
        ),
    )


def cmd_monitor(args: argparse.Namespace) -> ConsoleResult:
    return ConsoleResult(
        ok=True,
        command="monitor",
        message=(
            "Scaffold only. Implement periodic monitor loop with "
            f"interval={args.interval}s."
        ),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sealink-console",
        description="Sealink OEM Windows console scaffold",
    )

    parser.add_argument("--port", help="Serial port, for example COM3")
    parser.add_argument("--baud", type=int, default=9600, help="UART baud rate")
    parser.add_argument("--json", action="store_true", help="Output JSON")

    sub = parser.add_subparsers(dest="command", required=True)

    p_link = sub.add_parser("link", help="Link/connect to modem")
    p_link.set_defaults(handler=cmd_link)

    p_info = sub.add_parser("device-info", help="Read device information")
    p_info.set_defaults(handler=cmd_device_info)

    p_ping = sub.add_parser("ping", help="Run remote ping command")
    p_ping.add_argument("--tx", type=int, default=0, help="Transmit channel")
    p_ping.add_argument("--rx", type=int, default=0, help="Receive channel")
    p_ping.set_defaults(handler=cmd_ping)

    p_mon = sub.add_parser("monitor", help="Start monitor mode")
    p_mon.add_argument("--interval", type=float, default=1.0, help="Poll interval seconds")
    p_mon.set_defaults(handler=cmd_monitor)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    result = args.handler(args)
    return _print_result(result, as_json=args.json)


if __name__ == "__main__":
    raise SystemExit(main())
