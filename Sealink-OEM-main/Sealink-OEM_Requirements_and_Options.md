# Sealink-OEM – Requirements and Options

This document summarizes the **mandatory requirements** for operating the Sealink-OEM modem and the **optional/configurable elements** available to adapt it to different applications.

## Mandatory Requirements

### Power Supply
- Voltage: +12 V DC nominal  
- Range: 12 V minimum – 14 V maximum (±0.3 V tolerance)  
- Connector: XP2 (Molex 43045-0212)  
  - Pin 1: GND  
  - Pin 2: +12 V  
- **Caution**: Exceeding 14.3 V or dropping below 12 V may damage the board or cause unreliable operation.

### Communication Interface
- UART: 9600 baud, 8 data bits, no parity, 1 stop bit (8N1)  
- Logic level: 0–3.3 V (do not exceed 3.3 V on data lines)  
- Connector: XP5 (Molex 53253-0470)  
  - Pin 1: TxD  
  - Pin 2: RxD  
  - Pin 3: SVC/CMD (strobe output in firmware ≥1.2.0)  
  - Pin 4: GND  
- **Caution**: Applying >5.3 V to UART lines will cause automatic shutdown or permanent damage.

### Acoustic Transducer
- Must be connected to XP1 (Molex 105309-1102)  
- Use only the transducer supplied with the device or a compatible model (SW-T100, SW-T200, SW-T300)  
- **Caution**: Using a non-compatible antenna/transducer will result in damage to the board.

### Operating Environment
- The modem is designed for underwater/submerged use.  
- Dry-land testing is supported only for basic functional verification (transducers within ~6 inches).  
- **Note**: Dry-land operation does not guarantee payload data integrity.

### Testing App / Release Validation Policy
- The packaged Windows testing app for non-technical users is the Operator Package (`release/Sealink-OEM`).
- GitHub synchronization and documentation-only updates do **not** require issuing a new test app build.
- Issue a new test app build only when executable behavior changes (for example, runtime scripts, GUI/listener logic, protocol handling, or packaged launch flow).
- Keep one designated “published test baseline” release for team testing until a new candidate build is intentionally created.

### Firmware
- Minimum version: ≥1.2.0 (command mode always enabled, SVC/CMD repurposed as strobe output)

## Optional / Configurable Elements

### Transducer Selection
Choose based on range vs. depth trade-off:

| Model     | Max Acoustic Range (slant) | Max Operational Depth | Notes                              |
|-----------|----------------------------|------------------------|------------------------------------|
| SW-T100   | ~1,000 m                   | 600 m                  | Best for moderate range / deeper ops |
| SW-T200   | ~3,000 m                   | 300 m                  | Balanced range / depth             |
| SW-T300   | ~3,000 m                   | 1,000 m                | Maximum range + maximum depth      |

### Expansion Modules
- **XP6 – Pressure Sensor**  
  - Designed specifically for KELLER 4LD series (I²C)  
  - Pinout: +3.3 V, SDA, SCL, GND  
  - **Caution**: Connecting any other device is prohibited and may cause permanent failure.

- **XP7 – GNSS Module**  
  - +3.3 V, 1PPS, TxD, RxD, GND  
  - For optional position/time synchronization

- **XP8 – RF Module**  
  - +5 V, ENABLE, TxD, RxD, GND, SET  
  - For optional surface RF gateway/relay

### LED Indicators
- Connected via XP3/XP4 (LED +, LED -)  
- Can be used for status visualization (power, Tx/Rx activity, etc.)

### Sound Speed for Ranging
- Default in examples/scripts: 1500 m/s  
- Recommended to adjust for actual conditions (temperature, salinity, depth).  
- See [Basic Ranging Guide](docs/Sealink-OEM_Basic_Ranging_Guide.md) for reference table.

### Protocol & Addressing
- Up to 255 logical addresses (0–254 usable)  
- Up to 20 code channels  
- Configurable via $PUWV1 sentences (address, channel, baud rate, etc.)

---

**Questions or integration support?**  
Contact DiveNET: support@divenetgps.com

Last updated: March 2026
