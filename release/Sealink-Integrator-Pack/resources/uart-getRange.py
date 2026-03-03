"""\
Basic Sealink-OEM command-line utility / test harness.

This script demonstrates a few Sealink communication protocol commands
using the NMEA-style `$PUWV` sentences described in
`docs/Sealink-OEM_Communication_Protocol.md`.

- Remote code request (numeric): `$PUWV2,tx,rx,cmdID*hh`  
  Used for ping (cmdID=0) and requesting remote depth (cmdID=2).  
- Remote code response: `$PUWV3,tx,cmdID,propTime,MSR[,value][,azimuth]*hh`  
  Propagation time is parsed into slant range.  
- Device information request: `$PUWV?,0*hh` → response `$PUWV!,...*hh`.

The command-line interface supports three tests:
`ping`, `device-info`, and `remote-depth`.

Usage examples are in the repository documentation and the code comments.
"""

import serial
import time
import sys

def calculate_nmea_checksum(sentence):
    """NMEA checksum: XOR of bytes after $ up to * (excluding $)"""
    chk = 0
    for char in sentence[1:]:  # skip $
        chk ^= ord(char)
    return f"{chk:02X}".upper()

def send_rc_ping(ser, tx_ch=0, rx_ch=0):
    # remote code request using command ID 0 (RC_PING)
    # format per protocol: $PUWV2,txChID,rxChID,rcCmdID*hh<CR><LF>
    cmd_body = f"PUWV2,{tx_ch},{rx_ch},0"
    checksum = calculate_nmea_checksum(cmd_body)
    full_cmd = f"${cmd_body}*{checksum}\r\n"
    ser.write(full_cmd.encode('ascii'))
    print(f"Sent ping: {full_cmd.strip()}")

def read_response(ser, timeout_sec=5, sound_speed=1500):
    """Read response from modem, calculate distance using sound_speed (m/s)."""
    start_time = time.time()
    while time.time() - start_time < timeout_sec:
        line = ser.readline().decode('ascii', errors='ignore').strip()
        if not line:
            continue
        print(f"Received: {line}")
        
        # look for remote code response (PUWV3)
        if line.startswith('$PUWV3,'):
            parts = line.split(',')
            # parts: ['${PUWV3}', txChID, rcCmdID, propTime, MSR, ...]
            if len(parts) >= 4:
                try:
                    tp_sec = float(parts[3])  # one-way propagation time
                    # distance = time × sound speed
                    distance_m = tp_sec * sound_speed
                    print(f"Propagation time: {tp_sec:.4f} s → Slant range: {distance_m:.1f} m")
                    return tp_sec, distance_m
                except ValueError:
                    print("Failed to parse tp value")
        time.sleep(0.05)
    print("No RC_PING response received within timeout")
    return None, None

# command-line interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Send an RC ping over a Sealink serial port and measure range."
    )
    parser.add_argument("--port", "-p", help="serial port (e.g. COM3 or /dev/ttyUSB0)")
    parser.add_argument("--tx", "-t", type=int, help="transmit channel index (default 0)")
    parser.add_argument("--rx", "-r", type=int, help="receive channel index (default 0)")
    parser.add_argument("--timeout", "-o", type=float, default=10,
                        help="response timeout in seconds")
    parser.add_argument("--test", "-x", choices=["ping","device-info","remote-depth"],
                        help="which test command to execute (ping, device-info, remote-depth)")
    parser.add_argument("--depth", "-d", type=float, help="water depth in meters (for sound speed calc)")
    parser.add_argument("--temp", "-T", type=float, help="water temperature in °C (for sound speed calc)")
    parser.add_argument("--salinity", "-s", type=float, help="water salinity PSU (for sound speed calc)")
    args = parser.parse_args()

    # prompt for any missing values
    if not args.port:
        # show available ports for convenience
        try:
            from serial.tools import list_ports
            ports = [p.device for p in list_ports.comports()]
            if ports:
                print("Detected serial ports:", ", ".join(ports))
        except Exception:
            pass
        args.port = input("Enter serial port (e.g. COM3): ").strip()
    if args.tx is None:
        try:
            args.tx = int(input("Enter transmit channel [0]: ") or 0)
        except ValueError:
            args.tx = 0
    if args.rx is None:
        try:
            args.rx = int(input("Enter receive channel [0]: ") or 0)
        except ValueError:
            args.rx = 0

    # environmental inputs for sound speed
    if args.depth is None:
        try:
            args.depth = float(input("Enter depth in meters [0]: ") or 0)
        except ValueError:
            args.depth = 0.0
    if args.temp is None:
        try:
            args.temp = float(input("Enter temperature °C [10]: ") or 10)
        except ValueError:
            args.temp = 10.0
    if args.salinity is None:
        try:
            args.salinity = float(input("Enter salinity PSU [35]: ") or 35)
        except ValueError:
            args.salinity = 35.0

    # calculate sound speed using Mackenzie 1981 formula (approx)
    # speed m/s = 1449.2 + 4.6*T - 0.055*T^2 + 0.00029*T^3
    #             + (1.34 - 0.010*T)*(S-35) + 0.016*D
    T = args.temp
    S = args.salinity
    D = args.depth
    sound_speed = (1449.2 + 4.6*T - 0.055*T*T + 0.00029*T*T*T
                   + (1.34 - 0.010*T)*(S - 35) + 0.016*D)
    print(f"Using sound speed {sound_speed:.1f} m/s (depth={D}m, temp={T}°C, sal={S} PSU)")

    # attempt to open serial port, with helpful error if fails
    try:
        ser = serial.Serial(
            port=args.port,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
    except serial.SerialException as e:
        print(f"Error opening port {args.port}: {e}")
        print("Available ports:")
        try:
            from serial.tools import list_ports
            for p in list_ports.comports():
                print(f"  {p.device}")
        except Exception:
            pass
        sys.exit(1)

    # choose a test command
    TEST_COMMANDS = {
        "ping": "Remote-code ping (ID 0) – measure slant range",
        "device-info": "Request device information",
        "remote-depth": "Remote-code depth request (ID 2) using tx/rx channels"
    }

    if not args.test:
        print("Select a test command:")
        for i, (key, desc) in enumerate(TEST_COMMANDS.items(), start=1):
            print(f" {i}) {desc} ({key})")
        choice = input("Enter number or name [1]: ").strip()
        if not choice:
            choice = "1"
        # resolve choice
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(TEST_COMMANDS):
                args.test = list(TEST_COMMANDS.keys())[idx]
        else:
            if choice in TEST_COMMANDS:
                args.test = choice
    if args.test not in TEST_COMMANDS:
        print(f"Unknown test command '{args.test}', defaulting to ping")
        args.test = "ping"

    try:
        if args.test == "ping":
            send_rc_ping(ser, tx_ch=args.tx, rx_ch=args.rx)
            time.sleep(0.5)
            tp, distance = read_response(ser, timeout_sec=args.timeout, sound_speed=sound_speed)
        elif args.test == "device-info":
            # device info request per protocol: $PUWV?,reserved*hh
            body = "PUWV?,0"
            checksum = calculate_nmea_checksum(body)
            full = f"${body}*{checksum}\r\n"
            ser.write(full.encode('ascii'))
            print(f"Sent device info request: {full.strip()}")
            # read one line or until timeout
            start = time.time()
            while time.time() - start < args.timeout:
                line = ser.readline().decode('ascii', errors='ignore').strip()
                if line:
                    print(f"Received: {line}")
                    break
        elif args.test == "remote-depth":
            # the remote-depth command is a remote code request with ID 2
            body = f"PUWV2,{args.tx},{args.rx},2"
            checksum = calculate_nmea_checksum(body)
            full = f"${body}*{checksum}\r\n"
            ser.write(full.encode('ascii'))
            print(f"Sent remote depth request: {full.strip()}")
            tp, distance = read_response(ser, timeout_sec=args.timeout, sound_speed=sound_speed)
        else:
            print("No command executed")
    finally:
        ser.close()
