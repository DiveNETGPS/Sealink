#!/usr/bin/env python3
"""Sealink OEM console scaffold.

This is a non-breaking scaffold for future console-first workflows.
Current release tooling remains unchanged while this module evolves.
"""

from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import os
import shlex
import sys
import time
from dataclasses import asdict, dataclass
from typing import Any

from serial.tools import list_ports

try:
    import readline
except ImportError:
    readline = None


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


def _append_log_line(log_file: str | None, message: str) -> None:
    if not log_file:
        return
    parent = os.path.dirname(log_file)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(message + "\n")


def _debug_print(args: argparse.Namespace, message: str) -> None:
    if not getattr(args, "debug", False):
        return
    timestamp = dt.datetime.now().isoformat(timespec="seconds")
    line = f"{timestamp} [DEBUG] {message}"
    print(line, file=sys.stderr)
    _append_log_line(getattr(args, "log_file", None), line)


def _log_command_result(args: argparse.Namespace, result: ConsoleResult) -> None:
    log_file = getattr(args, "log_file", None)
    if not log_file:
        return
    payload = {
        "ts": dt.datetime.now().isoformat(timespec="seconds"),
        "command": result.command,
        "ok": result.ok,
        "message": result.message,
        "data": result.data,
    }
    _append_log_line(log_file, json.dumps(payload, ensure_ascii=True))


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
DEFAULT_PROFILE_PATH = os.path.join(os.path.expanduser("~"), ".sealink_console_profile.json")
DEFAULT_HISTORY_PATH = os.path.join(os.path.expanduser("~"), ".sealink_console_history")


def _open_serial(port: str, baud: int):
    return SERIAL.Serial(
        port=port,
        baudrate=baud,
        parity=SERIAL.PARITY_NONE,
        stopbits=SERIAL.STOPBITS_ONE,
        bytesize=SERIAL.EIGHTBITS,
        timeout=1,
    )


def _load_profile(path: str | None) -> dict[str, Any]:
    profile_path = path or DEFAULT_PROFILE_PATH
    if not os.path.isfile(profile_path):
        return {}
    try:
        with open(profile_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _save_profile(path: str | None, profile_data: dict[str, Any]) -> str:
    profile_path = path or DEFAULT_PROFILE_PATH
    parent = os.path.dirname(profile_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(profile_path, "w", encoding="utf-8") as f:
        json.dump(profile_data, f, indent=2)
    return profile_path


def _resolve_port_and_baud(args: argparse.Namespace, profile: dict[str, Any]) -> tuple[str | None, int]:
    port = args.port or profile.get("default_port")
    baud = args.baud if args.baud is not None else int(profile.get("default_baud", 9600))
    return port, baud


def _load_shell_history(path: str) -> None:
    if readline is None:
        return
    try:
        read_history = getattr(readline, "read_history_file", None)
        if os.path.isfile(path) and callable(read_history):
            read_history(path)
    except Exception:
        return


def _save_shell_history(path: str) -> None:
    if readline is None:
        return
    try:
        write_history = getattr(readline, "write_history_file", None)
        if callable(write_history):
            write_history(path)
    except Exception:
        return


def _read_first_nonempty_line(ser, timeout_sec: float) -> str | None:
    start = time.time()
    while time.time() - start < timeout_sec:
        line = ser.readline().decode("ascii", errors="ignore").strip()
        if line:
            return line
    return None


def cmd_link(args: argparse.Namespace) -> ConsoleResult:
    _debug_print(args, "cmd_link invoked")
    profile = _load_profile(args.profile)
    port, baud = _resolve_port_and_baud(args, profile)
    if not port:
        return ConsoleResult(
            ok=False,
            command="link",
            message="No serial port specified. Use --port or set a profile default.",
        )

    try:
        with _open_serial(port, baud) as ser:
            body = "PUWV?,0"
            checksum = CALCULATE_NMEA_CHECKSUM(body)
            ser.write(f"${body}*{checksum}\r\n".encode("ascii"))
            line = _read_first_nonempty_line(ser, args.timeout)

        if not line:
            return ConsoleResult(
                ok=False,
                command="link",
                message="Connected to serial port, but no modem response within timeout.",
                data={"port": port, "baud": baud, "timeout": args.timeout},
            )

        return ConsoleResult(
            ok=True,
            command="link",
            message="Serial link established and modem responded.",
            data={"port": port, "baud": baud, "response": line},
        )
    except Exception as exc:
        return ConsoleResult(
            ok=False,
            command="link",
            message=f"Failed to open link: {exc}",
            data={"port": port, "baud": baud},
        )


def cmd_device_info(args: argparse.Namespace) -> ConsoleResult:
    _debug_print(args, "cmd_device_info invoked")
    profile = _load_profile(args.profile)
    port, baud = _resolve_port_and_baud(args, profile)
    if not port:
        return ConsoleResult(
            ok=False,
            command="device-info",
            message="No serial port specified. Use --port or set a profile default.",
        )

    try:
        with _open_serial(port, baud) as ser:
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
    _debug_print(args, "cmd_ping invoked")
    profile = _load_profile(args.profile)
    port, baud = _resolve_port_and_baud(args, profile)
    if not port:
        return ConsoleResult(
            ok=False,
            command="ping",
            message="No serial port specified. Use --port or set a profile default.",
        )

    tx = args.tx if args.tx is not None else int(profile.get("default_tx", 0))
    rx = args.rx if args.rx is not None else int(profile.get("default_rx", 0))

    try:
        with _open_serial(port, baud) as ser:
            SEND_RC_PING(ser, tx_ch=tx, rx_ch=rx)
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
                    "tx": tx,
                    "rx": rx,
                    "timeout": args.timeout,
                    "sound_speed": args.sound_speed,
                },
            )

        return ConsoleResult(
            ok=True,
            command="ping",
            message="RC ping response received.",
            data={
                "tx": tx,
                "rx": rx,
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
            data={"tx": tx, "rx": rx},
        )


def cmd_list_ports(args: argparse.Namespace) -> ConsoleResult:
    _debug_print(args, "cmd_list_ports invoked")
    ports = []
    try:
        for p in list_ports.comports():
            ports.append(
                {
                    "device": p.device,
                    "description": p.description,
                    "hwid": p.hwid,
                }
            )
        if ports:
            return ConsoleResult(
                ok=True,
                command="list-ports",
                message=f"Found {len(ports)} serial port(s).",
                data={"ports": ports},
            )
        return ConsoleResult(
            ok=True,
            command="list-ports",
            message="No serial ports found.",
            data={"ports": []},
        )
    except Exception as exc:
        return ConsoleResult(
            ok=False,
            command="list-ports",
            message=f"Failed to enumerate serial ports: {exc}",
        )


def cmd_profile_set(args: argparse.Namespace) -> ConsoleResult:
    _debug_print(args, "cmd_profile_set invoked")
    profile = _load_profile(args.profile)

    if args.default_port is not None:
        profile["default_port"] = args.default_port
    if args.default_baud is not None:
        profile["default_baud"] = args.default_baud
    if args.default_tx is not None:
        profile["default_tx"] = args.default_tx
    if args.default_rx is not None:
        profile["default_rx"] = args.default_rx

    saved_path = _save_profile(args.profile, profile)
    return ConsoleResult(
        ok=True,
        command="profile-set",
        message="Profile saved.",
        data={"profile_path": saved_path, "profile": profile},
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


def cmd_shell(args: argparse.Namespace) -> ConsoleResult:
    shell_parser = build_parser()
    history_path = args.history_file or DEFAULT_HISTORY_PATH
    _debug_print(args, f"cmd_shell invoked history={history_path}")
    _load_shell_history(history_path)

    print("Sealink console shell. Type 'help' for usage, 'exit' to quit.")
    while True:
        try:
            line = input(args.prompt)
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print()
            continue

        line = line.strip()
        if not line:
            continue
        if line.lower() in {"exit", "quit"}:
            break
        if line.lower() in {"help", "?"}:
            print("Commands: link, device-info, ping, list-ports, profile-set, monitor")
            print("Use command-specific --help for options, for example: ping --help")
            continue

        try:
            tokens = shlex.split(line)
        except ValueError as exc:
            print(f"[ERROR] shell: {exc}")
            continue

        if not tokens:
            continue
        if tokens[0] == "shell":
            print("[ERROR] shell: nested shell is not supported.")
            continue

        if args.profile and "--profile" not in tokens:
            tokens.extend(["--profile", args.profile])
        if args.json and "--json" not in tokens:
            tokens.append("--json")
        if args.debug and "--debug" not in tokens:
            tokens.append("--debug")
        if args.log_file and "--log-file" not in tokens:
            tokens.extend(["--log-file", args.log_file])

        try:
            nested_args = shell_parser.parse_args(tokens)
        except SystemExit:
            continue

        _execute_args(nested_args)

    _save_shell_history(history_path)
    return ConsoleResult(ok=True, command="shell", message="Shell session ended.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sealink-console",
        description="Sealink OEM Windows console scaffold",
    )

    output_parent = argparse.ArgumentParser(add_help=False)
    output_parent.add_argument("--json", action="store_true", help="Output JSON")
    output_parent.add_argument("--debug", action="store_true", help="Enable debug diagnostics")
    output_parent.add_argument("--log-file", help="Append command logs to file (JSON lines)")
    output_parent.add_argument(
        "--profile",
        help="Profile path (default: ~/.sealink_console_profile.json)",
    )

    connection_parent = argparse.ArgumentParser(add_help=False, parents=[output_parent])
    connection_parent.add_argument("--port", help="Serial port, for example COM3")
    connection_parent.add_argument("--baud", type=int, help="UART baud rate")
    connection_parent.add_argument("--timeout", type=float, default=10.0, help="Response timeout in seconds")

    sub = parser.add_subparsers(dest="command", required=True)

    p_link = sub.add_parser("link", parents=[connection_parent], help="Link/connect to modem")
    p_link.set_defaults(handler=cmd_link)

    p_info = sub.add_parser("device-info", parents=[connection_parent], help="Read device information")
    p_info.set_defaults(handler=cmd_device_info)

    p_ping = sub.add_parser("ping", parents=[connection_parent], help="Run remote ping command")
    p_ping.add_argument("--tx", type=int, help="Transmit channel")
    p_ping.add_argument("--rx", type=int, help="Receive channel")
    p_ping.add_argument(
        "--sound-speed",
        type=float,
        default=1500.0,
        help="Sound speed in m/s for range estimation",
    )
    p_ping.set_defaults(handler=cmd_ping)

    p_ports = sub.add_parser("list-ports", parents=[output_parent], help="List available serial ports")
    p_ports.set_defaults(handler=cmd_list_ports)

    p_profile = sub.add_parser("profile-set", parents=[output_parent], help="Set and save default profile values")
    p_profile.add_argument("--default-port", help="Default serial port, for example COM3")
    p_profile.add_argument("--default-baud", type=int, help="Default baud rate")
    p_profile.add_argument("--default-tx", type=int, help="Default transmit channel")
    p_profile.add_argument("--default-rx", type=int, help="Default receive channel")
    p_profile.set_defaults(handler=cmd_profile_set)

    p_mon = sub.add_parser("monitor", parents=[output_parent], help="Start monitor mode")
    p_mon.add_argument("--interval", type=float, default=1.0, help="Poll interval seconds")
    p_mon.set_defaults(handler=cmd_monitor)

    p_shell = sub.add_parser("shell", parents=[output_parent], help="Start interactive shell mode")
    p_shell.add_argument("--prompt", default="sealink> ", help="Shell prompt text")
    p_shell.add_argument("--history-file", help="History file path")
    p_shell.set_defaults(handler=cmd_shell)

    return parser


def _execute_args(args: argparse.Namespace) -> int:
    result = args.handler(args)
    _log_command_result(args, result)
    return _print_result(result, as_json=getattr(args, "json", False))


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return _execute_args(args)


if __name__ == "__main__":
    raise SystemExit(main())
