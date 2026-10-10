"""Time, Frequency, and the acquisition-domain vocabulary that shares their dimensions.

Covers the registered pair (Time, Frequency) and the domain pair
(SamplingPeriod, SampleRate) and BaudRate: same two dimensions, three different
concepts, and the point of this module is to prove that sharing a dimension is not the
same as being interchangeable.
"""

from decimal import Decimal

import pytest

from kuchka import Baud
from kuchka import ConvertibleToFrequency
from kuchka import Day
from kuchka import Femtosecond
from kuchka import Fortnight
from kuchka import Frequency
from kuchka import Hertz
from kuchka import Hour
from kuchka import IncompatibleDimensionError
from kuchka import InvalidMeasurementError
from kuchka import Jiffy
from kuchka import JulianYear
from kuchka import Kilobaud
from kuchka import Kilohertz
from kuchka import Microsecond
from kuchka import Millisecond
from kuchka import Minute
from kuchka import Nanosecond
from kuchka import Picosecond
from kuchka import SampleRate
from kuchka import SamplesPerSecond
from kuchka import Second
from kuchka import UnrepresentableDimensionError
from kuchka import Volt
from kuchka import Week
from kuchka.units import SECOND


def test_time_addition_and_prefix_conversion():
    assert Second(1) + Millisecond(500) == Second(Decimal("1.5"))


def test_frequency_addition_and_prefix_conversion():
    assert Hertz(500) + Kilohertz(1) == Hertz(1500)


def test_time_and_frequency_are_reciprocals_of_each_other():
    assert 1 / Second(2) == Hertz(Decimal("0.5"))
    assert 1 / Hertz(50) == Second(Decimal("0.02"))


"""Curated list of reciprocal round-trips values.

`Decimal`'s division only terminates exactly when the divisor's prime factors are
2 and 5, so a value like 3 would make `1 / (1 / x) == x` a statement about rounding
behavior, not about whether the reciprocal itself is correct.
"""
CLEAN_RECIPROCAL_VALUES = [
    Decimal(1),
    Decimal(2),
    Decimal(4),
    Decimal(5),
    Decimal(8),
    Decimal(10),
    Decimal("0.5"),
    Decimal("0.25"),
    Decimal(100),
    Decimal(1000),
    Decimal("2.5"),
]


@pytest.mark.parametrize("value", CLEAN_RECIPROCAL_VALUES, ids=str)
def test_time_and_frequency_reciprocal_round_trips(value):
    original = Second(value)
    assert 1 / (1 / original) == original


@pytest.mark.parametrize("value", CLEAN_RECIPROCAL_VALUES, ids=str)
def test_sampling_period_and_sample_rate_reciprocal_round_trips(value):
    original = Second(value).to_sampling_period()
    assert 1 / (1 / original) == original


def test_time_times_frequency_is_dimensionless():
    ratio = Second(2) * Hertz(Decimal("0.5"))
    assert not hasattr(ratio, "magnitude")
    assert ratio == Decimal(1)


def test_frequency_and_sample_rate_are_not_interchangeable():
    """Frequency and SampleRate share a dimension but are different concepts."""
    with pytest.raises(IncompatibleDimensionError):
        Hertz(50) + SamplesPerSecond(50)  # type: ignore[operator]  # not (yet) flagged by ty across sibling quantity types

    with pytest.raises(IncompatibleDimensionError):
        Hertz(50) - SamplesPerSecond(50)  # type: ignore[operator]  # not (yet) flagged by ty across sibling quantity types

    assert (Hertz(50) == SamplesPerSecond(50)) is False


def test_frequency_and_baud_rate_are_not_interchangeable():
    with pytest.raises(IncompatibleDimensionError):
        Hertz(9600) + Baud(9600)  # type: ignore[operator]  # not (yet) flagged by ty across sibling quantity types

    assert (Hertz(9600) == Baud(9600)) is False


def test_sample_rate_and_baud_rate_are_not_interchangeable():
    with pytest.raises(IncompatibleDimensionError):
        SamplesPerSecond(9600) + Baud(9600)  # type: ignore[operator]  # not (yet) flagged by ty across sibling quantity types


def test_sampling_period_and_sample_rate_are_reciprocals_of_each_other():
    assert 1 / Second(2).to_sampling_period() == SamplesPerSecond(Decimal("0.5"))
    assert 1 / SamplesPerSecond(500) == Millisecond(2).to_sampling_period()


def test_sampling_period_reciprocal_does_not_produce_frequency():
    """SamplingPeriod shares Time's dimension, but its reciprocal is a SampleRate."""
    result = 1 / Second(2).to_sampling_period()
    assert isinstance(result, SampleRate)
    assert not isinstance(result, Frequency)


def test_sample_rate_as_frequency():
    rate = SamplesPerSecond(500)
    frequency = rate.to_frequency()
    assert isinstance(frequency, Frequency)
    assert frequency == Hertz(500)


def test_frequency_as_frequency_is_identity():
    frequency = Hertz(50)
    assert frequency.to_frequency() is frequency


def test_baud_rate_reciprocal_raises_type_error():
    """BaudRate has no default reciprocal: baud is not Hz."""
    with pytest.raises(TypeError):
        1 / Baud(9600)


def test_baud_rate_has_no_as_frequency():
    assert not hasattr(Baud(9600), "to_frequency")


def test_baud_rate_does_not_satisfy_convertible_to_frequency():
    assert isinstance(Hertz(50), ConvertibleToFrequency)
    assert isinstance(SamplesPerSecond(500), ConvertibleToFrequency)
    assert not isinstance(Baud(9600), ConvertibleToFrequency)


def test_reciprocal_of_an_unregistered_result_dimension_raises():
    """1 / Volt(5) is dimensionally valid but unregistered: raise, not succeed."""
    with pytest.raises(UnrepresentableDimensionError):
        1 / Volt(5)


def test_naked_number_addition_is_rejected_for_temporal_types_too():
    with pytest.raises(InvalidMeasurementError, match="wrap it in a unit constructor"):
        Second(5) + 4.2  # type: ignore[operator]  # ty: ignore[unsupported-operator]


@pytest.mark.parametrize(
    ("constructor", "value", "factor", "expected"),
    [
        pytest.param(Second, 2, 3, 6, id="Second"),
        pytest.param(Hertz, 2, 3, 6, id="Hertz"),
        pytest.param(
            lambda v: Second(v).to_sampling_period(),
            2,
            3,
            6,
            id="Time.to_sampling_period",
        ),
        pytest.param(SamplesPerSecond, 2, 3, 6, id="SamplesPerSecond"),
        pytest.param(Baud, 2, 3, 6, id="Baud"),
    ],
)
def test_scalar_multiplication_and_division(constructor, value, factor, expected):
    assert constructor(value) * factor == constructor(expected)
    assert constructor(expected) / factor == constructor(value)


def test_kilobaud_scales_correctly():
    assert Kilobaud(1) == Baud(1000)


def test_sampling_period_and_sample_rate_reject_unsupported_reflected_operands():
    with pytest.raises(TypeError):
        object() / Second(2).to_sampling_period()

    with pytest.raises(TypeError):
        object() / SamplesPerSecond(500)


def test_subsecond_si_prefixes_are_exact():
    assert Femtosecond(1000) == Picosecond(1)
    assert Picosecond(1000) == Nanosecond(1)
    assert Nanosecond(1000) == Microsecond(1)
    assert Microsecond(1000) == Millisecond(1)
    assert Millisecond(1000) == Second(1)


def test_day_is_exactly_86400_seconds():
    assert Day(1) == Second(86_400)


def test_week_is_exactly_seven_days():
    assert Week(1) == Day(7)
    assert Week(1) == Second(604_800)


def test_fortnight_is_exactly_two_weeks():
    assert Fortnight(1) == Week(2)
    assert Fortnight(1) == Day(14)
    assert Fortnight(1) == Second(1_209_600)


def test_julian_year_is_exactly_365_25_days():
    assert JulianYear(1) == Day(Decimal("365.25"))
    assert JulianYear(1) == Second(31_557_600)


def test_physics_jiffy_is_light_crossing_one_femtometre():
    speed_of_light = 299_792_458_000_000_000_000_000
    assert Jiffy(1) * speed_of_light == Second(1)


def test_jiffy_reciprocal_is_exact():
    speed_of_light = 299_792_458_000_000_000_000_000
    assert 1 / Jiffy(1) == Hertz(speed_of_light)


@pytest.mark.parametrize(
    ("constructor", "expected_seconds"),
    [
        pytest.param(Minute, Decimal(60), id="Minute"),
        pytest.param(Hour, Decimal(3600), id="Hour"),
        pytest.param(Day, Decimal(86_400), id="Day"),
        pytest.param(Week, Decimal(604_800), id="Week"),
        pytest.param(Fortnight, Decimal(1_209_600), id="Fortnight"),
        pytest.param(JulianYear, Decimal(31_557_600), id="JulianYear"),
    ],
)
def test_exact_long_duration_scales(constructor, expected_seconds):
    assert constructor(1) == Second(expected_seconds)


def test_human_scale_durations_compose_exactly():
    duration = Fortnight(1) + Day(1) + Hour(6) + Minute(30) + Second(15)
    assert duration.to(SECOND) == Second(1_319_415)
