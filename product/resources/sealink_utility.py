"""Simple GUI wrapper around uart-getRange.py functions.

This uses PySimpleGUI to provide a small window where the user can
enter serial port, channels, environmental parameters and choose a command.
The existing protocol logic is imported from uart-getRange so you keep
all the parsing and checksum code in one place.

Usage:
    python sealink_utility.py

Requirements are handled by the workspace venv; PySimpleGUI was added
via pip.  Feel free to convert this to Tkinter or a web frontend later.
"""

"""Tkinter-based GUI for Sealink commands.

This replaces the previous PySimpleGUI wrapper because the environment
had trouble installing the package.  Tkinter is included with the Python
standard library on Windows, so no external dependencies are required.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import importlib.util
import os
import sys
import time

# load protocol helpers from uart-getRange
def resolve_uart_helper_path():
    candidate_dirs = [os.path.dirname(os.path.abspath(__file__))]
    pyinstaller_temp_dir = getattr(sys, '_MEIPASS', None)
    if pyinstaller_temp_dir:
        candidate_dirs.insert(0, pyinstaller_temp_dir)

    checked_paths = []
    for directory in candidate_dirs:
        direct_candidate = os.path.join(directory, 'uart-getRange.py')
        nested_candidate = os.path.join(directory, 'product', 'resources', 'uart-getRange.py')
        dir_wrapped_candidate = os.path.join(directory, 'uart-getRange.py', 'uart-getRange.py')

        for candidate in (direct_candidate, nested_candidate, dir_wrapped_candidate):
            checked_paths.append(candidate)
            if os.path.isfile(candidate):
                return candidate

    checked_display = '\n'.join(checked_paths)
    raise FileNotFoundError(
        f"Unable to locate uart-getRange.py. Checked:\n{checked_display}"
    )


module_path = resolve_uart_helper_path()
module_spec = importlib.util.spec_from_file_location('sealink_uart_helpers', module_path)
if module_spec is None or module_spec.loader is None:
    raise ImportError(f'Unable to create module spec for helper script: {module_path}')

helper_module = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(helper_module)

calculate_nmea_checksum = helper_module.calculate_nmea_checksum
send_rc_ping = helper_module.send_rc_ping
read_response = helper_module.read_response
serial = helper_module.serial

# sound speed formula

def compute_sound_speed(T, S, D):
    return (1449.2 + 4.6*T - 0.055*T*T + 0.00029*T*T*T
            + (1.34 - 0.010*T)*(S - 35) + 0.016*D)

# build UI
root = tk.Tk()
root.title('Sealink-OEM Utility')

frm = ttk.Frame(root, padding=10)
frm.grid()

# port
ttk.Label(frm, text='Serial port').grid(column=0, row=0)
port_var = tk.StringVar()
port_entry = ttk.Entry(frm, textvariable=port_var, width=20)
port_entry.grid(column=1, row=0)

# channels
ttk.Label(frm, text='TX').grid(column=0, row=1)
tx_var = tk.StringVar(value='0')
tx_entry = ttk.Entry(frm, textvariable=tx_var, width=5)
tx_entry.grid(column=1, row=1)

ttk.Label(frm, text='RX').grid(column=2, row=1)
rx_var = tk.StringVar(value='0')
rx_entry = ttk.Entry(frm, textvariable=rx_var, width=5)
rx_entry.grid(column=3, row=1)

# env
ttk.Label(frm, text='Depth m').grid(column=0, row=2)
depth_var = tk.StringVar(value='0')
depth_entry = ttk.Entry(frm, textvariable=depth_var, width=6)
depth_entry.grid(column=1, row=2)

ttk.Label(frm, text='Temp °C').grid(column=2, row=2)
temp_var = tk.StringVar(value='10')
temp_entry = ttk.Entry(frm, textvariable=temp_var, width=6)
temp_entry.grid(column=3, row=2)

ttk.Label(frm, text='Salinity').grid(column=4, row=2)
sal_var = tk.StringVar(value='35')
sal_entry = ttk.Entry(frm, textvariable=sal_var, width=6)
sal_entry.grid(column=5, row=2)

# command
ttk.Label(frm, text='Command').grid(column=0, row=3)
cmd_var = tk.StringVar(value='ping')
cmd_combo = ttk.Combobox(frm, textvariable=cmd_var, values=['ping','device-info','remote-depth'], state='readonly')
cmd_combo.grid(column=1, row=3)

# output
out = scrolledtext.ScrolledText(frm, width=80, height=15)
out.grid(column=0, row=4, columnspan=6, pady=10)

# run

def run_command():
    port = port_var.get()
    try:
        tx = int(tx_var.get() or 0)
        rx = int(rx_var.get() or 0)
    except ValueError:
        messagebox.showerror('Input error','Channels must be integers')
        return
    try:
        depth = float(depth_var.get() or 0)
        temp = float(temp_var.get() or 10)
        sal = float(sal_var.get() or 35)
    except ValueError:
        messagebox.showerror('Input error','Environment values must be numeric')
        return
    sound_speed = compute_sound_speed(temp, sal, depth)
    out.insert(tk.END, f"Using sound speed {sound_speed:.1f} m/s\n")
    cmd = cmd_var.get()
    try:
        ser = serial.Serial(port=port, baudrate=9600,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS,
                            timeout=1)
    except Exception as e:
        out.insert(tk.END, f"Error opening port: {e}\n")
        return
    try:
        if cmd == 'ping':
            send_rc_ping(ser, tx_ch=tx, rx_ch=rx)
            out.insert(tk.END, f"Sent ping: $PUWV2,{tx},{rx},0*XX\n")
            out.see(tk.END)
            root.update()
            time.sleep(0.5)
            tp, distance = read_response(ser, timeout_sec=10, sound_speed=sound_speed)
            if tp is not None:
                out.insert(tk.END, f"Propagation time: {tp:.4f} s → Slant range: {distance:.1f} m\n")
            else:
                out.insert(tk.END, "No response received\n")
            out.see(tk.END)
            root.update()
        elif cmd == 'device-info':
            body = 'PUWV?,0'
            checksum = calculate_nmea_checksum(body)
            ser.write(f"${body}*{checksum}\r\n".encode())
            out.insert(tk.END, f"Sent device info request: ${body}*XX\n")
            out.see(tk.END)
            root.update()
            line = ser.readline().decode('ascii', errors='ignore').strip()
            out.insert(tk.END, f"Received {line}\n")
            out.see(tk.END)
            root.update()
        elif cmd == 'remote-depth':
            body = f"PUWV2,{tx},{rx},2"
            checksum = calculate_nmea_checksum(body)
            ser.write(f"${body}*{checksum}\r\n".encode())
            out.insert(tk.END, f"Sent remote depth request: ${body}*XX\n")
            out.see(tk.END)
            root.update()
            time.sleep(0.5)
            tp, distance = read_response(ser, timeout_sec=10, sound_speed=sound_speed)
            if tp is not None:
                out.insert(tk.END, f"Propagation time: {tp:.4f} s → Slant range: {distance:.1f} m\n")
            else:
                out.insert(tk.END, "No response received\n")
            out.see(tk.END)
            root.update()
    finally:
        ser.close()

run_button = ttk.Button(frm, text='Run', command=run_command)
run_button.grid(column=0, row=5)

quit_button = ttk.Button(frm, text='Quit', command=root.destroy)
quit_button.grid(column=1, row=5)

root.mainloop()
