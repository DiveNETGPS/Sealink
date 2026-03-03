# DiveNET: Sealink-OEM - Basic Ranging Guide (UART)

This guide explains how to perform basic range (distance) measurements using the Sealink-OEM acoustic modem over a serial (UART) interface. The system uses two-way travel time (propagation time) to calculate distance between two units.

## Key Principle

The Sealink-OEM measures the acoustic propagation time from a ping request to the response.  
The reported `propTime` is the **one-way** propagation time in seconds (from initiator to responder).

Distance is calculated as:

`range (m) = propTime (seconds) × sound_speed (m/s)`

- No further division is needed — the modem already computes the one-way time internally.
- Default sound speed used in examples: 1500 m/s (typical for seawater at ~20°C, moderate salinity).
- Real-world accuracy is typically ±0.15–0.5 m depending on sound speed precision and environmental conditions.

## 1. Requirements

### General Requirements
- At least two Sealink-OEM units powered and at least one connected via UART (9600 baud, 8N1, 3.3 V logic) for serial communication with a host system.
- Units must be on the same code channel (`txChID` and `rxChID` typically both 0 by default; configurable via protocol commands).
- Python environment with `pyserial` package installed on host machine.
  - **Note on XP5 pin 3 (`SVC/CMD`): This pin functions as a digital strobe output for transmit/receive events. It can be used by external systems for independent ToF timing. It does not improve nominal precision. No user action is required for normal UART protocol operation.**

### Dryland functional testing
- Place transducers within six inches of each other.
- **Note: Dryland operation is not designed to support payload data integrity! It is useful for functional testing only!**

### Water trials
- Devices positioned inside direct line of sight (LoS) and within maximum acoustic range (1 km or 3 km depending on transducer option).
- Supportive testing conditions: preferably open, calm waters; transducers stationary and approximately level; at least 3 m to both surface and bottom; and separated from adjacent large reflective surfaces.

## 2. Manual Ranging (via Serial Terminal)

Use any serial terminal (PuTTY, Tera Term, screen, minicom, etc.) at 9600 8N1.

### Step-by-step Example

**1. Connect to the local (initiator) unit via UART.**


**2. Send a ping request:**

`$PUWV2,0,0,0*2A<CR><LF>`

   - `0` = `txChID` (transmit channel)
   - `0` = `rxChID` (receive channel)
   - `0` = `rcCmdID` (remote command ID: 0 for ping)
   - `*2A` = example checksum (NMEA XOR of bytes between $ and *)

Note: The ping command does not include a target address. Units must be pre-configured with matching channels.


**3. Immediate acknowledgment from local modem (ACK):**

Typical ACK format:
`$PUWV0,cmdID,errCode*checksum<CR><LF>`

Example:
`$PUWV0,2,0*XX<CR><LF>`

   - `cmdID` = `2` (for `$PUWV2`)
   - `errCode` = `0` (no error; see protocol for other codes)

If `errCode` ≠ `0`, look up error code (e.g., invalid syntax, transmitter busy).


**4. Wait for response from the remote unit (automatic reply if in range and listening):**

Typical response format:
`$PUWV3,txChID,rcCmdID,propTime,MSR,value,azimuth*checksum<CR><LF>`

Example:
`$PUWV3,0,0,0.002489,22.75,,*1B<CR><LF>`

   - `propTime` = one-way propagation time in seconds
   - `MSR` = mean main lobe to side-peak ratio in dB (signal quality indicator)


**5. Calculate range:**

`range ≈ 0.002489 × 1500 = 3.7335 m`

## 3. Automated Ranging with Python Script

The repo currently includes a [basic ranging script](../resources/uart-getRange.py).

This script:

- Opens a serial port (via `--port` argument or interactive prompt)
- Sends a single ping request using sentence `$PUWV2,0,0,0*2A`
- Waits for and parses a `$PUWV3` sentence response
- Calculates sound speed from user inputs (depth, temperature, salinity)
- Prints propagation time and calculated slant range

Basic usage (from repository root):

1. Run: `python resources/uart-getRange.py`
2. Enter prompted values (port, channels, depth, temperature, salinity), or provide them as CLI arguments.
3. Observe the printed propagation time and range (or error if no response).

Example with explicit arguments:
`python resources/uart-getRange.py --port COM3 --tx 0 --rx 0 --test ping --depth 5 --temp 15 --salinity 35`

Example output (if successful):
`Range: 3733.5 m`

**Note: The script is designed for basic range testing only. For improved accuracy, use measured local environmental values and average multiple runs.**

## 4. Basic Ranging with Sealink-OEM Utility App

The Sealink-OEM Utility app can run the same basic ping/ranging workflow without command-line entry.

- Set serial port, channels, and environmental values directly in the app fields.
- Select `ping` and run the command.
- Review propagation time and calculated slant range in the app output panel.

See [Sealink-OEM Utility App Guide](Sealink-OEM_Utility_App_Guide.md) for full app workflow details.

## 5. Sound Speed Compensation Table

Sound speed varies with temperature, salinity, and depth. Use these approximate values or measure on-site.

| Water Type          | Temp (°C) | Salinity (ppt) | Depth (m) | Sound Speed (m/s) |
|---------------------|-----------|----------------|-----------|-------------------|
| Freshwater          | 20        | 0              | 0         | 1482              |
| Seawater (typical)  | 20        | 35             | 0         | 1522              |
| Seawater            | 10        | 35             | 0         | 1490              |
| Seawater            | 25        | 35             | 0         | 1534              |
| Deep ocean (avg)    | 4         | 35             | 1000+     | 1480–1550         |

## 6. Tips for Reliable Ranging

- Max range — Up to 1,000 m (SW-T100 transducer) / 3,000 m (SW-T200/300 transducers) in supportive conditions (clear, calm, open water, low noise).
- Shallow water / multipath — Use averaging (run script multiple times); avoid strong surface/bottom reflections or large reflective surfaces.
- Signal quality (MSR) — Higher dB values indicate cleaner link.
- No response? — Check: matching channels? Powered on? In water? Transducer connected?
- Power saving — Units only transmit during pings; keep Rx duty cycle low.

## 7. Troubleshooting Common Issues

- No `$PUWV3` response → May receive `$PUWV4` (timeout); check acoustic path, verify remote listening, confirm channel match.
- Inconsistent ranges → Environmental factors; repeat measurement and average manually.
- Checksum errors → Ensure terminal/script computes NMEA XOR correctly.
- Error in ACK (`$PUWV0`) → Check `errCode` (e.g., 3 = transmitter busy, 4 = out of range); resolve before retrying.

For advanced protocol commands (set/query channel/address, etc.), see [Sealink-OEM Communication Protocol](./Sealink-OEM_Communication_Protocol.md).
___
Questions or need help with custom ranging setups? Contact support@divenetgps.com.

Last updated: March 2026






