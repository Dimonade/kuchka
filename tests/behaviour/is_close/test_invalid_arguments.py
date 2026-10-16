"""`is_close` refuses invalid tolerances for every shape."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any

import pytest

from kuchka import IncompatibleDimensionError
from kuchka import InvalidMeasurementError
from kuchka.units import angular
from kuchka.units import logarithmic
from kuchka.units import resistance
from kuchka.units import thermal
from kuchka.units import voltage


@dataclass(frozen=True)
class Shape:
    """One reading of each quantity shape, with the arguments `is_close` rejects."""

    id: str
    reading: Any
    other: Any
    tolerance: Any
    negative: Any
    alien: Any


READINGS = [
    Shape(
        "linear",
        voltage.Volt(1),
        voltage.Volt(2),
        voltage.Volt(1),
        voltage.Volt(-1),
        resistance.Ohm(1),
    ),
    Shape(
        "affine",
        thermal.Celsius(1),
        thermal.Celsius(2),
        thermal.DeltaCelsius(1),
        thermal.DeltaCelsius(-1),
        voltage.Volt(1),
    ),
    Shape(
        "logarithmic",
        logarithmic.Decibel(1),
        logarithmic.Decibel(2),
        logarithmic.Decibel(1),
        logarithmic.Decibel(-1),
        voltage.Volt(1),
    ),
    Shape(
        "modular",
        angular.Degree(1),
        angular.Degree(2),
        angular.Degree(1),
        angular.Degree(-1),
        voltage.Volt(1),
    ),
]
READING_IDS = [shape.id for shape in READINGS]


@pytest.mark.parametrize("shape", READINGS, ids=READING_IDS)
def test_a_negative_tolerance_is_rejected(shape: Shape) -> None:
    with pytest.raises(InvalidMeasurementError, match="must not be negative"):
        shape.reading.is_close(shape.other, tolerance=shape.negative)


@pytest.mark.parametrize("shape", READINGS, ids=READING_IDS)
def test_a_plain_number_is_not_a_tolerance(shape: Shape) -> None:
    with pytest.raises(InvalidMeasurementError, match="must be a"):
        shape.reading.is_close(shape.other, tolerance=0.5)


@pytest.mark.parametrize("shape", READINGS, ids=READING_IDS)
def test_a_tolerance_of_another_type_is_rejected(shape: Shape) -> None:
    with pytest.raises(InvalidMeasurementError, match="must be a"):
        shape.reading.is_close(shape.other, tolerance=shape.alien)


@pytest.mark.parametrize("shape", READINGS, ids=READING_IDS)
def test_another_quantity_type_is_rejected_as_the_other_reading(shape: Shape) -> None:
    with pytest.raises(IncompatibleDimensionError):
        shape.reading.is_close(shape.alien, tolerance=shape.tolerance)


@pytest.mark.parametrize("shape", READINGS, ids=READING_IDS)
def test_the_tolerance_has_no_default(shape: Shape) -> None:
    with pytest.raises(TypeError):
        shape.reading.is_close(shape.other)


@pytest.mark.parametrize("shape", READINGS, ids=READING_IDS)
def test_the_tolerance_is_keyword_only(shape: Shape) -> None:
    with pytest.raises(TypeError):
        shape.reading.is_close(shape.other, shape.tolerance)


@pytest.mark.parametrize("shape", READINGS, ids=READING_IDS)
def test_a_zero_tolerance_accepts_only_equal_readings(shape: Shape) -> None:
    zero = type(shape.tolerance)(Fraction(0), shape.tolerance.unit)
    assert shape.reading.is_close(shape.reading, tolerance=zero)
    assert not shape.reading.is_close(shape.other, tolerance=zero)
