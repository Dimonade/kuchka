"""A unit of one type is refused by a type that shares its dimension.

`Frequency` has the hertz, `BaudRate` the baud, and `SampleRate` the sample per second,
all of dimension time to the minus one.
A unit may belong to several types: the second is a unit of `Time` and of
`SamplingPeriod`.
"""

from fractions import Fraction

import pytest

import kuchka.units as published
from kuchka import BaudRate
from kuchka import Frequency
from kuchka import InvalidConversionError
from kuchka import InvalidMeasurementError
from kuchka import SamplingPeriod
from kuchka import Time
from kuchka.units.electromagnetics import voltage
from kuchka.units.temporal import baud_rate
from kuchka.units.temporal import frequency
from kuchka.units.temporal import instant
from kuchka.units.temporal import sample_rate
from kuchka.units.temporal import time


def test_a_frequency_is_not_displayed_in_baud() -> None:
    with pytest.raises(InvalidConversionError, match="is not a unit of Frequency"):
        frequency.Hertz(1).to(baud_rate.BAUD)


def test_a_frequency_is_not_displayed_in_samples_per_second() -> None:
    with pytest.raises(InvalidConversionError):
        frequency.Hertz(1).to(sample_rate.SAMPLES_PER_SECOND)


def test_a_baud_rate_is_not_displayed_in_hertz() -> None:
    with pytest.raises(InvalidConversionError, match="is not a unit of BaudRate"):
        BaudRate(Fraction(1), baud_rate.BAUD).to(frequency.HERTZ)


def test_the_class_constructor_refuses_a_unit_of_a_sibling_type() -> None:
    with pytest.raises(InvalidMeasurementError, match="is not a unit of Frequency"):
        Frequency(Fraction(1), baud_rate.BAUD)


def test_the_message_names_the_type_the_unit_belongs_to() -> None:
    with pytest.raises(InvalidMeasurementError, match="It is a unit of BaudRate"):
        Frequency(Fraction(1), baud_rate.BAUD)
    with pytest.raises(InvalidConversionError, match="It is a unit of Frequency"):
        BaudRate(Fraction(1), baud_rate.BAUD).to(frequency.HERTZ)


def test_the_conversion_message_names_both_units() -> None:
    with pytest.raises(InvalidConversionError) as caught:
        frequency.Hertz(1).to(baud_rate.BAUD)
    assert "Hz" in str(caught.value)
    assert "Bd" in str(caught.value)


def test_a_unit_that_belongs_to_no_type_names_no_owner() -> None:
    from kuchka.quantities.base import UnitDef

    stray = UnitDef("stray", "st", 1, Frequency.dimension)
    with pytest.raises(InvalidMeasurementError) as caught:
        Frequency(Fraction(1), stray)
    assert str(caught.value) == "stray (st) is not a unit of Frequency."


def test_the_second_is_a_unit_of_time_and_of_sampling_period() -> None:
    assert time.SECOND in Time._applicable_units  # noqa: SLF001
    assert time.SECOND in SamplingPeriod._applicable_units  # noqa: SLF001


def test_a_time_and_a_sampling_period_display_in_milliseconds() -> None:
    assert time.Second(1).to(time.MILLISECOND).value_in(time.MILLISECOND) == Fraction(
        1000
    )
    period = time.Second(1).to_sampling_period()
    assert period.to(time.MILLISECOND).value_in(time.MILLISECOND) == Fraction(1000)


def test_an_instant_displays_only_in_the_instant_second() -> None:
    from kuchka import Instant

    assert Instant._applicable_units == frozenset({instant.INSTANT_SECOND})  # noqa: SLF001


def test_a_unit_of_the_type_converts_as_before() -> None:
    assert voltage.Volt(5).to(published.MILLIVOLT).value_in(published.MILLIVOLT) == 5000  # noqa: PLR2004
    assert (
        frequency.Hertz(1000).to(published.KILOHERTZ).value_in(published.KILOHERTZ) == 1
    )


def test_a_foreign_dimension_still_reports_incompatible_dimensions() -> None:
    with pytest.raises(InvalidMeasurementError, match="incompatible dimensions"):
        Frequency(Fraction(1), voltage.VOLT)
    with pytest.raises(InvalidConversionError, match="incompatible dimensions"):
        frequency.Hertz(1).to(voltage.VOLT)
