"""Interactive USB-serial client for an Arduino; type `q` to quit."""
from __future__ import annotations

import argparse
import sys
import time

import serial
import serial.tools.list_ports

from common import add_serial_args, is_quit

DEFAULT_PORT_INDEX = 4  # index into the list of detected serial ports


def pick_port(devices: list[str], index: int) -> str:
    """Return the device at `index`, with a clear error when out of range."""
    if not 0 <= index < len(devices):
        raise IndexError(f"port index {index} out of range; detected: {devices or 'none'}")
    return devices[index]


def normalize_command(raw: str) -> str | None:
    """Upper-case a typed command; None means the user asked to quit."""
    cmd = raw.upper()
    return None if is_quit(cmd, "q") else cmd


def run(ser: serial.Serial) -> None:
    """Print pending device output, then prompt and send one command per loop."""
    print("Connected to Arduino. Ready to send commands. Type 'q' to quit.")
    while True:
        while ser.in_waiting > 0:
            print(f"Response: {ser.readline().decode('utf-8').strip()}")

        cmd = normalize_command(input("Command: "))
        if cmd is None:
            break
        ser.write(cmd.encode())
        print(f"Sending Command: {cmd}")
        time.sleep(2)  # wait for the data to be sent


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_serial_args(parser)
    parser.add_argument("--index", type=int, default=DEFAULT_PORT_INDEX,
                        help="index into detected ports, used when --port is omitted (default: %(default)s)")
    parser.add_argument("--list", action="store_true", help="list detected serial ports and exit")
    args = parser.parse_args(argv)

    devices = [p.device for p in serial.tools.list_ports.comports()]
    if args.list:
        for i, dev in enumerate(devices):
            print(f"{i}: {dev}")
        return 0

    ser = None
    try:
        port = args.port or pick_port(devices, args.index)
        ser = serial.Serial(port, args.baud, timeout=1)
        time.sleep(1)  # wait for the connection to initialize
        run(ser)
    except (serial.SerialException, IndexError) as e:
        print(f"Error: {e}")
        return 1
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        if ser is not None and ser.is_open:
            ser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
