"""Test the parser module."""
import pytest
import os
import sys
import io

from names import Names
from devices import Devices
from network import Network
from monitors import Monitors
from scanner import Scanner
from parse import Parser


@pytest.fixture
def parser_with_flip_flop():
    """Return a parser instance with flip-flop circuit configuration."""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)

    # Create a test file path for flip-flop circuit
    file_path = os.path.join(os.path.dirname(__file__), "test_maintenance",
                             "siggen_flip_flop.txt")
    scanner = Scanner(file_path, names)
    parser = Parser(names, devices, network, monitors, scanner)

    return parser, names, devices, network, monitors

@pytest.fixture
def parser_with_error_devices():
    """Return a parser instance with error test file one."""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)

    file_path = os.path.join(os.path.dirname(__file__), "test_maintenance",
                             "siggen_flip_flop_incorrect.txt")
    scanner = Scanner(file_path, names)
    parser = Parser(names, devices, network, monitors, scanner)

    return parser


def test_monitor_connections_flip_flop(parser_with_flip_flop):
    """Test if the parser correctly handles monitor connections for the
    flip-flop circuit."""
    parser, names, devices, network, monitors = parser_with_flip_flop

    # Parse the network which includes monitor definitions
    assert parser.parse_network()

    # Get the device IDs we expect to be monitored based on test_flip_flop.txt
    [D1_ID, N1_ID, QBAR_ID, SI1_ID] = names.lookup(["D1", "N1", "QBAR", "SI1"])

    # Check that the monitors dictionary contains the expected monitors
    # Note: D1.QBAR is monitored, so we need to check for (D1_ID, QBAR_ID)
    assert (D1_ID, QBAR_ID) in monitors.monitors_dictionary
    assert (N1_ID, None) in monitors.monitors_dictionary
    assert (SI1_ID, None) in monitors.monitors_dictionary

    # Check that the monitors dictionary has the correct structure
    assert monitors.monitors_dictionary[(D1_ID, QBAR_ID)] == []
    assert monitors.monitors_dictionary[(N1_ID, None)] == []
    assert monitors.monitors_dictionary[(SI1_ID, None)] == []

    # Verify that only these two devices are being monitored
    assert len(monitors.monitors_dictionary) == 3

    # Get the monitored signal names
    monitored_signals, _ = monitors.get_signal_names()

    # Verify the correct signals are being monitored
    assert "D1.QBAR" in monitored_signals
    assert "N1" in monitored_signals
    assert "SI1" in monitored_signals
    assert len(monitored_signals) == 3

def test_parser_error_devices(parser_with_error_devices, capsys):
    """Test if the parser correctly handles errors in
    test_print_error_devices.txt."""
    parser = parser_with_error_devices

    # Parse the network which should contain errors
    assert not parser.parse_network()  # Should return False due to errors

    # Get the captured output
    captured = capsys.readouterr()
    output = captured.out

    # Check for expected error messages
    expected_errors = [
        "Expected a waveform",
        "Expected a waveform",
        "Expected number of inputs",
        "Expected a waveform",
        "Expected a waveform",
        "Expected a waveform",
        "Device has already been initialised",
        "Expected a waveform",
        "Siggen waveform must only consist of bits",
        "Expected a waveform",
        "Expected a waveform",
        "Expected a waveform",
        "Expected a waveform",
        "Expected a waveform",
        "Invalid device name",
        "Expected a clock period",
        "Expected a clock period",
        "Device has already been initialised",
        "Expected a bit (0 or 1)",
        "Expected a bit (0 or 1)",
        "Device not found",
        "Device not found",
        "Device not found"
    ]

    expected_lines = [
        "LINE 1:",
        "LINE 2:",
        "LINE 5:",
        "LINE 6:",
        "LINE 8:",
        "LINE 9:",
        "LINE 10:",
        "LINE 12:",
        "LINE 13:",
        "LINE 14:",
        "LINE 15:",
        "LINE 16:",
        "LINE 17:",
        "LINE 18:",
        "LINE 18:",
        "LINE 22:",
        "LINE 23:",
        "LINE 26:",
        "LINE 28:",
        "LINE 29:",
        "LINE 43:",
        "LINE 44:",
        "LINE 48:"
    ]

    expected_indications = [
        "DEVICES SI25:SIGGEN,\n                   ^",
        "        SI25:SIGGEN XOR,\n                       ^",
        "        N1:NAND,\n               ^",
        "        SI2:SIGGEN a000b001,\n                           ^",
        "        SI3:SIGGEN DEVICES,\n                          ^",
        "        SI4:SIGGEN a,\n                    ^",
        "        SI1:SIGGEN 00001001,\n                           ^",
        "        SI6:SIGGEN,\n                  ^",
        "        SI7:SIGGEN 4,\n                    ^",
        "        SI8:SIGGEN A,\n                    ^",
        "        SI9:SIGGEN .,\n                    ^",
        "        SI10:SIGGEN :,\n                     ^",
        "        SI11:SIGGEN >,\n                     ^",
        "        SI12:SIGGEN ,,\n                    ^",
        "        SI12:SIGGEN ,,\n                     ^",
        "        C1:CLOCK,\n                ^",
        "        C2:CLOCK AND,\n                    ^",
        "        S1:SIGGEN 1001001,\n                         ^",
        "        S4:SWITCH,\n                 ^",
        "        S5:SWITCH AND,\n                     ^",
        "        D2.Q > N1.I1,\n               ^",
        "        D2.QBAR > N1.I2 ;\n",
        "        N1 ;\n           ^"
    ]

    # Check that each expected error appears in the output
    for error in expected_errors:
        assert error in output

    for line in expected_lines:
        assert line in output

    for indication in expected_indications:
        assert indication in output

    # Check total number of errors
    print(len(expected_errors), len(expected_lines), len(expected_indications))
    assert parser.error_count == len(expected_errors)
    assert parser.error_count == len(expected_lines)
    assert parser.error_count == len(expected_indications)