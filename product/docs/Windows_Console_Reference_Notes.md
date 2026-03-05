# Windows Console Reference Notes

This note captures implementation signals from the reference app and related docs.

## uWaveCommander reference cues

Source:

- `https://github.com/ucnl/uWaveCommander`
- `https://github.com/ucnl/uWaveCommander/blob/main/README.md`

Key interaction cues to map into console workflows:

- Connect/link step that validates physical connection and command mode readiness.
- Immediate visibility of modem identity and firmware metadata after link.
- Separate operational areas for:
  - local sensor updates,
  - short remote command tests,
  - packet mode operations.
- Fast test actions that can be repeated automatically.

## uWave docs portal cues

Source:

- `https://docs.unavlab.com/underwater_acoustic_modems_en.html#uwave`

Useful alignment points:

- Host app and protocol documentation are published together.
- Wiring and protocol references are first-class onboarding links.
- "demo host application" pattern suggests scripted and interactive flows should both exist.

## Console design implications for Sealink

- Provide both one-shot commands and an interactive shell mode.
- Keep command names task-oriented (`link`, `device-info`, `ping`, `monitor`).
- Return concise operator text by default and JSON for automation.
- Make diagnostics explicit (timeouts, parse errors, serial state).
- Keep profiles for repeated field setups (port/channels/environment).
