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


@pytest.mark.parametrize(
    ("old", "new", "match"),
    [
        ('min = "-1.000 mV"', 'min = "-1.000 mA"', "'mA' is not a unit of Voltage"),
        ('min = "-1.000 mV"', 'min = "-1.000 dBm"', "'dBm' is not a unit of Voltage"),
        ('min = "-1.000 mV"', "min = -1.0", "expected a number with its unit as text"),
        ('min = "-1.000 mV"', 'min = "-1.000"', "red_led.accepted_voltage.min"),
        ('max = "20.000 mA"', 'max = "-20.000 mA"', "exceeds maximum"),
        ("[red_led.accepted_current]", "[red_led.accepted_curent]", "missing"),
        ("[red_led.", "[red_ld.", "unknown top-level section"),
    ],
)
def test_a_broken_config_fails_at_load_naming_the_field(
    tmp_path: Path, old: str, new: str, match: str
) -> None:
    path = tmp_path / "config.toml"
    path.write_text(
        CONFIG_PATH.read_text(encoding="utf-8").replace(old, new, 1), encoding="utf-8"
    )
    with pytest.raises(ConfigError, match=match):
        load_device_config(path)
