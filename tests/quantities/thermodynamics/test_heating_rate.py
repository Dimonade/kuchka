"""HeatingRate: its units and the arithmetic with temperature differences and time.

The generic contracts (arithmetic, conversion, formatting, spellings) run for every
unit of the table; this module covers what is specific to a heating rate.
"""

from __future__ import annotations

from decimal import Decimal

import pytest

from kuchka import HeatingRate
from kuchka import TemperatureDelta
from kuchka import parse
from kuchka.units import temporal
from kuchka.units import thermal
from kuchka.units.thermodynamics import heating_rate as hr


def test_a_degree_celsius_per_minute_is_exactly_a_kelvin_per_minute() -> None:
    assert hr.CelsiusPerMinute(5) == hr.KelvinPerMinute(5)
    assert hr.CelsiusPerMinute(5) == hr.CelsiusPerHour(300)


def test_a_degree_fahrenheit_is_five_ninths_of_a_degree_celsius_per_time() -> None:
    assert hr.FahrenheitPerMinute(9) == hr.CelsiusPerMinute(5)
    assert hr.FahrenheitPerSecond(9) == hr.CelsiusPerSecond(5)


def test_a_temperature_difference_over_a_time_is_a_heating_rate() -> None:
    rate = thermal.DeltaKelvin(60) / temporal.Minute(2)
    assert type(rate) is HeatingRate
    assert rate == hr.KelvinPerMinute(30)


def test_a_heating_rate_over_a_time_is_a_temperature_difference() -> None:
    warmed = hr.CelsiusPerMinute(5) * temporal.Minute(12)
    assert type(warmed) is TemperatureDelta
    assert warmed == thermal.DeltaCelsius(60)


def test_a_difference_times_a_frequency_is_a_heating_rate() -> None:
    assert thermal.DeltaKelvin(3) * temporal.Hertz(2) == hr.KelvinPerSecond(6)


def test_a_falling_temperature_is_a_negative_heating_rate() -> None:
    cooling = (thermal.Celsius(20) - thermal.Celsius(80)) / temporal.Minute(10)
    assert cooling == hr.CelsiusPerMinute(-6)


def test_a_reading_is_not_a_difference_so_it_does_not_divide_by_a_time() -> None:
    with pytest.raises(TypeError):
        thermal.Celsius(20) / temporal.Second(1)  # type: ignore[operator]


def test_text_resolves_through_the_table() -> None:
    assert parse("5 °C/min", HeatingRate) == hr.CelsiusPerMinute(5)
    assert parse("5 degrees C per minute", HeatingRate) == hr.CelsiusPerMinute(5)
    assert parse("0.2 K/s", HeatingRate) == hr.KelvinPerSecond(Decimal("0.2"))
