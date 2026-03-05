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

- [x] Unified executable entrypoint for Windows console usage.
- [x] Link/connect command (`link`) with port and baud options.
- [x] Device info command (`device-info`) and structured output.
- [x] Remote ping command (`ping`) with channel options.
- [x] Human output and machine-readable JSON output mode.

### Phase 2: Session and workflow ergonomics

- [x] Interactive shell mode (`shell`) with command history.
- [x] Persistent profile support (default port/channels/env values).
- [x] Unified logging (`--log-file`) and verbose diagnostics (`--debug`).
- [x] Command aliases for common workflows.

### Phase 3: Sensor and monitoring features

- [x] Live monitor command for periodic local/remote telemetry.
- [x] Sampling interval and timeout controls.
- [x] CSV logging mode for field collection.
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

1. Refine console-friendly status table view and formatting presets.
2. Start packet-mode command group design.
3. Add a concise operator command reference page for shell usage.
4. Add monitor presets for common field test workflows.
5. Add response formatting presets for operator vs automation output.
