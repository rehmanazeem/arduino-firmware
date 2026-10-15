import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import bluetooth
import serialCom
import tcp
from common import is_quit


def test_tcp_number_validation_and_framing():
    assert tcp.is_valid_number("99") and tcp.is_valid_number("0")
    assert not tcp.is_valid_number("") and not tcp.is_valid_number("-1") and not tcp.is_valid_number("a1")
    assert tcp.encode_request("1") == b"1\n"


def test_bluetooth_framing():
    assert bluetooth.encode_message("hi") == b"hi\r\n"


def test_quit_words_case_insensitive():
    assert is_quit(" EXIT ", "exit") and not is_quit("go", "exit")


def test_serial_command_normalisation():
    assert serialCom.normalize_command("on") == "ON"
    assert serialCom.normalize_command("Q") is None


def test_pick_port():
    assert serialCom.pick_port(["a", "b"], 1) == "b"
    with pytest.raises(IndexError):
        serialCom.pick_port(["a"], 4)
