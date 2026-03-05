#!/usr/bin/env python3
"""Sealink OEM console scaffold.

This is a non-breaking scaffold for future console-first workflows.
Current release tooling remains unchanged while this module evolves.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
import time
from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class ConsoleResult:
    ok: bool
    command: str
    message: str
    data: dict[str, Any] | None = None


def _print_result(result: ConsoleResult, as_json: bool) -> int:
    if as_json:
        print(json.dumps(asdict(result), indent=2))
    else:
        status = "OK" if result.ok else "ERROR"
        print(f"[{status}] {result.command}: {result.message}")
    return 0 if result.ok else 1


def _resolve_uart_helper_path() -> str:
    candidate_dirs = [os.path.dirname(os.path.abspath(__file__))]
    pyinstaller_temp_dir = getattr(sys, "_MEIPASS", None)
    if pyinstaller_temp_dir:
        candidate_dirs.insert(0, pyinstaller_temp_dir)

    checked_paths: list[str] = []
    for directory in candidate_dirs:
        direct_candidate = os.path.join(directory, "uart-getRange.py")
        nested_candidate = os.path.join(directory, "product", "resources", "uart-getRange.py")
        dir_wrapped_candidate = os.path.join(directory, "uart-getRange.py", "uart-getRange.py")

        for candidate in (direct_candidate, nested_candidate, dir_wrapped_candidate):
            checked_paths.append(candidate)
            if os.path.isfile(candidate):
                return candidate

    checked_display = "\n".join(checked_paths)
    raise FileNotFoundError(f"Unable to locate uart-getRange.py. Checked:\n{checked_display}")


def _load_uart_helpers() -> tuple[Any, Any, Any, Any]:
    module_path = _resolve_uart_helper_path()
    module_spec = importlib.util.spec_from_file_location("sealink_uart_helpers", module_path)
    if module_spec is None or module_spec.loader is None:
        raise ImportError(f"Unable to create module spec for helper script: {module_path}")

    helper_module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(helper_module)

    return (
        helper_module.serial,
        helper_module.calculate_nmea_checksum,
        helper_module.send_rc_ping,
        helper_module.read_response,
    )


SERIAL, CALCULATE_NMEA_CHECKSUM, SEND_RC_PING, READ_RESPONSE = _load_uart_helpers()


def _open_serial(port: str, baud: int):
    return SERIAL.Serial(
        port=port,
        baudrate=baud,
        parity=SERIAL.PARITY_NONE,
        stopbits=SERIAL.STOPBITS_ONE,
        bytesize=SERIAL.EIGHTBITS,
        timeout=1,
    )


def _read_first_nonempty_line(ser, timeout_sec: float) -> str | None:
    start = time.time()
    while time.time() - start < timeout_sec:
        line = ser.readline().decode("ascii", errors="ignore").strip()
        if line:
            return line
    return None


def cmd_link(args: argparse.Namespace) -> ConsoleResult:
    try:
        with _open_serial(args.port, args.baud) as ser:
            body = "PUWV?,0"
            checksum = CALCULATE_NMEA_CHECKSUM(body)
            ser.write(f"${body}*{checksum}\r\n".encode("ascii"))
            line = _read_first_nonempty_line(ser, args.timeout)

        if not line:
            return ConsoleResult(
                ok=False,
                command="link",
                message="Connected to serial port, but no modem response within timeout.",
                data={"port": args.port, "baud": args.baud, "timeout": args.timeout},
            )

        return ConsoleResult(
            ok=True,
            command="link",
            message="Serial link established and modem responded.",
            data={"port": args.port, "baud": args.baud, "response": line},
        )
    except Exception as exc:
        return ConsoleResult(
            ok=False,
            command="link",
            message=f"Failed to open link: {exc}",
            data={"port": args.port, "baud": args.baud},
        )


def cmd_device_info(args: argparse.Namespace) -> ConsoleResult:
    try:
        with _open_serial(args.port, args.baud) as ser:
            body = "PUWV?,0"
            checksum = CALCULATE_NMEA_CHECKSUM(body)
            full_cmd = f"${body}*{checksum}\r\n"
            ser.write(full_cmd.encode("ascii"))
            line = _read_first_nonempty_line(ser, args.timeout)

        if not line:
            return ConsoleResult(
                ok=False,
                command="device-info",
                message="No response received within timeout.",
                data={"sent": full_cmd.strip(), "timeout": args.timeout},
            )

        return ConsoleResult(
            ok=True,
            command="device-info",
            message="Device information response received.",
            data={"sent": full_cmd.strip(), "response": line},
        )
    except Exception as exc:
        return ConsoleResult(
            ok=False,
            command="device-info",
            message=f"Device info request failed: {exc}",
        )


def cmd_ping(args: argparse.Namespace) -> ConsoleResult:
    try:
        with _open_serial(args.port, args.baud) as ser:
            SEND_RC_PING(ser, tx_ch=args.tx, rx_ch=args.rx)
            time.sleep(0.5)
            tp_sec, distance_m = READ_RESPONSE(
                ser,
                timeout_sec=args.timeout,
                sound_speed=args.sound_speed,
            )

        if tp_sec is None or distance_m is None:
            return ConsoleResult(
                ok=False,
                command="ping",
                message="No RC ping response received within timeout.",
                data={
                    "tx": args.tx,
                    "rx": args.rx,
                    "timeout": args.timeout,
                    "sound_speed": args.sound_speed,
                },
            )

        return ConsoleResult(
            ok=True,
            command="ping",
            message="RC ping response received.",
            data={
                "tx": args.tx,
                "rx": args.rx,
                "propagation_time_sec": tp_sec,
                "slant_range_m": distance_m,
                "sound_speed": args.sound_speed,
            },
        )
    except Exception as exc:
        return ConsoleResult(
            ok=False,
            command="ping",
            message=f"Ping request failed: {exc}",
            data={"tx": args.tx, "rx": args.rx},
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

    output_parent = argparse.ArgumentParser(add_help=False)
    output_parent.add_argument("--json", action="store_true", help="Output JSON")

    connection_parent = argparse.ArgumentParser(add_help=False, parents=[output_parent])
    connection_parent.add_argument("--port", required=True, help="Serial port, for example COM3")
    connection_parent.add_argument("--baud", type=int, default=9600, help="UART baud rate")
    connection_parent.add_argument("--timeout", type=float, default=10.0, help="Response timeout in seconds")

    sub = parser.add_subparsers(dest="command", required=True)

    p_link = sub.add_parser("link", parents=[connection_parent], help="Link/connect to modem")
    p_link.set_defaults(handler=cmd_link)

    p_info = sub.add_parser("device-info", parents=[connection_parent], help="Read device information")
    p_info.set_defaults(handler=cmd_device_info)

    p_ping = sub.add_parser("ping", parents=[connection_parent], help="Run remote ping command")
    p_ping.add_argument("--tx", type=int, default=0, help="Transmit channel")
    p_ping.add_argument("--rx", type=int, default=0, help="Receive channel")
    p_ping.add_argument(
        "--sound-speed",
        type=float,
        default=1500.0,
        help="Sound speed in m/s for range estimation",
    )
    p_ping.set_defaults(handler=cmd_ping)

    p_mon = sub.add_parser("monitor", parents=[output_parent], help="Start monitor mode")
    p_mon.add_argument("--interval", type=float, default=1.0, help="Poll interval seconds")
    p_mon.set_defaults(handler=cmd_monitor)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    result = args.handler(args)
    return _print_result(result, as_json=getattr(args, "json", False))


if __name__ == "__main__":
    raise SystemExit(main())
