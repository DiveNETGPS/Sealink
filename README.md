# DiveNET: Sealink

## Basic UART Ranging Instructions  



### 1. Setup:

* Two modems inside maximum range and line-of-sight constraints.
* Active COM ports identified.
* Both modems in Command Mode (default on power-up; if in Transparent Mode, send `$PUWV,MD,1*checksum` to switch).
* Both modems on same code channel (default 0; configurable via `$PUWV,CH,tx,rx*checksum` if needed).
* Baud rate: 9600 bps (default).




### 2. Send request command:

* Send **RC_PING** command (Remote Code Ping) to get response with propogation time/TOF.
  * `PUWV2,0,0,0`
* Checksum calculation: XOR of all bytes after $ up to * (standard NMEA method).




### 3. Get response with propagation time (Tp in seconds) and other info:

* `$PUWV3,txCh,rcCmdID,propTime,MSR*hh<CR><LF>` (example: "$PUWV3,0,0,0.667,25.40*3F")

  * tp = propagation time in seconds (e.g. 0.667 > ~1 km round-trip > ~500 m one-way)
  * msr = signal-to-noise ratio / mark level in dB
  * az = azimuth if available (requires USBL antenna)




### 4. For testing, apply simple range formula:

* **one_way_distance_m = tp * sound_speed_mps / 2**
  * sound_speed_mps ≈ 1500 m/s (fresh water 20°C); adjust for salinity/temp if needed (1.5 m/s per PSU, etc.).
 



### 5. For accuracy, set accurate environmental parameters and use a better range formula (e.g. Mackenzie or UNESCO equation).

* `$PUWV,SW,txCh,rxCh,salinityPSU,commandModeByDefault,ACKonTxFinished,gravityMps2*checksum<CR><LF>`

Where:
* salinityPSU: Salinity in PSU (practical salinity units) — typical seawater 35 PSU, fresh water 0.
* gravityMps2: Local gravity acceleration in m/s² — standard 9.80665, but varies slightly by latitude/altitude (e.g. 9.78 at equator, 9.83 at poles).
* Other fields:
  * txCh, rxCh: code channels (usually same, e.g. 0,0)
  * commandModeByDefault: 1 = start in Command Mode (recommended)
  * ACKonTxFinished: 0 or 1 (ACK after transmit complete — usually 0 for ranging)
 
Example:
* Set salinity to 35 PSU, gravity to 9.81 m/s², Command Mode default, no ACK on TX:
  * `$PUWV,SW,0,0,35,1,0,9.81*checksum`
* Set salinity to 0 (fresh water), gravity to 9.82:
  * `$PUWV,SW,0,0,0,1,0,9.82*checksum`
* Query current settings:
  * `$PUWV,SW?*checksum`



 



 




