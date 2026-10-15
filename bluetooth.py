"""Send typed messages to an HC-05 Bluetooth serial bridge; type `exit` to quit."""
from __future__ import annotations

import argparse
import sys

import serial

from common import add_serial_args, is_quit

DEFAULT_PORT = "/dev/cu.HC-05"  # macOS name of a paired HC-05; adjust for your OS


def encode_message(message: str) -> bytes:
    """Frame a message with the CRLF terminator the HC-05 side expects."""
    return (message + "\r\n").encode("utf-8")


def run(link: serial.Serial) -> None:
    """Prompt loop: send each typed line until the user types `exit`."""
    print("Enter messages to send to HC-05 (type 'exit' to quit):")
    while True:
        message = input(">>> ").strip()
        if is_quit(message, "exit"):
            break
        link.write(encode_message(message))
        print(f"Sent: {message}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_serial_args(parser, default_port=DEFAULT_PORT)
    args = parser.parse_args(argv)

    link = None
    try:
        link = serial.Serial(args.port, args.baud, timeout=1)
        print(f"Connected to {args.port} at {args.baud} baud rate.")
        run(link)
    except serial.SerialException as e:
        print(f"Error: {e}")
        return 1
    finally:
        if link is not None and link.is_open:
            link.close()
            print("Connection closed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
