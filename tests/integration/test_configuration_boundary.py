"""Quantities cross a text boundary: read, computed with, stored, and read back.

A device is described by text that people write: `"3 kW"`, `"3000 rpm"`, `"50 Hz"`.
The `*_UNITS` tables turn the unit part into a constructor, the values are computed with
exactly, and the stored form carries each result as exact text and a unit symbol.
"""

from __future__ import annotations

import json
from fractions import Fraction

import pytest

from kuchka import Energy
from kuchka import Torque
from kuchka.units import temporal
from kuchka.units.kinematics import angular_velocity
from kuchka.units.mechanics import energy
from kuchka.units.mechanics import power
from kuchka.units.mechanics import torque
from kuchka.units.temporal import frequency

CONFIGURATION = json.loads(
    '{"rating": "3 kW", "speed": "3000 rpm", "supply": "50 Hz", "shift": "8 h"}'
)


def read(table, text: str):
    """Parse `"<number> <unit>"` through a table of unit constructors."""
    number, unit = text.split(maxsplit=1)
    return table[unit](Fraction(number))


def test_each_field_reads_through_its_own_table() -> None:
    rating = read(power.POWER_UNITS, CONFIGURATION["rating"])
    speed = read(angular_velocity.ANGULAR_VELOCITY_UNITS, CONFIGURATION["speed"])
    supply = read(frequency.FREQUENCY_UNITS, CONFIGURATION["supply"])
    assert rating == power.Kilowatt(3)
    assert speed == angular_velocity.RevolutionPerMinute(3000)
    assert supply == frequency.Hertz(50)


def test_a_unit_of_another_quantity_is_refused_at_the_boundary() -> None:
    with pytest.raises(KeyError):
        read(power.POWER_UNITS, "3 rpm")
    with pytest.raises(KeyError):
        read(angular_velocity.ANGULAR_VELOCITY_UNITS, "3 kW")


def test_the_configured_values_compute_to_the_expected_torque_and_energy() -> None:
    rating = read(power.POWER_UNITS, CONFIGURATION["rating"])
    speed = read(angular_velocity.ANGULAR_VELOCITY_UNITS, CONFIGURATION["speed"])
    shift = read(temporal.TIME_UNITS, CONFIGURATION["shift"])
    shaft = rating / speed
    assert type(shaft) is Torque
    assert shaft * speed == rating
    assert type(rating * shift) is Energy
    assert rating * shift == energy.KilowattHour(24)


def test_the_supply_frequency_and_the_shaft_speed_are_consistent() -> None:
    speed = read(angular_velocity.ANGULAR_VELOCITY_UNITS, CONFIGURATION["speed"])
    supply = read(frequency.FREQUENCY_UNITS, CONFIGURATION["supply"])
    assert speed.to_frequency() == supply


def test_a_result_is_stored_as_text_and_comes_back_equal() -> None:
    shaft = read(power.POWER_UNITS, "3 kW") / read(
        angular_velocity.ANGULAR_VELOCITY_UNITS, "3000 rpm"
    )
    shown = shaft.to(torque.NEWTON_METRE)
    stored = json.dumps(
        {"value": str(shown.value_in(shown.unit)), "unit": shown.unit.symbol}
    )
    loaded = json.loads(stored)
    restored = torque.TORQUE_UNITS[loaded["unit"]](Fraction(loaded["value"]))
    assert restored == shaft
    assert restored.unit is torque.NEWTON_METRE
