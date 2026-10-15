"""Interactive TCP client for the ESP8266 relay sketches (port 8080 by default).

Type a number to send it; `99` asks the device to close the session and exits.
"""
from __future__ import annotations

import argparse
import socket
import sys
import time

DEFAULT_HOST = "192.168.x.x"  # replace with the IP printed by the ESP8266
DEFAULT_PORT = 8080
EXIT_CODE = "99"


def is_valid_number(text: str) -> bool:
    """True if `text` is a non-negative integer the sketches can parse."""
    return text.isdigit()


def encode_request(num: str) -> bytes:
    """Frame a command as the newline-terminated line the sketches read."""
    return (num + "\n").encode()


def connect(host: str, port: int, timeout: float = 10) -> socket.socket:
    """Open a TCP connection to the device."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(timeout)
    client.connect((host, port))
    return client


def run(client: socket.socket) -> None:
    """Prompt loop: send each valid number and print the device's reply."""
    while True:
        num = input("Enter a number: ")
        if not is_valid_number(num):
            print("Please enter a valid number.")
            continue

        client.send(encode_request(num))
        time.sleep(0.2)  # wait for ESP8266 to process
        print("ESP8266 says:", client.recv(1024).decode())

        if num == EXIT_CODE:
            break


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default=DEFAULT_HOST, help="ESP8266 IP address (default: %(default)s)")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="TCP port (default: %(default)s)")
    args = parser.parse_args(argv)

    print("Attempting to connect to ESP8266...")
    try:
        client = connect(args.host, args.port)
    except OSError as e:
        print(f"Error connecting to ESP8266: {e}")
        return 1
    print("Connection established.")
    print("Connected to ESP8266 at", args.host)

    try:
        run(client)
    except KeyboardInterrupt:
        pass
    finally:
        client.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
