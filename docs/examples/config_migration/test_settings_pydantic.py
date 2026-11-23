"""Tests for settings_pydantic.py, rung 1: what only this rung does."""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import pytest

pytest.importorskip("pydantic")

import settings_pydantic
from mistakes import TEMPERATURE
from mistakes import swap_values
from pydantic import ValidationError

MODERN = (HERE / "config_modern.toml").read_text(encoding="utf-8")


def test_every_mistake_in_the_file_is_reported_at_once() -> None:
    text = MODERN.replace('minimum = "-1 mV"', 'minimum = "-1 mA"')
    text = text.replace('uart_baud_rate = "9600 Bd"', 'uart_baud_rate = "9600 V"')
    with pytest.raises(ValidationError) as raised:
        settings_pydantic.loads(text)
    places = {".".join(str(part) for part in e["loc"]) for e in raised.value.errors()}
    assert places == {"red_led.accepted_voltage.minimum", "comms.uart_baud_rate"}


def test_each_error_names_the_path_and_says_why() -> None:
    text = MODERN.replace('maximum = "20 mA"', 'maximum = "0.5 A"')
    with pytest.raises(ValidationError) as raised:
        settings_pydantic.loads(text)
    (error,) = raised.value.errors()
    assert error["loc"] == ("red_led", "accepted_current", "maximum")
    assert error["msg"] == "Value error, 0.5 A is above 100 mA, the most allowed."


def test_the_swapped_range_is_reported_at_the_window() -> None:
    text = swap_values(MODERN, TEMPERATURE, "minimum", "maximum")
    with pytest.raises(ValidationError) as raised:
        settings_pydantic.loads(text)
    (error,) = raised.value.errors()
    assert error["loc"] == ("red_led", "accepted_temperature")
    assert "no measurement is at least 45 °C and at most 15 °C" in error["msg"]


def test_the_configuration_is_frozen() -> None:
    config = settings_pydantic.loads(MODERN)
    with pytest.raises(ValidationError, match="frozen"):
        config.red_led = config.blue_led  # type: ignore[misc]
