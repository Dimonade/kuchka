"""A unit that is no unit of a quantity is refused, wherever a unit is taken.

`value_in` once did the division and returned a number for any unit at all, so
`Millivolt(2800).value_in(AMPERE)` was `14/5`: a voltage expressed in amperes.
`to` and `value_in` take a unit, and a quantity has the same answer for both: a unit of
its own kind, or `InvalidConversionError`, and nothing else, whatever the shape.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import Ampere
from kuchka import Celsius
from kuchka import Decibel
from kuchka import Degree
from kuchka import InvalidConversionError
from kuchka import Millivolt
from kuchka import Volt
from kuchka.units import AMPERE
from kuchka.units import KELVIN
from kuchka.units import KILOGRAM
from kuchka.units.electromagnetics.voltage import MILLIVOLT
from kuchka.units.electromagnetics.voltage import VOLT
from tests.support.kinds import UNIT_TABLES


class Dinosaur:
    """Nothing a quantity should take for a unit."""


NONSENSE = {
    "an integer": 5,
    "a string": "mV",
    "None": None,
    "a dinosaur": Dinosaur(),
    "a class": Millivolt,
    "a quantity": Volt(1),
    "a list": [MILLIVOLT],
}

SAMPLES = {name: next(iter(table.values()))(1) for name, table in UNIT_TABLES.items()}
EVERY_UNIT = [unit for table in UNIT_TABLES.values() for unit in table.units]


def test_the_voltage_in_amperes_is_refused_and_not_fourteen_fifths() -> None:
    with pytest.raises(InvalidConversionError, match="incompatible dimensions"):
        Millivolt(2800).value_in(AMPERE)
    with pytest.raises(InvalidConversionError, match="incompatible dimensions"):
        Millivolt(2800).to(AMPERE)


@pytest.mark.parametrize("name", list(SAMPLES))
@pytest.mark.parametrize("what", list(NONSENSE))
def test_nothing_that_is_no_unit_is_taken_for_one(name: str, what: str) -> None:
    sample = SAMPLES[name]
    for method in (sample.value_in, sample.to):
        with pytest.raises(InvalidConversionError):
            method(NONSENSE[what])  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


@pytest.mark.parametrize("name", list(SAMPLES))
def test_value_in_and_to_agree_on_every_unit_there_is(name: str) -> None:
    sample = SAMPLES[name]
    refused = 0
    for unit in EVERY_UNIT:
        try:
            sample.to(unit)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
        except InvalidConversionError:
            refused += 1
            with pytest.raises(InvalidConversionError):
                sample.value_in(unit)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
        else:
            assert sample.value_in(unit) is not None  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
    assert refused > len(EVERY_UNIT) // 2


@pytest.mark.parametrize(
    ("value", "foreign"),
    [
        (Volt(1), KELVIN),
        (Volt(1), KILOGRAM),
        (Ampere(1), VOLT),
        (Celsius(20), VOLT),
        (Degree(90), VOLT),
        (Decibel(3), VOLT),
    ],
)
def test_every_shape_refuses_a_unit_of_another_dimension(
    value: object, foreign: object
) -> None:
    with pytest.raises(InvalidConversionError):
        value.value_in(foreign)  # type: ignore[attr-defined]  # ty: ignore[unresolved-attribute]


def test_the_units_a_quantity_does_take_are_still_taken() -> None:
    assert Millivolt(2800).value_in(VOLT) == Fraction(14, 5)
    assert Millivolt(2800).value_in(MILLIVOLT) == Fraction(2800)
    assert Celsius(20).value_in(Celsius(0).unit) == Fraction(20)
