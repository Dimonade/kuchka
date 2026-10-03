"""`is_close`: whether two readings are within a stated tolerance of each other.

Equality is exact, so a reading that carries floating-point error never equals its
ideal value.
`is_close` takes the tolerance as a quantity and has no default, so what counts as
close is always written down by the caller.
The tolerance is whatever a difference of two readings is: the same type for linear,
logarithmic, and modular quantities, the delta type for affine ones (`Temperature` by
`TemperatureDelta`, `Instant` by `Time`).
The comparison is exact and inclusive, and a modular quantity measures the distance
the short way round its circle.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

import pytest

from kuchka import ArcSecond
from kuchka import Baud
from kuchka import Bel
from kuchka import Celsius
from kuchka import Decibel
from kuchka import Degree
from kuchka import DeltaCelsius
from kuchka import DeltaKelvin
from kuchka import Hertz
from kuchka import IncompatibleDimensionError
from kuchka import InvalidMeasurementError
from kuchka import Kelvin
from kuchka import Kilometre
from kuchka import Metre
from kuchka import Millimetre
from kuchka import Millisecond
from kuchka import Millivolt
from kuchka import Ohm
from kuchka import Radian
from kuchka import Turn
from kuchka import Volt
from kuchka.units import INSTANT_UNITS

# Linear: Voltage, Length, Frequency, ...


def test_linear_readings_within_the_tolerance_are_close() -> None:
    assert Volt(1).is_close(Volt(1.0004), tolerance=Millivolt(1))


def test_linear_readings_outside_the_tolerance_are_not_close() -> None:
    assert not Volt(1).is_close(Volt(1.01), tolerance=Millivolt(1))


def test_the_tolerance_boundary_is_inclusive_and_exact() -> None:
    assert Metre(1).is_close(Metre(1.001), tolerance=Millimetre(1))
    assert not Metre(1).is_close(Metre(1.0010000000000001), tolerance=Millimetre(1))


def test_linear_readings_in_different_units_compare_by_value() -> None:
    assert Kilometre(1).is_close(Metre(1000.4), tolerance=Metre(0.5))


def test_the_float_sum_is_close_to_its_ideal_value_but_not_equal() -> None:
    reading = Volt(0.1 + 0.2)
    assert reading != Volt(0.3)
    assert reading.is_close(Volt(0.3), tolerance=Volt(1e-12))


def test_linear_closeness_is_symmetric() -> None:
    a, b, tolerance = Volt(1), Volt(1.5), Volt(0.5)
    assert a.is_close(b, tolerance=tolerance) is b.is_close(a, tolerance=tolerance)


def test_a_zero_tolerance_means_exactly_equal() -> None:
    assert Volt(1).is_close(Millivolt(1000), tolerance=Volt(0))
    assert not Volt(0.1 + 0.2).is_close(Volt(0.3), tolerance=Volt(0))


def test_closeness_is_not_transitive() -> None:
    a, b, c, tolerance = Volt(0), Volt(0.8), Volt(1.6), Volt(1)
    assert a.is_close(b, tolerance=tolerance)
    assert b.is_close(c, tolerance=tolerance)
    assert not a.is_close(c, tolerance=tolerance)


def test_two_types_that_share_a_dimension_are_not_comparable() -> None:
    with pytest.raises(IncompatibleDimensionError):
        Hertz(1).is_close(Baud(1), tolerance=Hertz(1))  # type: ignore[arg-type]


# Affine: Temperature, Instant.


def test_temperatures_are_close_across_scales() -> None:
    assert Celsius(20).is_close(Kelvin(293.1500001), tolerance=DeltaKelvin(0.001))


def test_the_temperature_tolerance_is_a_temperature_delta() -> None:
    assert Celsius(20).is_close(Celsius(20.4), tolerance=DeltaCelsius(0.5))
    assert not Celsius(20).is_close(Celsius(20.6), tolerance=DeltaCelsius(0.5))


def test_a_temperature_is_not_a_valid_tolerance() -> None:
    with pytest.raises(InvalidMeasurementError, match="TemperatureDelta"):
        Celsius(20).is_close(Celsius(20), tolerance=Celsius(1))  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_instants_are_close_within_a_time_tolerance() -> None:
    first = INSTANT_UNITS["s"](1_700_000_000)
    second = INSTANT_UNITS["s"](1_700_000_000.0004)
    assert first.is_close(second, tolerance=Millisecond(1))
    assert not first.is_close(second, tolerance=Millisecond(0.3))


def test_an_instant_is_not_a_valid_tolerance() -> None:
    first = INSTANT_UNITS["s"](5)
    with pytest.raises(InvalidMeasurementError, match="Time"):
        first.is_close(first, tolerance=first)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


# Logarithmic: LogarithmicRatio.


def test_levels_within_the_tolerance_are_close() -> None:
    assert Decibel(3.0).is_close(Decibel(3.04), tolerance=Decibel(0.05))
    assert not Decibel(3.0).is_close(Decibel(3.06), tolerance=Decibel(0.05))


def test_levels_compare_across_units() -> None:
    assert Decibel(10).is_close(Bel(1), tolerance=Decibel(0))


# Modular: Angle.


@pytest.mark.parametrize(
    ("degrees", "radians"),
    [
        (90, math.pi / 2),
        (45, math.pi / 4),
        (60, math.pi / 3),
        (30, math.pi / 6),
        (180, math.pi),
        (360, 2 * math.pi),
    ],
    ids=["90", "45", "60", "30", "180", "360"],
)
def test_float_radians_are_close_to_the_matching_degrees(
    degrees: int, radians: float
) -> None:
    assert Degree(degrees).is_close(Radian(radians), tolerance=Radian(1e-15))


def test_the_angle_tolerance_may_be_written_in_any_angular_unit() -> None:
    reading = Radian(math.pi / 2)
    assert Degree(90).is_close(reading, tolerance=ArcSecond(1e-9))
    assert Degree(90).is_close(reading, tolerance=Turn(1e-12))


def test_angles_either_side_of_the_wrap_point_are_close() -> None:
    assert Degree(359.9999).is_close(Degree(0.0001), tolerance=Degree(0.001))
    assert Degree(0.0001).is_close(Degree(359.9999), tolerance=Degree(0.001))


def test_unnormalised_angles_are_compared_by_position() -> None:
    assert Degree(370).is_close(Degree(10), tolerance=Degree(0))


def test_an_angle_tolerance_of_half_a_turn_accepts_everything() -> None:
    assert Degree(0).is_close(Degree(180), tolerance=Degree(180))
    assert Degree(0).is_close(Degree(123), tolerance=Turn(1))


def test_angle_closeness_is_symmetric() -> None:
    a, b, tolerance = Degree(10), Degree(350), Degree(20)
    assert a.is_close(b, tolerance=tolerance) is b.is_close(a, tolerance=tolerance)


# Invalid arguments, every shape.


@dataclass(frozen=True)
class Shape:
    """One reading of each quantity shape, with the arguments `is_close` rejects."""

    id: str
    reading: Any
    other: Any
    tolerance: Any
    negative: Any
    alien: Any


SHAPES = [
    Shape("linear", Volt(1), Volt(2), Volt(1), Volt(-1), Ohm(1)),
    Shape("affine", Celsius(1), Celsius(2), DeltaCelsius(1), DeltaCelsius(-1), Volt(1)),
    Shape("logarithmic", Decibel(1), Decibel(2), Decibel(1), Decibel(-1), Volt(1)),
    Shape("modular", Degree(1), Degree(2), Degree(1), Degree(-1), Volt(1)),
]
SHAPE_IDS = [shape.id for shape in SHAPES]


@pytest.mark.parametrize("shape", SHAPES, ids=SHAPE_IDS)
def test_a_negative_tolerance_is_rejected(shape: Shape) -> None:
    with pytest.raises(InvalidMeasurementError, match="must not be negative"):
        shape.reading.is_close(shape.other, tolerance=shape.negative)


@pytest.mark.parametrize("shape", SHAPES, ids=SHAPE_IDS)
def test_a_plain_number_is_not_a_tolerance(shape: Shape) -> None:
    with pytest.raises(InvalidMeasurementError, match="must be a"):
        shape.reading.is_close(shape.other, tolerance=0.5)


@pytest.mark.parametrize("shape", SHAPES, ids=SHAPE_IDS)
def test_a_tolerance_of_another_type_is_rejected(shape: Shape) -> None:
    with pytest.raises(InvalidMeasurementError, match="must be a"):
        shape.reading.is_close(shape.other, tolerance=shape.alien)


@pytest.mark.parametrize("shape", SHAPES, ids=SHAPE_IDS)
def test_another_quantity_type_is_rejected_as_the_other_reading(shape: Shape) -> None:
    with pytest.raises(IncompatibleDimensionError):
        shape.reading.is_close(shape.alien, tolerance=shape.tolerance)


@pytest.mark.parametrize("shape", SHAPES, ids=SHAPE_IDS)
def test_the_tolerance_has_no_default(shape: Shape) -> None:
    with pytest.raises(TypeError):
        shape.reading.is_close(shape.other)


@pytest.mark.parametrize("shape", SHAPES, ids=SHAPE_IDS)
def test_the_tolerance_is_keyword_only(shape: Shape) -> None:
    with pytest.raises(TypeError):
        shape.reading.is_close(shape.other, shape.tolerance)


@pytest.mark.parametrize("shape", SHAPES, ids=SHAPE_IDS)
def test_a_zero_tolerance_accepts_only_equal_readings(shape: Shape) -> None:
    zero = type(shape.tolerance)(Fraction(0), shape.tolerance.unit)
    assert shape.reading.is_close(shape.reading, tolerance=zero)
    assert not shape.reading.is_close(shape.other, tolerance=zero)
