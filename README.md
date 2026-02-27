# DiveNET: Sealink-OEM Subsea Wireless Modem

**Sealink-OEM** is a compact, high-reliability underwater acoustic modem and communication platform by DiveNET Subsea Wireless (Beringia Enterprises LLC).

## Key features:
- Highly compact (75 mm x 44 mm PCB)
- Reliable, energy-efficient performance
- Communication envelope up to 3,000 m range / 1,000 m depth
- Up to 634 bps bandwidth
- 255 responders and 20 code channels per device
- 9600 bps UART interface (3.3V logic)
- Support for external pressure/temperature sensor (I²C)
- GNSS and RF module expansion
- Built-in TOF and Tx/Rx strobe output for external timing/ranging
- Designed for ROV, AUV, subsea IoT and diver systems 

## Quick Start
1. Connect power (connector XP2; +12 V nominal) and transducer (conector XP1).
2. Use any serial terminal (PuTTY, Tera Term) at 9600 8N1.
3. Send `$PUWV2,0,0,0*2A` to ping a remote unit.
4. Receive `$PUWV3,0,0,tp,msr*hh` → range (approximate for testing) = tp × 1500 / 2 (m).
5. Refine performance with improved distance formula and setting of correct ambient parameters.

Full documentation → see `/docs/` folder.

## Download & Resources
- [Ranging Python Script](/resources/Sealink_Ranging_Script.py)
- [Firmware Updater](/resources/DiveNET_Firmware_Updater.exe) (coming soon)

Questions? Contact DiveNET support: support@divenetgps.com

© 2026 DiveNET Subsea Wireless — All rights reserved.
