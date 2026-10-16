"""A specialisation is a role of a kind of its dimension and shape."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from kuchka import Time
from kuchka.quantities.base import registry
from tests.support.synthetic import linear_kind
from tests.support.synthetic import modular_kind

if TYPE_CHECKING:
    from kuchka.dimensions import Dimension


@pytest.mark.usefixtures("open_registry")
def test_a_specialisation_joins_without_becoming_principal(novel: Dimension) -> None:
    general, role = linear_kind("General", novel), linear_kind("Role", novel)
    registry._register(novel, general)  # noqa: SLF001
    registry._register(novel, role, specialisation_of=general)  # noqa: SLF001
    assert registry._DIMENSION_REGISTRY[novel] is general  # noqa: SLF001
    assert registry._kinds_of(novel) == (general, role)  # noqa: SLF001


@pytest.mark.usefixtures("open_registry")
def test_a_linear_phase_can_share_a_dimension_with_a_modular_angle(
    novel: Dimension,
) -> None:
    angle = modular_kind("Wrapped", novel)
    displacement = linear_kind("Displacement", novel)
    phase = linear_kind("Phase", novel)
    registry._register(novel, angle)  # noqa: SLF001
    registry._register(novel, displacement)  # noqa: SLF001
    registry._register(novel, phase, specialisation_of=displacement)  # noqa: SLF001
    assert registry._DIMENSION_REGISTRY[novel] is displacement  # noqa: SLF001
    assert registry._kinds_of(novel) == (angle, displacement, phase)  # noqa: SLF001


@pytest.mark.usefixtures("open_registry")
def test_a_specialisation_is_not_limited_to_linear_kinds(novel: Dimension) -> None:
    wrapped, heading = modular_kind("Wrapped", novel), modular_kind("Heading", novel)
    registry._register(novel, wrapped)  # noqa: SLF001
    registry._register(novel, heading, specialisation_of=wrapped)  # noqa: SLF001
    assert registry._SPECIALISATIONS[heading] is wrapped  # noqa: SLF001
    assert novel not in registry._DIMENSION_REGISTRY  # noqa: SLF001


@pytest.mark.usefixtures("open_registry")
def test_a_specialisation_names_a_kind_registered_for_its_dimension(
    novel: Dimension,
) -> None:
    role = linear_kind("Role", novel)
    with pytest.raises(TypeError, match="cannot specialise"):
        registry._register(novel, role, specialisation_of=Time)  # noqa: SLF001
    registry._register(novel, linear_kind("General", novel))  # noqa: SLF001
    with pytest.raises(TypeError, match="cannot specialise"):
        registry._register(novel, role, specialisation_of=Time)  # noqa: SLF001


@pytest.mark.usefixtures("open_registry")
def test_a_specialisation_is_not_a_target(novel: Dimension) -> None:
    general, role = linear_kind("General", novel), linear_kind("Role", novel)
    registry._register(novel, general)  # noqa: SLF001
    registry._register(novel, role, specialisation_of=general)  # noqa: SLF001
    with pytest.raises(TypeError, match="itself a specialisation"):
        registry._register(novel, linear_kind("Deeper", novel), specialisation_of=role)  # noqa: SLF001


@pytest.mark.usefixtures("open_registry")
def test_a_kind_cannot_specialise_itself(novel: Dimension) -> None:
    general = linear_kind("General", novel)
    registry._register(novel, general)  # noqa: SLF001
    with pytest.raises(TypeError, match="different relation"):
        registry._register(novel, general, specialisation_of=general)  # noqa: SLF001
    unregistered = linear_kind("Unregistered", novel)
    with pytest.raises(TypeError, match="cannot specialise"):
        registry._register(novel, unregistered, specialisation_of=unregistered)  # noqa: SLF001


@pytest.mark.usefixtures("open_registry")
def test_a_specialisation_has_the_shape_of_its_kind(novel: Dimension) -> None:
    wrapped, unwrapped = modular_kind("Wrapped", novel), linear_kind("Unwrapped", novel)
    registry._register(novel, wrapped)  # noqa: SLF001
    with pytest.raises(TypeError, match="shape"):
        registry._register(novel, unwrapped, specialisation_of=wrapped)  # noqa: SLF001
    assert registry._kinds_of(novel) == (wrapped,)  # noqa: SLF001
