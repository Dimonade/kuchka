"""Tests for device_config.py.

This directory is documentation, not part of the installed `kuchka` package,
so `device_config` is imported by adding this directory to `sys.path` and not through
a package import.

Run with `pytest docs/examples/config_migration` from the repository root, or `pytest`
from inside this directory.
"""

from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pytest
from device_config import ConfigError
from device_config import load_device_config

from kuchka import Baud
from kuchka import Celsius
from kuchka import Hertz
from kuchka import Kelvin
from kuchka import Millivolt
from kuchka import Volt

CONFIG_PATH = Path(__file__).parent / "config_modern.toml"


def test_loads_the_shipped_config() -> None:
    config = load_device_config(CONFIG_PATH)

    assert config.red_led.voltage.minimum == Millivolt(-1)
    assert config.red_led.voltage.maximum == Millivolt(1)
    assert config.blue_led.voltage.minimum == Volt(0)
    assert config.blue_led.voltage.maximum == Volt(Decimal("3.300"))


def test_comparison_works_across_differently_declared_units() -> None:
    """Comparing a millivolt limit and a volt limit needs no manual conversion."""
    config = load_device_config(CONFIG_PATH)
    assert config.red_led.voltage.maximum < config.blue_led.voltage.maximum


def test_temperature_fields_accept_either_celsius_or_kelvin() -> None:
    config = load_device_config(CONFIG_PATH)
    assert config.red_led.temperature.minimum == Celsius(15)
    assert config.blue_led.temperature.minimum == Kelvin(Decimal("288.15"))


def test_comms_settings_use_frequency_and_baud_rate() -> None:
    config = load_device_config(CONFIG_PATH)
    assert config.comms.uart_baud_rate == Baud(9600)
    assert config.comms.sensor_poll_rate == Hertz(500)


def test_unit_from_the_wrong_dimension_is_rejected() -> None:
    broken = """
    [red_led.accepted_voltage]
    min = { value = "-1.000", unit = "mA" }
    max = { value = "1.000", unit = "mV" }
    [red_led.accepted_current]
    min = { value = "0.000", unit = "mA" }
    max = { value = "20.000", unit = "mA" }
    [red_led.accepted_temperature]
    min = { value = "15.0", unit = "C" }
    max = { value = "45.0", unit = "C" }
    [blue_led.accepted_voltage]
    min = { value = "0.000", unit = "V" }
    max = { value = "3.300", unit = "V" }
    [blue_led.accepted_current]
    min = { value = "0.000", unit = "A" }
    max = { value = "0.050", unit = "A" }
    [blue_led.accepted_temperature]
    min = { value = "288.15", unit = "K" }
    max = { value = "318.15", unit = "K" }
    [comms]
    uart_baud_rate = { value = "9600", unit = "Bd" }
    sensor_poll_rate = { value = "500", unit = "Hz" }
    """
    _assert_toml_string_raises(broken, match="not recognised for this field")


def test_unrecognised_unit_is_rejected() -> None:
    broken = """
    [red_led.accepted_voltage]
    min = { value = "-1.000", unit = "dBm" }
    max = { value = "1.000", unit = "mV" }
    [red_led.accepted_current]
    min = { value = "0.000", unit = "mA" }
    max = { value = "20.000", unit = "mA" }
    [red_led.accepted_temperature]
    min = { value = "15.0", unit = "C" }
    max = { value = "45.0", unit = "C" }
    [blue_led.accepted_voltage]
    min = { value = "0.000", unit = "V" }
    max = { value = "3.300", unit = "V" }
    [blue_led.accepted_current]
    min = { value = "0.000", unit = "A" }
    max = { value = "0.050", unit = "A" }
    [blue_led.accepted_temperature]
    min = { value = "288.15", unit = "K" }
    max = { value = "318.15", unit = "K" }
    [comms]
    uart_baud_rate = { value = "9600", unit = "Bd" }
    sensor_poll_rate = { value = "500", unit = "Hz" }
    """
    _assert_toml_string_raises(broken, match="dBm")


def test_inverted_range_is_rejected() -> None:
    broken = """
    [red_led.accepted_voltage]
    min = { value = "1.000", unit = "mV" }
    max = { value = "-1.000", unit = "mV" }
    [red_led.accepted_current]
    min = { value = "0.000", unit = "mA" }
    max = { value = "20.000", unit = "mA" }
    [red_led.accepted_temperature]
    min = { value = "15.0", unit = "C" }
    max = { value = "45.0", unit = "C" }
    [blue_led.accepted_voltage]
    min = { value = "0.000", unit = "V" }
    max = { value = "3.300", unit = "V" }
    [blue_led.accepted_current]
    min = { value = "0.000", unit = "A" }
    max = { value = "0.050", unit = "A" }
    [blue_led.accepted_temperature]
    min = { value = "288.15", unit = "K" }
    max = { value = "318.15", unit = "K" }
    [comms]
    uart_baud_rate = { value = "9600", unit = "Bd" }
    sensor_poll_rate = { value = "500", unit = "Hz" }
    """
    _assert_toml_string_raises(broken, match="exceeds maximum")


def test_unknown_top_level_section_is_rejected() -> None:
    broken = """
    [red_ld.accepted_voltage]
    min = { value = "-1.000", unit = "mV" }
    max = { value = "1.000", unit = "mV" }
    """
    _assert_toml_string_raises(broken, match="unknown top-level section")


def _assert_toml_string_raises(toml_text: str, *, match: str) -> None:
    import tempfile  # noqa: PLC0415 -- test-only, keeps the fixture inline with the test

    with tempfile.NamedTemporaryFile("w", suffix=".toml", delete=False) as handle:
        handle.write(toml_text)
        temp_path = Path(handle.name)
    try:
        with pytest.raises(ConfigError, match=match):
            load_device_config(temp_path)
    finally:
        temp_path.unlink()
