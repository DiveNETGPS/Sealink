# Sealink OEM Windows Console Roadmap

This document tracks the plan for evolving the Windows host tooling into a full console-first application while keeping current release builds stable.

## Branching strategy

- Stable release line: `main`
- Console development line: `feature/windows-console-app`
- Keep current Utility/Listener release flow unchanged until console parity is reached.

## External references

Primary references for behavior and workflow:

- `https://github.com/ucnl/uWaveCommander`
- `https://github.com/ucnl/uWaveCommander/blob/main/README.md`
- `https://docs.unavlab.com/underwater_acoustic_modems_en.html#uwave`

Observed patterns to replicate:

- Explicit link/connect workflow with modem identity readback.
- Dedicated operations for local sensor streaming.
- Remote short-command test loop behavior.
- Packet mode style operations and diagnostics.
- Operator-friendly guided usage in addition to scriptable control.

## Target console capabilities

### Phase 1: CLI core and parity baseline

- [ ] Unified executable entrypoint for Windows console usage.
- [ ] Link/connect command (`link`) with port and baud options.
- [ ] Device info command (`device-info`) and structured output.
- [ ] Remote ping command (`ping`) with channel options.
- [ ] Human output and machine-readable JSON output mode.

### Phase 2: Session and workflow ergonomics

- [ ] Interactive shell mode (`shell`) with command history.
- [ ] Persistent profile support (default port/channels/env values).
- [ ] Unified logging (`--log-file`) and verbose diagnostics (`--debug`).
- [ ] Command aliases for common workflows.

### Phase 3: Sensor and monitoring features

- [ ] Live monitor command for periodic local/remote telemetry.
- [ ] Sampling interval and timeout controls.
- [ ] CSV logging mode for field collection.
- [ ] Console-friendly status table view.

### Phase 4: Packet and advanced operations

- [ ] Packet mode command group.
- [ ] Logical-addressed request workflows.
- [ ] Reliability and retry policy options.
- [ ] Scenario scripts for repeatable validation tests.

## Release gate to replace current Utility-first workflow

Before replacing current primary workflow, require:

- [ ] All Utility critical commands have console parity.
- [ ] Internal test checklist passes on Windows 10/11.
- [ ] Updated docs for operator and integrator flows.
- [ ] Signed-off migration note in release notes.

## Near-term implementation order

1. Finish CLI scaffold command contracts.
2. Implement serial transport wrapper and protocol adapter.
3. Implement `link`, `device-info`, and `ping` end-to-end.
4. Add JSON output mode and file logging.
5. Add interactive shell mode.
