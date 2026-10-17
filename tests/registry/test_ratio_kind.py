"""The ratio kind: the kind that a ratio of two like quantities has."""

from __future__ import annotations

import pytest

from kuchka import Proportion
from kuchka import Voltage
from kuchka.dimensions import DIMENSIONLESS
from kuchka.quantities.base import registry
from tests.support.synthetic import linear_kind


def test_proportion_is_the_ratio_kind() -> None:
    assert registry._RATIO_KIND[DIMENSIONLESS] is Proportion  # noqa: SLF001


def test_the_ratio_kind_is_fixed_once_the_registry_is_closed() -> None:
    with pytest.raises(RuntimeError, match="closed"):
        registry._register_ratio(Proportion)  # noqa: SLF001


def test_a_kind_with_extent_cannot_be_the_ratio_kind(open_registry: None) -> None:
    del open_registry
    with pytest.raises(TypeError, match="dimensionless"):
        registry._register_ratio(Voltage)  # noqa: SLF001


def test_an_unregistered_kind_cannot_be_the_ratio_kind(open_registry: None) -> None:
    del open_registry
    with pytest.raises(TypeError, match="registered"):
        registry._register_ratio(linear_kind("Unregistered", DIMENSIONLESS))  # noqa: SLF001


def test_a_registered_dimensionless_kind_can_be_the_ratio_kind(
    open_registry: None,
) -> None:
    del open_registry
    kind = linear_kind("Made", DIMENSIONLESS)
    registry._register(DIMENSIONLESS, kind)  # noqa: SLF001
    registry._register_ratio(kind)  # noqa: SLF001
    assert registry._RATIO_KIND[DIMENSIONLESS] is kind  # noqa: SLF001
