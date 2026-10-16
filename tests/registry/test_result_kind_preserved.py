"""A dimensionless operand keeps the kind of the other operand."""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import BaudRate
from kuchka import Frequency
from kuchka import Proportion
from kuchka import SampleRate
from kuchka import SamplingPeriod
from kuchka import Voltage
from kuchka.units import proportion
from kuchka.units import voltage

SAMPLE_RATE = SampleRate(Fraction(8), SampleRate._canonical_unit)  # noqa: SLF001


SAMPLING_PERIOD = SamplingPeriod(Fraction(1, 8), SamplingPeriod._canonical_unit)  # noqa: SLF001


BAUD_RATE = BaudRate(Fraction(9600), BaudRate._canonical_unit)  # noqa: SLF001


@pytest.mark.parametrize(
    ("quantity", "kind"),
    [
        (SAMPLE_RATE, SampleRate),
        (SAMPLING_PERIOD, SamplingPeriod),
        (BAUD_RATE, BaudRate),
        (voltage.Volt(3), Voltage),
    ],
    ids=lambda value: (
        type(value).__name__ if not isinstance(value, type) else value.__name__
    ),
)
@pytest.mark.parametrize(
    "scale", [proportion.Ratio(2), proportion.Percent(50)], ids=["ratio", "percent"]
)
def test_a_proportion_keeps_the_kind_of_the_other_operand(
    quantity: object, kind: type, scale: Proportion
) -> None:
    for result in (quantity * scale, scale * quantity, quantity / scale):  # type: ignore[operator]
        assert type(result) is kind


def test_a_scaled_role_keeps_its_own_unit_and_value() -> None:
    assert (SAMPLE_RATE * proportion.Percent(50)).magnitude == Fraction(4)
    assert str(SAMPLE_RATE * proportion.Percent(50)) == "4 Sa/s"
    assert str(BAUD_RATE * proportion.Percent(50)) == "4800 Bd"
    assert (SAMPLING_PERIOD / proportion.Percent(50)).magnitude == Fraction(1, 4)


def test_a_proportion_does_not_divide_into_a_kind() -> None:
    assert type(proportion.Ratio(1) / SAMPLING_PERIOD) is Frequency
