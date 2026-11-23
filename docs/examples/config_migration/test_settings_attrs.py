"""Tests for settings_attrs.py, rung 2: what only this rung does."""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import pytest

pytest.importorskip("attrs")

import attrs
import settings_attrs

from kuchka import BoundsError
from kuchka import Milliampere
from kuchka import Millivolt
from kuchka import ParseError
from kuchka import UnknownUnitError

MODERN = (HERE / "config_modern.toml").read_text(encoding="utf-8")


def test_the_first_mistake_stops_the_load_with_the_kuchka_error() -> None:
    with pytest.raises(UnknownUnitError):
        settings_attrs.loads(
            MODERN.replace('minimum = "-1 mV"', 'minimum = "-1 mA"', 1)
        )
    with pytest.raises(ParseError, match="has no unit"):
        settings_attrs.loads(MODERN.replace('minimum = "-1 mV"', "minimum = -1.0", 1))


def test_a_bound_error_names_the_attribute() -> None:
    text = MODERN.replace('maximum = "20 mA"', 'maximum = "0.5 A"')
    with pytest.raises(BoundsError) as raised:
        settings_attrs.loads(text)
    assert str(raised.value) == "maximum: 0.5 A is above 100 mA, the most allowed."


def test_the_classes_are_frozen_and_hold_the_quantities() -> None:
    config = settings_attrs.loads(MODERN)
    assert config.red_led.accepted_voltage.minimum == Millivolt(-1)
    with pytest.raises(attrs.exceptions.FrozenInstanceError):
        config.comms = config.comms  # type: ignore[misc]


def test_an_instance_is_kept_and_a_table_is_built() -> None:
    window = settings_attrs.VoltageWindow("-1 mV", "1 mV")
    limits = settings_attrs.LedLimits(
        accepted_voltage=window,
        accepted_current={"minimum": "0 mA", "maximum": "20 mA"},
        accepted_temperature={"minimum": "15 °C", "maximum": "45 °C"},
    )
    assert limits.accepted_voltage is window
    assert limits.accepted_current.maximum == Milliampere(20)
