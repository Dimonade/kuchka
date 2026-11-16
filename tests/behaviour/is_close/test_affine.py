"""`is_close` on temperatures and instants."""

from __future__ import annotations

import pytest

from kuchka import InvalidMeasurementError
from kuchka.units import thermal
from kuchka.units.temporal import instant
from kuchka.units.temporal import time


def test_temperatures_are_close_across_scales() -> None:
    assert thermal.Celsius(20).is_close(
        thermal.Kelvin(293.1500001), tolerance=thermal.DeltaKelvin(0.001)
    )


def test_the_temperature_tolerance_is_a_temperature_delta() -> None:
    assert thermal.Celsius(20).is_close(
        thermal.Celsius(20.4), tolerance=thermal.DeltaCelsius(0.5)
    )
    assert not thermal.Celsius(20).is_close(
        thermal.Celsius(20.6), tolerance=thermal.DeltaCelsius(0.5)
    )


def test_a_temperature_is_not_a_valid_tolerance() -> None:
    with pytest.raises(InvalidMeasurementError, match="TemperatureDelta"):
        thermal.Celsius(20).is_close(thermal.Celsius(20), tolerance=thermal.Celsius(1))  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_instants_are_close_within_a_time_tolerance() -> None:
    first = instant.INSTANT_UNITS["s"](1_700_000_000)
    second = instant.INSTANT_UNITS["s"](1_700_000_000.0004)
    assert first.is_close(second, tolerance=time.Millisecond(1))
    assert not first.is_close(second, tolerance=time.Millisecond(0.3))


def test_an_instant_is_not_a_valid_tolerance() -> None:
    first = instant.INSTANT_UNITS["s"](5)
    with pytest.raises(InvalidMeasurementError, match="Time"):
        first.is_close(first, tolerance=first)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
