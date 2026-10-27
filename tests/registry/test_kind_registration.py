"""Kinds that share a dimension state how they relate, or are refused."""

from __future__ import annotations

import pytest

from kuchka import Activity
from kuchka import ApparentPower
from kuchka import BaudRate
from kuchka import Frequency
from kuchka import Impedance
from kuchka import Power
from kuchka import Pressure
from kuchka import Reactance
from kuchka import ReactivePower
from kuchka import Resistance
from kuchka import SampleRate
from kuchka import SamplingPeriod
from kuchka import Stress
from kuchka import Time
from kuchka.dimensions import DIMENSIONLESS
from kuchka.dimensions import TIME
from kuchka.dimensions import Dimension
from kuchka.quantities.base import registry
from tests.support.synthetic import linear_kind
from tests.support.synthetic import modular_kind
from tests.support.synthetic import registry_state


@pytest.mark.parametrize(
    ("kind", "target"),
    [
        (Activity, Frequency),
        (ApparentPower, Power),
        (BaudRate, Frequency),
        (Impedance, Resistance),
        (Reactance, Resistance),
        (ReactivePower, Power),
        (SampleRate, Frequency),
        (SamplingPeriod, Time),
        (Stress, Pressure),
    ],
    ids=lambda value: value.__name__,
)
def test_a_role_of_a_kind_is_its_specialisation(kind: type, target: type) -> None:
    assert registry._SPECIALISATIONS[kind] is target  # noqa: SLF001


def test_only_the_listed_kinds_are_specialisations() -> None:
    assert set(registry._SPECIALISATIONS) == {  # noqa: SLF001
        Activity,
        ApparentPower,
        BaudRate,
        Impedance,
        Reactance,
        ReactivePower,
        SampleRate,
        SamplingPeriod,
        Stress,
    }


def test_every_specialisation_is_consistent() -> None:
    for kind, target in registry._SPECIALISATIONS.items():  # noqa: SLF001
        assert kind.dimension == target.dimension
        assert target not in registry._SPECIALISATIONS  # noqa: SLF001
        assert registry._shape_of(kind) is registry._shape_of(target)  # noqa: SLF001
        assert kind not in registry._DIMENSION_REGISTRY.values()  # noqa: SLF001


def test_an_affine_kind_shares_the_dimension_of_its_delta_type() -> None:
    for found in registry._KINDS_BY_DIMENSION.values():  # noqa: SLF001
        for kind in found:
            delta = getattr(kind, "_delta_type", None)
            if delta is not None:
                assert registry._is_registered(delta)  # noqa: SLF001
                assert delta.dimension == kind.dimension


@pytest.mark.usefixtures("open_registry")
def test_a_second_linear_kind_without_a_relation_is_refused(novel: Dimension) -> None:
    first = linear_kind("Incumbent", novel)
    registry._register(novel, first)  # noqa: SLF001
    with pytest.raises(TypeError, match="Incumbent"):
        registry._register(novel, linear_kind("Newcomer", novel))  # noqa: SLF001
    assert registry._kinds_of(novel) == (first,)  # noqa: SLF001


@pytest.mark.usefixtures("open_registry")
def test_a_kind_is_registered_for_its_own_dimension_only(novel: Dimension) -> None:
    with pytest.raises(TypeError, match="cannot be registered"):
        registry._register(novel, linear_kind("Stray", TIME))  # noqa: SLF001


@pytest.mark.usefixtures("open_registry")
def test_a_kind_states_one_relation(novel: Dimension) -> None:
    first = linear_kind("First", novel)
    registry._register(novel, first)  # noqa: SLF001
    with pytest.raises(TypeError, match="not both"):
        registry._register(  # noqa: SLF001
            novel,
            linear_kind("Second", novel),
            specialisation_of=first,
            contested_with=first,
        )


@pytest.mark.usefixtures("open_registry")
def test_a_refused_registration_leaves_the_registry_unchanged(novel: Dimension) -> None:
    registry._register(novel, linear_kind("General", novel))  # noqa: SLF001
    before = registry_state()
    for attempt in (
        {"specialisation_of": Time},
        {"contested_with": Time},
        {},
    ):
        with pytest.raises(TypeError):
            registry._register(novel, linear_kind("Role", novel), **attempt)  # noqa: SLF001
        assert before == registry_state()


@pytest.mark.usefixtures("open_registry")
def test_a_kind_of_another_shape_shares_a_dimension_without_a_relation(
    novel: Dimension,
) -> None:
    linear, wrapped, other = (
        linear_kind("Linear", novel),
        modular_kind("Wrapped", novel),
        modular_kind("Other", novel),
    )
    for kind in (linear, wrapped, other):
        registry._register(novel, kind)  # noqa: SLF001
    assert registry._kinds_of(novel) == (linear, wrapped, other)  # noqa: SLF001


@pytest.mark.usefixtures("open_registry")
def test_the_first_linear_kind_is_principal_whatever_registered_before_it(
    novel: Dimension,
) -> None:
    wrapped, linear = modular_kind("Wrapped", novel), linear_kind("Linear", novel)
    registry._register(novel, wrapped)  # noqa: SLF001
    registry._register(novel, linear)  # noqa: SLF001
    assert registry._DIMENSION_REGISTRY[novel] is linear  # noqa: SLF001
    assert registry._kinds_of(novel) == (wrapped, linear)  # noqa: SLF001


@pytest.mark.usefixtures("open_registry")
def test_the_principal_is_the_same_in_either_registration_order(
    novel: Dimension,
) -> None:
    linear, wrapped = linear_kind("Linear", novel), modular_kind("Wrapped", novel)
    registry._register(novel, linear)  # noqa: SLF001
    registry._register(novel, wrapped)  # noqa: SLF001
    assert registry._DIMENSION_REGISTRY[novel] is linear  # noqa: SLF001
    assert registry._kinds_of(novel) == (linear, wrapped)  # noqa: SLF001


@pytest.mark.usefixtures("open_registry")
def test_a_dimensionless_kind_never_competes(novel: Dimension) -> None:
    del novel
    first, second = (linear_kind(n, DIMENSIONLESS) for n in ("Count", "Level"))
    registry._DIMENSION_REGISTRY.pop(DIMENSIONLESS, None)  # noqa: SLF001
    registry._register(DIMENSIONLESS, first)  # noqa: SLF001
    registry._register(DIMENSIONLESS, second)  # noqa: SLF001
    assert DIMENSIONLESS not in registry._DIMENSION_REGISTRY  # noqa: SLF001
    assert first in registry._kinds_of(DIMENSIONLESS)  # noqa: SLF001
    assert second in registry._kinds_of(DIMENSIONLESS)  # noqa: SLF001


@pytest.mark.usefixtures("open_registry")
def test_registering_the_same_kind_again_is_not_an_error(novel: Dimension) -> None:
    general, role = linear_kind("General", novel), linear_kind("Role", novel)
    registry._register(novel, general)  # noqa: SLF001
    registry._register(novel, role, specialisation_of=general)  # noqa: SLF001
    before = registry_state()
    registry._register(novel, general)  # noqa: SLF001
    registry._register(novel, role, specialisation_of=general)  # noqa: SLF001
    assert before == registry_state()


@pytest.mark.usefixtures("open_registry")
def test_a_registered_kind_cannot_change_its_relation(novel: Dimension) -> None:
    general, role = linear_kind("General", novel), linear_kind("Role", novel)
    registry._register(novel, general)  # noqa: SLF001
    registry._register(novel, role, specialisation_of=general)  # noqa: SLF001
    with pytest.raises(TypeError, match="different relation"):
        registry._register(novel, role)  # noqa: SLF001
    with pytest.raises(TypeError, match="different relation"):
        registry._register(novel, role, contested_with=general)  # noqa: SLF001
    with pytest.raises(TypeError, match="different relation"):
        registry._register(novel, general, specialisation_of=role)  # noqa: SLF001
