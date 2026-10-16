"""A contested dimension needs a rule, or the result is ambiguous."""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import AmbiguousKindError
from kuchka import Frequency
from kuchka import Length
from kuchka import SampleRate
from kuchka import Time
from kuchka import Velocity
from kuchka.quantities.base import registry
from kuchka.units import acceleration as acc
from kuchka.units import length
from kuchka.units import proportion
from kuchka.units import velocity

SAMPLE_RATE = SampleRate(Fraction(8), SampleRate._canonical_unit)  # noqa: SLF001


@pytest.mark.usefixtures("contested_frequency")
def test_a_contested_result_without_a_rule_is_ambiguous() -> None:
    with pytest.raises(AmbiguousKindError, match="Frequency, SampleRate") as caught:
        acc.MetrePerSecondSquared(6) / velocity.MetrePerSecond(3)
    assert caught.value.candidates == (Frequency, SampleRate)
    assert "construct the one you mean" in str(caught.value)


@pytest.mark.usefixtures("contested_frequency")
def test_a_rule_names_the_kind_of_a_contested_result() -> None:
    registry._rule(Velocity, "/", Length, SampleRate)  # noqa: SLF001
    result = velocity.MetrePerSecond(10) / length.Metre(2)
    assert type(result) is SampleRate
    assert result.magnitude == Fraction(5)


@pytest.mark.usefixtures("contested_frequency")
def test_a_rule_decides_only_its_own_operands() -> None:
    registry._rule(Velocity, "/", Length, SampleRate)  # noqa: SLF001
    with pytest.raises(AmbiguousKindError):
        acc.MetrePerSecondSquared(6) / velocity.MetrePerSecond(3)


@pytest.mark.usefixtures("contested_frequency")
def test_a_contested_kind_keeps_its_kind_when_scaled() -> None:
    frequency = Frequency(Fraction(4), Frequency._canonical_unit)  # noqa: SLF001
    assert type(frequency * proportion.Ratio(2)) is Frequency
    assert type(SAMPLE_RATE * proportion.Ratio(2)) is SampleRate


@pytest.mark.usefixtures("contested_frequency")
def test_the_reciprocal_of_a_contested_kind_is_resolved_by_dimension() -> None:
    assert type(1 / Frequency(Fraction(4), Frequency._canonical_unit)) is Time  # noqa: SLF001
