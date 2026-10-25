"""A type accepts the display units of its own shape and dimension, and no others.

A linear type takes linear units, an absolute temperature or an instant takes affine
units, an angle takes angular units, a logarithmic ratio takes levels, and a proportion
takes dimensionless units.
Each shape refuses the units of the others, and a unit of another dimension.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import Angle
from kuchka import Instant
from kuchka import InvalidMeasurementError
from kuchka import LogarithmicRatio
from kuchka import Proportion
from kuchka import Temperature
from kuchka.units import angular
from kuchka.units import current
from kuchka.units import logarithmic
from kuchka.units import proportion
from kuchka.units import thermal
from kuchka.units import thermal as thermal_units
from kuchka.units.electromagnetics import voltage
from kuchka.units.temporal import instant

ACCEPTED_UNITS = (
    (Temperature, (thermal.KELVIN, thermal.CELSIUS)),
    (Instant, (instant.INSTANT_SECOND,)),
    (Angle, (angular.RADIAN, angular.DEGREE)),
    (LogarithmicRatio, (logarithmic.DECIBEL,)),
    (Proportion, (proportion.RATIO, proportion.PERCENT)),
)
ACCEPTED_UNITS_UNIT_IDS = [cls.__name__ for cls, _ in ACCEPTED_UNITS]
REFUSED = (
    (Temperature, (voltage.VOLT, None, "K"), "display unit"),
    (Instant, (voltage.VOLT,), "display unit"),
    (Angle, (thermal.KELVIN,), "display unit"),
    (Angle, (voltage.VOLT,), "incompatible dimensions"),
    (
        LogarithmicRatio,
        (proportion.RATIO, voltage.VOLT, thermal.KELVIN),
        "display unit",
    ),
    (Proportion, (voltage.VOLT,), "incompatible dimensions"),
    (Proportion, (current.AMPERE,), "incompatible dimensions"),
)
REFUSED_IDS = [f"{cls.__name__}-{match}" for cls, _, match in REFUSED]


@pytest.mark.parametrize(("cls", "units"), ACCEPTED_UNITS, ids=ACCEPTED_UNITS_UNIT_IDS)
def test_a_type_accepts_the_units_of_its_shape(cls: type, units: tuple) -> None:
    for unit in units:
        assert cls(Fraction(1), unit).unit is unit


@pytest.mark.parametrize(("cls", "units", "match"), REFUSED, ids=REFUSED_IDS)
def test_a_type_refuses_the_units_of_other_shapes_and_dimensions(
    cls: type, units: tuple, match: str
) -> None:
    for unit in units:
        with pytest.raises(InvalidMeasurementError, match=match):
            cls(Fraction(1), unit)


def test_a_linear_unit_that_is_a_ratio_is_not_a_level() -> None:
    with pytest.raises(InvalidMeasurementError, match="display unit"):
        LogarithmicRatio(Fraction(1), proportion.RATIO)


def test_the_type_of_a_magnitude_is_checked_before_absolute_zero() -> None:
    with pytest.raises(InvalidMeasurementError, match="unit constructors"):
        Temperature(-1, thermal.KELVIN)  # type: ignore[arg-type]


def test_a_temperature_below_absolute_zero_is_rejected_by_both_constructors() -> None:
    with pytest.raises(InvalidMeasurementError, match="absolute zero"):
        Temperature(Fraction(-1), thermal.KELVIN)
    with pytest.raises(InvalidMeasurementError, match="absolute zero"):
        thermal_units.Celsius(-300)
