# DiveNET: Sealink-OEM - Getting Started

## 1. Barebones operation

The modem can operate interely independetly as a remote responder able to receive and respond to standard command requests.  
To operate the modem as a remote responder in minimum configuration:  

- Connect the transducer to connector XP1 (OUT)
- Connect a +12-14V power supply to connector XP2 (POWER)

References: Sealink-OEM technical drawing; pinout diagram  

## 2. Manual control (send commands, read results)

For manual control, at least one modem must be connected to a serial interface to act as the "host" device and send command requests as needed.
   
- Transducer connected to XP1  
- Main power to XP2 (+12-14V)
- Serial connection to XP5 (serial to USB adapter or direct UART pins)  
- Default settings: 9600 8N1 (9600 speed, 8 data bits, no parity, 1 stop bit)  

Easy tools that work right away (no extra install):  

- Windows: PuTTY or Tera Term  
- Mac: CoolTerm  
- Linux: minicom or screen  

Tip: On Windows, find your COM port in Device Manager → Ports (COM & LPT).

For hardware projects, Arduino or Raspberry Pi can also connect directly to XP5 pins for manual control.

## 3. Automated control / custom features
   
For scripting, logging, or integration, any language that can open a serial port at 9600 8N1 works.

We recommend Python:  

- Install Python (free from python.org) with `pyserial` package 
- Use our sample Python script for initial testing and familiarization — just change the port name and run.

Other options:  
- C# (Windows apps)  
- Arduino or Raspberry Pi (for embedded projects — use serial libraries like Serial or pyserial)

Questions? Write to support@divenetgps.com.
