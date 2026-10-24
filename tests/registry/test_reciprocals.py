"""Reciprocal specialisations: the one pair of roles that multiply together."""

from __future__ import annotations

import pytest

from kuchka import Frequency
from kuchka import SampleRate
from kuchka import SamplingPeriod
from kuchka import Time
from kuchka.quantities.base import registry


def test_a_sampling_period_and_a_sample_rate_are_reciprocals() -> None:
    assert registry._RECIPROCALS[SamplingPeriod] is SampleRate  # noqa: SLF001
    assert registry._RECIPROCALS[SampleRate] is SamplingPeriod  # noqa: SLF001


def test_reciprocals_are_fixed_once_the_registry_is_closed() -> None:
    with pytest.raises(RuntimeError, match="closed"):
        registry._register_reciprocal(SamplingPeriod, SampleRate)  # noqa: SLF001


def test_only_specialisations_with_a_dimensionless_product_are_reciprocals(
    open_registry: None,
) -> None:
    del open_registry
    with pytest.raises(TypeError, match="specialisations"):
        registry._register_reciprocal(Time, Frequency)  # noqa: SLF001
    with pytest.raises(TypeError, match="dimensionless"):
        registry._register_reciprocal(SampleRate, SampleRate)  # noqa: SLF001
