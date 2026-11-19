"""`auto_scale` shows a measurement in the unit of its ladder that suits its size.

Each case writes out the unit it expects, since the equality of the result with the
measurement it came from holds whichever unit was picked.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka.units import angular
from kuchka.units import current
from kuchka.units import logarithmic
from kuchka.units import temporal
from kuchka.units import thermal
from kuchka.units.electromagnetics import voltage


@pytest.mark.parametrize(
    ("measurement", "unit", "text"),
    [
        (current.Ampere(0.000045), current.MICROAMPERE, "45 µA"),
        (current.Ampere(0.5), current.MILLIAMPERE, "500 mA"),
        (current.Milliampere(1000), current.AMPERE, "1 A"),
        (current.Milliampere(999.999), current.MILLIAMPERE, "999.999 mA"),
        (current.Microampere(2_500_000), current.AMPERE, "2.5 A"),
        (current.Ampere(12_000), current.KILOAMPERE, "12 kA"),
        (voltage.Volt(-0.025), voltage.MILLIVOLT, "-25 mV"),
        (voltage.Millivolt(-0.5), voltage.MICROVOLT, "-500 µV"),
        (temporal.Hertz(2_400_000_000), temporal.GIGAHERTZ, "2.4 GHz"),
        (temporal.Kilohertz(0.5), temporal.HERTZ, "500 Hz"),
        (thermal.Kelvin(0.005), thermal.MILLIKELVIN, "5 mK"),
        (thermal.Microkelvin(1500), thermal.MILLIKELVIN, "1.5 mK"),
        (thermal.DeltaKelvin(0.002), thermal.DELTA_MILLIKELVIN, "2 ΔmK"),
        (thermal.DeltaCelsius(0.002), thermal.DELTA_MILLICELSIUS, "2 Δm°C"),
    ],
)
def test_the_largest_unit_that_the_size_reaches_is_picked(
    measurement, unit, text: str
) -> None:
    scaled = measurement.auto_scale()
    assert scaled.unit == unit
    assert scaled == measurement
    assert str(scaled) == text


def test_the_scaled_measurement_formats_like_any_other() -> None:
    assert f"{temporal.Hertz(2_400_000_000).auto_scale():.1f}" == "2.4 GHz"
    assert f"{current.Ampere(0.000045).auto_scale():.2f}" == "45.00 µA"


@pytest.mark.parametrize(
    ("measurement", "unit"),
    [
        (current.Ampere(1e-15), current.PICOAMPERE),
        (current.Ampere(5e9), current.MEGAAMPERE),
        (temporal.Hertz(1e-12), temporal.NANOHERTZ),
        (temporal.Hertz(5e18), temporal.PETAHERTZ),
    ],
)
def test_a_size_past_the_ends_of_the_ladder_takes_the_end_unit(
    measurement, unit
) -> None:
    assert measurement.auto_scale().unit == unit


def test_a_negative_value_is_picked_by_its_size() -> None:
    assert voltage.Volt(-0.025).auto_scale().unit == voltage.MILLIVOLT
    assert voltage.Volt(-5000).auto_scale().unit == voltage.KILOVOLT


@pytest.mark.parametrize("unit", [voltage.VOLT, voltage.MILLIVOLT, voltage.MEGAVOLT])
def test_zero_keeps_the_unit_it_has(unit) -> None:
    zero = voltage.Volt(0).to(unit)
    assert zero.auto_scale() is zero
    assert zero.auto_scale().unit == unit


def test_a_measurement_already_in_the_unit_it_would_get_is_returned_itself() -> None:
    reading = current.Milliampere(5)
    assert reading.auto_scale() is reading


def test_a_measurement_in_any_unit_of_the_ladder_reaches_the_same_unit() -> None:
    expected = current.Ampere(0.000045).auto_scale().unit
    for unit in current.CURRENT_LADDERS[0]:
        assert current.Ampere(0.000045).to(unit).auto_scale().unit == expected


def test_an_exact_fraction_stays_exact() -> None:
    third = current.Ampere(Fraction(1, 3)).auto_scale()
    assert third.unit == current.MILLIAMPERE
    assert third.value_in(current.MILLIAMPERE) == Fraction(1000, 3)


@pytest.mark.parametrize(
    "measurement",
    [
        thermal.Celsius(0.5),
        thermal.Celsius(0.001),
        thermal.Celsius(25),
        thermal.Fahrenheit(0.5),
        thermal.Millicelsius(500),
        thermal.Rankine(0.5),
        thermal.DeltaFahrenheit(0.002),
    ],
    ids=str,
)
def test_a_unit_that_starts_away_from_zero_keeps_its_measurement(measurement) -> None:
    assert measurement.auto_scale() is measurement


@pytest.mark.parametrize(
    "measurement",
    [angular.Degree(350), angular.Turn(0.0004), logarithmic.Decibel(20)],
    ids=str,
)
def test_a_shape_whose_magnitude_is_no_size_keeps_its_measurement(measurement) -> None:
    assert measurement.auto_scale() is measurement


def test_a_value_just_under_a_step_rounds_up_to_the_step_when_shown() -> None:
    scaled = current.Milliampere(0.9999999).auto_scale()
    assert scaled.unit == current.MICROAMPERE
    assert f"{scaled:.1f}" == "1000.0 µA"
