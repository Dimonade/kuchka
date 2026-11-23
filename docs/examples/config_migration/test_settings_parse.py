"""Tests for settings_parse.py, rung 3: what only this rung does."""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import pytest
import settings_parse

from kuchka import Volt

MODERN = (HERE / "config_modern.toml").read_text(encoding="utf-8")


@pytest.mark.parametrize(
    ("old", "new", "message"),
    [
        (
            'minimum = "-1 mV"',
            'minimum = "-1 mA"',
            "red_led.accepted_voltage.minimum: 'mA' is not a unit of Voltage",
        ),
        (
            'minimum = "-1 mV"',
            "minimum = -1.0",
            "red_led.accepted_voltage.minimum: expected a number and its unit as text",
        ),
        (
            'maximum = "20 mA"',
            'maximum = "0.5 A"',
            "red_led.accepted_current.maximum: 0.5 A is above 100 mA",
        ),
        (
            'minimum = "15 °C"\nmaximum = "45 °C"',
            'minimum = "45 °C"\nmaximum = "15 °C"',
            "red_led.accepted_temperature: no measurement is at least 45 °C",
        ),
        ('maximum = "20 mA"\n', "", "red_led.accepted_current.maximum: missing"),
        ("[comms]\n", '[comms]\nparity = "none"\n', "comms: unknown key(s) parity"),
    ],
)
def test_the_message_names_the_key_and_says_why(
    old: str, new: str, message: str
) -> None:
    with pytest.raises(settings_parse.ConfigError) as raised:
        settings_parse.loads(MODERN.replace(old, new, 1))
    assert message in str(raised.value)


def test_a_section_that_is_no_table_is_refused() -> None:
    text = "comms = 5\n" + MODERN.split("[comms]")[0]
    with pytest.raises(settings_parse.ConfigError, match="comms: expected a table"):
        settings_parse.loads(text)


def test_the_swap_cannot_be_constructed_at_all() -> None:
    with pytest.raises(ValueError, match="no measurement is at least 3 V"):
        settings_parse.VoltageWindow(minimum=Volt(3), maximum=Volt(1))
