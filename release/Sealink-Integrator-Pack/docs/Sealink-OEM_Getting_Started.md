# DiveNET: Sealink-OEM - Getting Started

## 1. Bare-bones Operation

The modem can operate independently as a remote responder able to receive and respond to standard command requests without a data interface to a host system. To operate the modem as a remote responder in minimum configuration:  

- Connect the transducer to connector XP1 (OUT)
- Connect a +12-14V power supply to connector XP2 (POWER)

## 2. Manual Control (Send Commands, Read Results)

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

## 3. Automated Control / Custom Features
   
For scripting, logging, or integration, any language that can open a serial port at 9600 8N1 works.

We recommend Python:  

- Install Python (free from python.org) with `pyserial` package 
- Use our sample Python script for initial testing and familiarization.
- The script accepts command-line options (for example `--port`, `--tx`, `--rx`, `--test`) and prompts for any missing values.
- For interactive operation, use the Sealink-OEM Utility app and enter port/channels/environment values in the app fields.
- See [Sealink-OEM Utility App Guide](Sealink-OEM_Utility_App_Guide.md) for app workflows.

Other options:  
- C# (Windows apps)  
- Arduino or Raspberry Pi (for embedded projects — use serial libraries like Serial or pyserial)

## 4. References
- [Sealink-OEM technical drawing](Sealink-OEM_Technical_Drawing.pdf)
- [Connector pinout guide](Sealink-OEM_Pinout_and_Interface.md)
- [Communication protocol](Sealink-OEM_Communication_Protocol.md) 

## 5. Next steps

- For app-focused operation (Windows package + local launch scripts), continue with [Sealink-OEM Utility App Guide](Sealink-OEM_Utility_App_Guide.md).
- For command details, use [Communication protocol](Sealink-OEM_Communication_Protocol.md).
- For range testing specifics, use [Basic Ranging Guide](Sealink-OEM_Basic_Ranging_Guide.md).

___
Questions? Write to support@divenetgps.com.
