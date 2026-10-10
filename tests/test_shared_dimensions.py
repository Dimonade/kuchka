"""Several kinds can share a dimension, and the registry keeps three questions apart.

A type is a kind of its dimension, whatever its shape (linear, affine, modular,
logarithmic), and every concrete quantity type is in the catalogue of kinds.
Arithmetic produces one linear kind per dimension with extent, its principal, so the
rules that pick it look only at linear kinds: a second linear kind states its relation
to the first, as a specialisation of it or as contested with it.
A kind of another shape, and a dimensionless kind, is catalogued and never competes.
A specialisation records meaning and shape: it converts nothing and picks no result.
The shared dimensions are listed here, so a new one is a deliberate change.
"""

from __future__ import annotations

from fractions import Fraction
from typing import TYPE_CHECKING

import pytest

import kuchka
from kuchka import AmbiguousKindError
from kuchka import Angle
from kuchka import BaudRate
from kuchka import Frequency
from kuchka import Instant
from kuchka import LogarithmicRatio
from kuchka import MeasurementError
from kuchka import Proportion
from kuchka import SampleRate
from kuchka import SamplingPeriod
from kuchka import Temperature
from kuchka import TemperatureDelta
from kuchka import Time
from kuchka import UnrepresentableDimensionError
from kuchka.dimensions import ANGLE
from kuchka.dimensions import DIMENSIONLESS
from kuchka.dimensions import FREQUENCY
from kuchka.dimensions import TEMPERATURE_DELTA
from kuchka.dimensions import TIME
from kuchka.dimensions import Dimension
from kuchka.quantities.base import AffineQuantity
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base import ModularQuantity
from kuchka.quantities.base import registry
from tests.quantity_families import CONCRETE_QUANTITY_TYPES

if TYPE_CHECKING:
    from collections.abc import Callable

SHARED = {
    TIME: (Time, SamplingPeriod, Instant),
    FREQUENCY: (Frequency, SampleRate, BaudRate),
    TEMPERATURE_DELTA: (TemperatureDelta, Temperature),
    DIMENSIONLESS: (Proportion, LogarithmicRatio),
}


def _linear(name: str, dimension: Dimension) -> type[LinearQuantity]:
    return type(name, (LinearQuantity,), {"dimension": dimension, "__slots__": ()})


def _modular(name: str, dimension: Dimension) -> type[ModularQuantity]:
    return type(name, (ModularQuantity,), {"dimension": dimension, "__slots__": ()})


def _state() -> tuple[object, ...]:
    return (
        dict(registry._KINDS_BY_DIMENSION),  # noqa: SLF001
        dict(registry._DIMENSION_REGISTRY),  # noqa: SLF001
        dict(registry._CONTESTED),  # noqa: SLF001
        dict(registry._SPECIALISATIONS),  # noqa: SLF001
    )


# The catalogue of kinds.


def test_the_shared_dimensions_are_exactly_the_listed_ones() -> None:
    assert registry._shared_dimensions() == SHARED  # noqa: SLF001


def test_an_unknown_dimension_has_no_kinds() -> None:
    assert registry._kinds_of(Dimension(mass=7)) == ()  # noqa: SLF001


@pytest.mark.parametrize("cls", CONCRETE_QUANTITY_TYPES, ids=lambda kind: kind.__name__)
def test_every_concrete_type_is_a_registered_kind(cls: type) -> None:
    assert registry._is_registered(cls)  # noqa: SLF001


def test_each_shape_has_registered_kinds() -> None:
    kinds = {kind for found in registry._KINDS_BY_DIMENSION.values() for kind in found}  # noqa: SLF001
    for shape in (LinearQuantity, AffineQuantity, ModularQuantity):
        assert any(issubclass(kind, shape) for kind in kinds)
    assert LogarithmicRatio in kinds


def test_a_dimensionless_kind_is_catalogued() -> None:
    assert registry._kinds_of(DIMENSIONLESS) == (Proportion, LogarithmicRatio)  # noqa: SLF001


# What arithmetic can return stays linear.


@pytest.mark.parametrize(
    "kind",
    [Angle, Instant, Temperature, LogarithmicRatio, Proportion],
    ids=lambda k: k.__name__,
)
def test_a_kind_arithmetic_cannot_produce_is_never_principal(kind: type) -> None:
    assert kind not in registry._DIMENSION_REGISTRY.values()  # noqa: SLF001
    assert not any(kind in group for group in registry._CONTESTED.values())  # noqa: SLF001


def test_a_dimension_with_a_kind_of_another_shape_keeps_its_principal() -> None:
    assert registry._DIMENSION_REGISTRY[TIME] is Time  # noqa: SLF001
    assert registry._DIMENSION_REGISTRY[TEMPERATURE_DELTA] is TemperatureDelta  # noqa: SLF001
    assert DIMENSIONLESS not in registry._DIMENSION_REGISTRY  # noqa: SLF001


def test_the_principal_kinds_are_linear_kinds_with_extent() -> None:
    for dimension, kind in registry._DIMENSION_REGISTRY.items():  # noqa: SLF001
        assert issubclass(kind, LinearQuantity)
        assert kind.dimension == dimension != DIMENSIONLESS
        assert registry._is_registered(kind)  # noqa: SLF001


def test_no_shipped_dimension_is_contested() -> None:
    assert registry._CONTESTED == {}  # noqa: SLF001


# Specialisations.


@pytest.mark.parametrize(
    ("kind", "target"),
    [(SamplingPeriod, Time), (SampleRate, Frequency), (BaudRate, Frequency)],
    ids=lambda value: value.__name__,
)
def test_a_role_of_a_kind_is_its_specialisation(kind: type, target: type) -> None:
    assert registry._SPECIALISATIONS[kind] is target  # noqa: SLF001


def test_only_the_listed_kinds_are_specialisations() -> None:
    assert set(registry._SPECIALISATIONS) == {SamplingPeriod, SampleRate, BaudRate}  # noqa: SLF001


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


# A second linear kind has to state its relation.


@pytest.fixture
def open_registry(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(registry, "_closed", False)
    for name in (
        "_KINDS_BY_DIMENSION",
        "_DIMENSION_REGISTRY",
        "_CONTESTED",
        "_SPECIALISATIONS",
    ):
        monkeypatch.setattr(registry, name, dict(getattr(registry, name)))


@pytest.fixture
def novel() -> Dimension:
    return Dimension(mass=3, angle=2)


open_ = pytest.mark.usefixtures("open_registry")


@open_
def test_a_second_linear_kind_without_a_relation_is_refused(novel: Dimension) -> None:
    first = _linear("Incumbent", novel)
    registry._register(novel, first)  # noqa: SLF001
    with pytest.raises(TypeError, match="Incumbent"):
        registry._register(novel, _linear("Newcomer", novel))  # noqa: SLF001
    assert registry._kinds_of(novel) == (first,)  # noqa: SLF001


@open_
def test_a_kind_is_registered_for_its_own_dimension_only(novel: Dimension) -> None:
    with pytest.raises(TypeError, match="cannot be registered"):
        registry._register(novel, _linear("Stray", TIME))  # noqa: SLF001


@open_
def test_a_kind_states_one_relation(novel: Dimension) -> None:
    first = _linear("First", novel)
    registry._register(novel, first)  # noqa: SLF001
    with pytest.raises(TypeError, match="not both"):
        registry._register(  # noqa: SLF001
            novel,
            _linear("Second", novel),
            specialisation_of=first,
            contested_with=first,
        )


@open_
def test_a_refused_registration_leaves_the_registry_unchanged(novel: Dimension) -> None:
    registry._register(novel, _linear("General", novel))  # noqa: SLF001
    before = _state()
    for attempt in (
        {"specialisation_of": Time},
        {"contested_with": Time},
        {},
    ):
        with pytest.raises(TypeError):
            registry._register(novel, _linear("Role", novel), **attempt)  # noqa: SLF001
        assert before == _state()


@open_
def test_a_kind_of_another_shape_shares_a_dimension_without_a_relation(
    novel: Dimension,
) -> None:
    linear, wrapped, other = (
        _linear("Linear", novel),
        _modular("Wrapped", novel),
        _modular("Other", novel),
    )
    for kind in (linear, wrapped, other):
        registry._register(novel, kind)  # noqa: SLF001
    assert registry._kinds_of(novel) == (linear, wrapped, other)  # noqa: SLF001


@open_
def test_the_first_linear_kind_is_principal_whatever_registered_before_it(
    novel: Dimension,
) -> None:
    wrapped, linear = _modular("Wrapped", novel), _linear("Linear", novel)
    registry._register(novel, wrapped)  # noqa: SLF001
    registry._register(novel, linear)  # noqa: SLF001
    assert registry._DIMENSION_REGISTRY[novel] is linear  # noqa: SLF001
    assert registry._kinds_of(novel) == (wrapped, linear)  # noqa: SLF001


@open_
def test_the_principal_is_the_same_in_either_registration_order(
    novel: Dimension,
) -> None:
    linear, wrapped = _linear("Linear", novel), _modular("Wrapped", novel)
    registry._register(novel, linear)  # noqa: SLF001
    registry._register(novel, wrapped)  # noqa: SLF001
    assert registry._DIMENSION_REGISTRY[novel] is linear  # noqa: SLF001
    assert registry._kinds_of(novel) == (linear, wrapped)  # noqa: SLF001


@open_
def test_a_dimensionless_kind_never_competes(novel: Dimension) -> None:
    del novel
    first, second = (_linear(n, DIMENSIONLESS) for n in ("Count", "Level"))
    registry._DIMENSION_REGISTRY.pop(DIMENSIONLESS, None)  # noqa: SLF001
    registry._register(DIMENSIONLESS, first)  # noqa: SLF001
    registry._register(DIMENSIONLESS, second)  # noqa: SLF001
    assert DIMENSIONLESS not in registry._DIMENSION_REGISTRY  # noqa: SLF001
    assert first in registry._kinds_of(DIMENSIONLESS)  # noqa: SLF001
    assert second in registry._kinds_of(DIMENSIONLESS)  # noqa: SLF001


@open_
def test_registering_the_same_kind_again_is_not_an_error(novel: Dimension) -> None:
    general, role = _linear("General", novel), _linear("Role", novel)
    registry._register(novel, general)  # noqa: SLF001
    registry._register(novel, role, specialisation_of=general)  # noqa: SLF001
    before = _state()
    registry._register(novel, general)  # noqa: SLF001
    registry._register(novel, role, specialisation_of=general)  # noqa: SLF001
    assert before == _state()


@open_
def test_a_registered_kind_cannot_change_its_relation(novel: Dimension) -> None:
    general, role = _linear("General", novel), _linear("Role", novel)
    registry._register(novel, general)  # noqa: SLF001
    registry._register(novel, role, specialisation_of=general)  # noqa: SLF001
    with pytest.raises(TypeError, match="different relation"):
        registry._register(novel, role)  # noqa: SLF001
    with pytest.raises(TypeError, match="different relation"):
        registry._register(novel, role, contested_with=general)  # noqa: SLF001
    with pytest.raises(TypeError, match="different relation"):
        registry._register(novel, general, specialisation_of=role)  # noqa: SLF001


# Specialisations.


@open_
def test_a_specialisation_joins_without_becoming_principal(novel: Dimension) -> None:
    general, role = _linear("General", novel), _linear("Role", novel)
    registry._register(novel, general)  # noqa: SLF001
    registry._register(novel, role, specialisation_of=general)  # noqa: SLF001
    assert registry._DIMENSION_REGISTRY[novel] is general  # noqa: SLF001
    assert registry._kinds_of(novel) == (general, role)  # noqa: SLF001


@open_
def test_a_linear_phase_can_share_a_dimension_with_a_modular_angle(
    novel: Dimension,
) -> None:
    angle = _modular("Wrapped", novel)
    displacement, phase = _linear("Displacement", novel), _linear("Phase", novel)
    registry._register(novel, angle)  # noqa: SLF001
    registry._register(novel, displacement)  # noqa: SLF001
    registry._register(novel, phase, specialisation_of=displacement)  # noqa: SLF001
    assert registry._DIMENSION_REGISTRY[novel] is displacement  # noqa: SLF001
    assert registry._kinds_of(novel) == (angle, displacement, phase)  # noqa: SLF001


@open_
def test_a_specialisation_is_not_limited_to_linear_kinds(novel: Dimension) -> None:
    wrapped, heading = _modular("Wrapped", novel), _modular("Heading", novel)
    registry._register(novel, wrapped)  # noqa: SLF001
    registry._register(novel, heading, specialisation_of=wrapped)  # noqa: SLF001
    assert registry._SPECIALISATIONS[heading] is wrapped  # noqa: SLF001
    assert novel not in registry._DIMENSION_REGISTRY  # noqa: SLF001


@open_
def test_a_specialisation_names_a_kind_registered_for_its_dimension(
    novel: Dimension,
) -> None:
    role = _linear("Role", novel)
    with pytest.raises(TypeError, match="cannot specialise"):
        registry._register(novel, role, specialisation_of=Time)  # noqa: SLF001
    registry._register(novel, _linear("General", novel))  # noqa: SLF001
    with pytest.raises(TypeError, match="cannot specialise"):
        registry._register(novel, role, specialisation_of=Time)  # noqa: SLF001


@open_
def test_a_specialisation_is_not_a_target(novel: Dimension) -> None:
    general, role = _linear("General", novel), _linear("Role", novel)
    registry._register(novel, general)  # noqa: SLF001
    registry._register(novel, role, specialisation_of=general)  # noqa: SLF001
    with pytest.raises(TypeError, match="itself a specialisation"):
        registry._register(novel, _linear("Deeper", novel), specialisation_of=role)  # noqa: SLF001


@open_
def test_a_kind_cannot_specialise_itself(novel: Dimension) -> None:
    general = _linear("General", novel)
    registry._register(novel, general)  # noqa: SLF001
    with pytest.raises(TypeError, match="different relation"):
        registry._register(novel, general, specialisation_of=general)  # noqa: SLF001
    unregistered = _linear("Unregistered", novel)
    with pytest.raises(TypeError, match="cannot specialise"):
        registry._register(novel, unregistered, specialisation_of=unregistered)  # noqa: SLF001


@open_
def test_a_specialisation_has_the_shape_of_its_kind(novel: Dimension) -> None:
    wrapped, unwrapped = _modular("Wrapped", novel), _linear("Unwrapped", novel)
    registry._register(novel, wrapped)  # noqa: SLF001
    with pytest.raises(TypeError, match="shape"):
        registry._register(novel, unwrapped, specialisation_of=wrapped)  # noqa: SLF001
    assert registry._kinds_of(novel) == (wrapped,)  # noqa: SLF001


# Contested kinds.


@open_
def test_two_contested_kinds_leave_the_dimension_without_a_principal(
    novel: Dimension,
) -> None:
    first, second = _linear("First", novel), _linear("Second", novel)
    registry._register(novel, first)  # noqa: SLF001
    registry._register(novel, second, contested_with=first)  # noqa: SLF001
    assert novel not in registry._DIMENSION_REGISTRY  # noqa: SLF001
    assert registry._CONTESTED[novel] == (first, second)  # noqa: SLF001
    assert registry._kinds_of(novel) == (first, second)  # noqa: SLF001


@open_
def test_a_third_contested_kind_joins_through_any_member(novel: Dimension) -> None:
    first, second, third = (_linear(n, novel) for n in ("First", "Second", "Third"))
    registry._register(novel, first)  # noqa: SLF001
    registry._register(novel, second, contested_with=first)  # noqa: SLF001
    registry._register(novel, third, contested_with=second)  # noqa: SLF001
    assert registry._CONTESTED[novel] == (first, second, third)  # noqa: SLF001


@open_
def test_a_specialisation_can_refine_a_contested_kind(novel: Dimension) -> None:
    first, second, role = (_linear(n, novel) for n in ("First", "Second", "Role"))
    registry._register(novel, first)  # noqa: SLF001
    registry._register(novel, second, contested_with=first)  # noqa: SLF001
    registry._register(novel, role, specialisation_of=second)  # noqa: SLF001
    assert registry._kinds_of(novel) == (first, second, role)  # noqa: SLF001


@open_
def test_only_linear_kinds_are_contested(novel: Dimension) -> None:
    first = _linear("First", novel)
    registry._register(novel, first)  # noqa: SLF001
    with pytest.raises(TypeError, match="only linear kinds"):
        registry._register(novel, _modular("Wrapped", novel), contested_with=first)  # noqa: SLF001
    assert registry._DIMENSION_REGISTRY[novel] is first  # noqa: SLF001


@open_
def test_a_contest_is_with_a_kind_arithmetic_could_produce(novel: Dimension) -> None:
    wrapped = _modular("Wrapped", novel)
    registry._register(novel, wrapped)  # noqa: SLF001
    with pytest.raises(TypeError, match="only linear kinds"):
        registry._register(novel, _linear("Linear", novel), contested_with=wrapped)  # noqa: SLF001


@open_
def test_a_contested_dimension_is_not_resolved_to_one_kind(novel: Dimension) -> None:
    first, second = _linear("First", novel), _linear("Second", novel)
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


# The registry closes only when every kind is catalogued.


def test_closing_a_second_time_does_nothing() -> None:
    registry._close()  # noqa: SLF001
    assert registry._closed is True  # noqa: SLF001


@pytest.mark.parametrize(
    "make",
    [
        lambda: _linear("Unregistered", FREQUENCY),
        lambda: _linear("Unregistered", DIMENSIONLESS),
        lambda: _modular("Unregistered", ANGLE),
    ],
    ids=["linear", "dimensionless", "modular"],
)
def test_closing_with_an_unregistered_kind_is_refused(
    monkeypatch: pytest.MonkeyPatch, make: Callable[[], type]
) -> None:
    kind = make()
    monkeypatch.setattr(registry, "_closed", False)
    with pytest.raises(TypeError, match="Unregistered"):
        registry._close()  # noqa: SLF001
    assert registry._closed is False  # noqa: SLF001
    del kind


def test_closing_with_every_kind_registered_succeeds(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(registry, "_closed", False)
    monkeypatch.setattr(registry, "_concrete_kinds", lambda: [Time, Angle, Instant])
    registry._close()  # noqa: SLF001
    assert registry._closed is True  # noqa: SLF001
