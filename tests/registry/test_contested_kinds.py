"""Linear kinds on equal footing leave a dimension without a principal."""

from __future__ import annotations

from fractions import Fraction
from typing import TYPE_CHECKING

import pytest

import kuchka
from kuchka import AmbiguousKindError
from kuchka import MeasurementError
from kuchka import UnrepresentableDimensionError
from kuchka.quantities.base import registry
from tests.support.synthetic import linear_kind
from tests.support.synthetic import modular_kind

if TYPE_CHECKING:
    from kuchka.dimensions import Dimension


@pytest.mark.usefixtures("open_registry")
def test_two_contested_kinds_leave_the_dimension_without_a_principal(
    novel: Dimension,
) -> None:
    first, second = linear_kind("First", novel), linear_kind("Second", novel)
    registry._register(novel, first)  # noqa: SLF001
    registry._register(novel, second, contested_with=first)  # noqa: SLF001
    assert novel not in registry._DIMENSION_REGISTRY  # noqa: SLF001
    assert registry._CONTESTED[novel] == (first, second)  # noqa: SLF001
    assert registry._kinds_of(novel) == (first, second)  # noqa: SLF001


@pytest.mark.usefixtures("open_registry")
def test_a_third_contested_kind_joins_through_any_member(novel: Dimension) -> None:
    first, second, third = (linear_kind(n, novel) for n in ("First", "Second", "Third"))
    registry._register(novel, first)  # noqa: SLF001
    registry._register(novel, second, contested_with=first)  # noqa: SLF001
    registry._register(novel, third, contested_with=second)  # noqa: SLF001
    assert registry._CONTESTED[novel] == (first, second, third)  # noqa: SLF001


@pytest.mark.usefixtures("open_registry")
def test_a_specialisation_can_refine_a_contested_kind(novel: Dimension) -> None:
    first, second, role = (linear_kind(n, novel) for n in ("First", "Second", "Role"))
    registry._register(novel, first)  # noqa: SLF001
    registry._register(novel, second, contested_with=first)  # noqa: SLF001
    registry._register(novel, role, specialisation_of=second)  # noqa: SLF001
    assert registry._kinds_of(novel) == (first, second, role)  # noqa: SLF001


@pytest.mark.usefixtures("open_registry")
def test_only_linear_kinds_are_contested(novel: Dimension) -> None:
    first = linear_kind("First", novel)
    registry._register(novel, first)  # noqa: SLF001
    with pytest.raises(TypeError, match="only linear kinds"):
        registry._register(novel, modular_kind("Wrapped", novel), contested_with=first)  # noqa: SLF001
    assert registry._DIMENSION_REGISTRY[novel] is first  # noqa: SLF001


@pytest.mark.usefixtures("open_registry")
def test_a_contest_is_with_a_kind_arithmetic_could_produce(novel: Dimension) -> None:
    wrapped = modular_kind("Wrapped", novel)
    registry._register(novel, wrapped)  # noqa: SLF001
    with pytest.raises(TypeError, match="only linear kinds"):
        registry._register(novel, linear_kind("Linear", novel), contested_with=wrapped)  # noqa: SLF001


@pytest.mark.usefixtures("open_registry")
def test_a_contested_dimension_is_not_resolved_to_one_kind(novel: Dimension) -> None:
    first, second = linear_kind("First", novel), linear_kind("Second", novel)
    registry._register(novel, first)  # noqa: SLF001
    registry._register(novel, second, contested_with=first)  # noqa: SLF001
    with pytest.raises(AmbiguousKindError, match="First, Second") as caught:
        registry._promote(novel, Fraction(1))  # noqa: SLF001
    assert caught.value.dimension == novel
    assert caught.value.candidates == (first, second)


def test_the_ambiguity_error_is_part_of_the_library_family() -> None:
    assert issubclass(AmbiguousKindError, UnrepresentableDimensionError)
    assert issubclass(AmbiguousKindError, MeasurementError)
    assert kuchka.AmbiguousKindError is AmbiguousKindError
