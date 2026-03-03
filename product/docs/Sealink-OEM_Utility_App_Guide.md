# DiveNET: Sealink-OEM Utility App Guide

This guide covers packaged Windows usage and local repository launch workflows for the Sealink-OEM Utility app.

## 1. Scope

The Utility app is intended for:

- Initial product familiarization
- Basic command execution and response verification
- Essential functionality/performance checks

## 2. Packaged Windows Workflow

Operator package location:

- `release/Sealink-OEM`

Main files:

- `SealinkUtility.exe` (main app)
- `SealinkListener.exe` (test/demo listener)
- `run_utility.bat` (start utility only)
- `run_listener.bat` (start listener only)
- `run_all.bat` (start listener + utility)

Typical use:

1. Connect hardware and identify COM port.
2. Start `run_utility.bat`.
3. Enter serial port, channels, and environmental parameters in the app.
4. Select command (`ping`, `device-info`, or `remote-depth`) and run.

## 3. Local Repository Workflow (Python)

From repository root:

- Start utility: `launch_utility.bat`
- Start listener only: `launch_listener.bat`
- Start both windows: `start_all.bat`
- Quiet start: `start_all_quiet.bat`

Underlying script:

- `product/resources/sealink_utility.py`

## 4. Utility Inputs

Required/typical fields:

- Serial port (for example `COM3`)
- TX channel
- RX channel
- Depth (m)
- Temperature (°C)
- Salinity (PSU)
- Command selection

The app computes sound speed from environmental values and reports propagation time and slant range from responses.

## 5. Relationship to CLI/Test Script

The Utility app wraps the same command logic used by:

- `product/resources/uart-getRange.py`

Use the script directly when CLI automation is preferred.

## 6. Troubleshooting

- Port open error: verify COM port and close other serial tools.
- No response: verify wiring, transducer connection, channel match, and acoustic path.
- Unstable results: collect multiple pings and average under stable conditions.

For protocol-level details, see [Sealink-OEM Communication Protocol](Sealink-OEM_Communication_Protocol.md).
