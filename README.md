# DiveNET: Sealink-OEM Subsea Wireless Modem

<img src="/docs/images/img002.jpg" alt="Sealink-OEM" width="50%">

**Sealink-OEM** is a compact, high-reliability underwater acoustic modem and communication platform developed by DiveNET Subsea Wireless (Beringia Enterprises LLC).

### Key Features
- Extremely compact PCB: 73.5 mm × 44 mm
- Reliable long-range communication
- Multi-mode functionality
- Communication envelope up to 3,000 m range / 1,000 m depth (transducer-dependent)
- Up to 634 bps bandwidth
- 255 logical addresses (responders) and 20 code channels
- 9600 bps UART interface (3.3 V logic)
- Built-in support for external pressure/temperature sensor (I²C on XP6)
- GNSS and RF module expansion (XP7 & XP8)
- Built-in Time-of-Flight (ToF) ranging with ~0.15 m resolution
- Tx/Rx strobe output (SVC/CMD on XP5 Pin 3) for external high-precision timing
- Designed for ROV, AUV, diver systems, subsea IoT, and custom integrations

### Primary Specifications
- **Board size**: 73.5 mm × 44 mm
- **Power**: +12 V DC nominal
- **Logic level**: 3.3 V UART (0–3.3 V)
- **UART settings**: 9600 baud, 8N1 (default)
- **Connectors**: Molex Mini-Fit Jr. series
- **Operating modes**: Transparent channel, Command mode, Packet mode
- **Ranging**: ~0.15 m resolution (acoustic detection limit)

### Transducer Options
Sealink-OEM supports interchangeable transducers for different mission profiles:

1. **1,000 m acoustic range / 600 m depth rating**  
   - Model: SW-T100  
   - Max slant range: ~1,000 m (line-of-sight)  
   - Max operational depth: 600 m  
   - [Specification]

2. **3,000 m acoustic range / 300 m depth rating**  
   - Model: SW-T200    
   - Max slant range: ~3,000 m (line-of-sight)  
   - Max operational depth: 300 m  
   - [Specification]

3. **3,000 m acoustic range / 1,000 m depth rating**  
   - Model: SW-T300    
   - Max slant range: ~3,000 m (line-of-sight)  
   - Max operational depth: 1,000 m  
   - [Specification]

### Quick Start
1. Connect power (+12 V nominal) to XP2 and transducer to XP1.  
2. Use any serial terminal (PuTTY, Tera Term, CoolTerm, minicom) at 9600 8N1.  
3. Send `$PUWV2,0,0,0*2A` to ping a remote unit.  
4. Receive `$PUWV3,0,0,tp,msr*hh` → approximate range = tp × 1500 / 2 (m).  
5. Refine with correct sound speed (adjust for temperature/salinity).  
6. For automation, use Python or similar over XP5 UART.

Full documentation → see [docs](docs) folder.

### Download & Resources
- [Getting Started Guide](/docs/getting-started.md)
- [Pinout & Interface](/docs/pinout-and-interface.md)
- [Ranging Python Script](/resources/uart-getRange.py)

Questions? Contact DiveNET support: support@divenetgps.com

© 2026 DiveNET Subsea Wireless — All rights reserved.
