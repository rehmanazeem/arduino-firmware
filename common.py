"""Helpers shared by the host-side utilities (tcp.py, serialCom.py, bluetooth.py)."""
from __future__ import annotations

import argparse

DEFAULT_BAUD = 9600  # matches the sketches / HC-05 default


def add_serial_args(parser: argparse.ArgumentParser, default_port: str | None = None) -> None:
    """Add the --port/--baud options used by the serial-based clients."""
    parser.add_argument("--port", default=default_port, help="serial device path (e.g. /dev/ttyUSB0, COM3)")
    parser.add_argument("--baud", type=int, default=DEFAULT_BAUD, help="baud rate (default: %(default)s)")


def is_quit(text: str, *words: str) -> bool:
    """Case-insensitive check of whether `text` is one of the quit `words`."""
    return text.strip().lower() in words
