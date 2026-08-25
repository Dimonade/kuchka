"""Time, Frequency, and the acquisition-domain vocabulary that shares their dimensions.

Covers the registered pair (Time, Frequency) and the domain pair
(SamplingPeriod, SampleRate) and BaudRate: same two dimensions, three different concepts,
and the point of this module is to prove that sharing a dimension is not the same as
being interchangeable.
"""

from decimal import Decimal

import pytest
from kuchka import Baud
from kuchka import ConvertibleToFrequency
from kuchka import Frequency
from kuchka import Hertz
from kuchka import IncompatibleDimensionError
from kuchka import InvalidMeasurementError
from kuchka import Kilobaud
from kuchka import Kilohertz
from kuchka import Millisecond
from kuchka import MillisecondSamplingPeriod
from kuchka import SampleRate
from kuchka import SamplesPerSecond
from kuchka import Second
from kuchka import SecondSamplingPeriod
from kuchka import UnrepresentableDimensionError
from kuchka import Volt
from kuchka.dimensions import FREQUENCY
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base import register


def test_time_addition_and_prefix_conversion():
    assert Second(1) + Millisecond(500) == Second(Decimal("1.5"))


def test_frequency_addition_and_prefix_conversion():
    assert Hertz(500) + Kilohertz(1) == Hertz(1500)


def test_time_and_frequency_are_reciprocals_of_each_other():
    assert 1 / Second(2) == Hertz(Decimal("0.5"))
    assert 1 / Hertz(50) == Second(Decimal("0.02"))


def test_reciprocal_round_trips():
    original = Second(4)
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
    assert 1 / SecondSamplingPeriod(2) == SamplesPerSecond(Decimal("0.5"))
    assert 1 / SamplesPerSecond(500) == MillisecondSamplingPeriod(2)


def test_sampling_period_reciprocal_does_not_produce_frequency():
    """SamplingPeriod shares Time's dimension, but its reciprocal is a SampleRate."""
    result = 1 / SecondSamplingPeriod(2)
    assert isinstance(result, SampleRate)
    assert not isinstance(result, Frequency)


def test_sample_rate_as_frequency():
    rate = SamplesPerSecond(500)
    frequency = rate.as_frequency()
    assert isinstance(frequency, Frequency)
    assert frequency == Hertz(500)


def test_frequency_as_frequency_is_identity():
    frequency = Hertz(50)
    assert frequency.as_frequency() is frequency


def test_baud_rate_reciprocal_raises_type_error():
    """BaudRate has no default reciprocal: baud is not Hz."""
    with pytest.raises(TypeError):
        1 / Baud(9600)


def test_baud_rate_has_no_as_frequency():
    assert not hasattr(Baud(9600), "as_frequency")


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


def test_register_rejects_a_second_type_for_an_already_registered_dimension():
    class RogueFrequency(LinearQuantity):
        dimension = FREQUENCY

    with pytest.raises(TypeError, match="already registered"):
        register(FREQUENCY, RogueFrequency)


def test_register_is_idempotent_for_the_same_type():
    """Re-registering the exact same type for the same dimension is not an error."""
    register(FREQUENCY, Frequency)  # should not raise


def test_scalar_multiplication_and_division_across_all_temporal_types():
    assert Second(2) * 3 == Second(6)
    assert Second(6) / 3 == Second(2)
    assert Hertz(2) * 3 == Hertz(6)
    assert Hertz(6) / 3 == Hertz(2)
    assert SecondSamplingPeriod(2) * 3 == SecondSamplingPeriod(6)
    assert SecondSamplingPeriod(6) / 3 == SecondSamplingPeriod(2)
    assert SamplesPerSecond(2) * 3 == SamplesPerSecond(6)
    assert SamplesPerSecond(6) / 3 == SamplesPerSecond(2)
    assert Baud(2) * 3 == Baud(6)
    assert Baud(6) / 3 == Baud(2)
    assert Kilobaud(1) == Baud(1000)


def test_sampling_period_and_sample_rate_reject_unsupported_reflected_operands():
    with pytest.raises(TypeError):
        object() / SecondSamplingPeriod(2)

    with pytest.raises(TypeError):
        object() / SamplesPerSecond(500)
