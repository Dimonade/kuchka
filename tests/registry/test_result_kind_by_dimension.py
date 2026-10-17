"""Otherwise the principal kind of the dimension is the result."""

from __future__ import annotations

from fractions import Fraction

from kuchka import Frequency
from kuchka import Power
from kuchka import Proportion
from kuchka import SampleRate
from kuchka import SamplingPeriod
from kuchka.units import current
from kuchka.units import proportion
from kuchka.units import time
from kuchka.units import voltage

SAMPLING_PERIOD = SamplingPeriod(Fraction(1, 8), SamplingPeriod._canonical_unit)  # noqa: SLF001


def test_a_product_of_two_quantities_takes_the_principal_kind() -> None:
    assert type(voltage.Volt(5) * current.Ampere(2)) is Power
    assert type(time.Second(1) / time.Second(2)) is Proportion


def test_a_ratio_of_like_quantities_is_a_proportion() -> None:
    assert proportion.Percent(50) * proportion.Percent(50) == proportion.Ratio(
        Fraction(1, 4)
    )
    assert type(time.Second(1) / time.Second(2)) is Proportion


def test_the_reciprocal_of_a_role_is_still_its_own_partner() -> None:
    assert type(1 / SAMPLING_PERIOD) is SampleRate
    assert type(1 / time.Second(2)) is Frequency
