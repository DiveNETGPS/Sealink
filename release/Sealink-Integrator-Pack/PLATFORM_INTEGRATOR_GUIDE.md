# Sealink OEM Integrator Platform Guide

## Recommended release model (2 versions)

One-command build for both distributables:
- `make_all_releases.bat`

### Version A: Operator Package (Windows, non-technical users)
Send `release/Sealink-OEM`.

This is the turnkey package with `.exe` binaries and `.bat` launchers for normal day-to-day use.

When to resend this package to testers:
- Resend only for intentional candidate builds that change app/runtime behavior.
- Do not resend for GitHub sync only, documentation updates, or other non-runtime changes.
- Keep the previously published Operator Package as the active testing baseline until a new candidate is announced.

### Version B: Integrator Package (technical users)
Send `release/Sealink-Integrator-Pack` (or its zip) created by:
- `build_integrator_pack.bat`
- `make_integrator_zip.bat`

This package covers Linux/Raspberry Pi and Arduino workflows in a single technical bundle.

## Integrator targets included

### Raspberry Pi / Linux
Files:
- `resources/uart-getRange.py`
- `resources/requirements.txt`
- `integrations/raspberry-pi/run_sealink_cli.sh`

Quick start on Pi:
```bash
cd integrations/raspberry-pi
chmod +x run_sealink_cli.sh
./run_sealink_cli.sh --port /dev/ttyUSB0 --test ping --tx 0 --rx 0
```

Notes:
- UART protocol is `9600 8N1`.
- For onboard UART (GPIO), port is commonly `/dev/serial0`.
- CLI is preferred for headless/system integration.

### Arduino / MCU
File:
- `integrations/arduino/SealinkOEM_Basic.ino`

What it does:
- Builds proper `$PUWV...*hh` checksum sentences.
- Sends device info request (`PUWV?,0`) and remote ping (`PUWV2,tx,rx,0`).
- Parses `PUWV3` propagation time and prints approximate range.

Hardware requirements:
- 3.3V UART logic compatible with Sealink-OEM.
- Board with a hardware UART connected to modem (example sketch uses `Serial1`).

## macOS policy
macOS is not packaged by default.

If requested by a partner, provide source-based CLI instructions (same pattern as Linux) instead of maintaining a separate turnkey macOS release.
