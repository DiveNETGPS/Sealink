Sealink-OEM Windows Package
===========================

This folder includes:
- SealinkGUI.exe        (main GUI app)
- SealinkListener.exe   (test listener)
- run_gui.bat           (launch GUI only)
- run_listener.bat      (launch listener only)
- run_all.bat           (launch listener + GUI)

Quick start:
1) Connect your hardware and identify the COM port.
2) Double-click run_gui.bat for normal operation.
3) For local testing/demo mode, double-click run_all.bat.

Virtual COM simulation:
- For bench testing without hardware, use a virtual COM port pair and run_all.bat.
- run_all.bat starts SealinkListener.exe plus the GUI to simulate protocol responses.

Troubleshooting:
- If Windows SmartScreen warns, click "More info" then "Run anyway" (if trusted source).
- Ensure the serial device appears in Device Manager.
- Listener is only for test workflows; production users typically run GUI only.
