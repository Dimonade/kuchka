"""The dimension registry is closed, and only kuchka's own modules fill it.

Arithmetic on quantities hands back the named type for the resulting dimension:
``Volt(2) * Ampere(3)`` is a `Power`.
Each quantity module registers its type while it is imported, and the registry closes
when the package has finished importing, so the named dimensions are part of the library
and the registration function is internal.
Registering a second type for a dimension that has one is refused unless the type
states its relation to the first, so a dimension always resolves to a single general
type: `Frequency` for the dimension shared with `SampleRate` and `BaudRate`.
"""

from __future__ import annotations

import pytest

import kuchka
from kuchka import Ampere
from kuchka import Frequency
from kuchka import Hertz
from kuchka import Power
from kuchka import Second
from kuchka import Volt
from kuchka import quantities
from kuchka.dimensions import FREQUENCY
from kuchka.dimensions import TIME
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base import registry
from tests.quantity_families import CONCRETE_QUANTITY_TYPES

REGISTERED = registry._DIMENSION_REGISTRY  # noqa: SLF001 -- inspected, never modified


class _Rogue(LinearQuantity):
    dimension = FREQUENCY
    __slots__ = ()


# The registration function is internal.


def test_the_function_is_not_exported_from_the_base_package() -> None:
    assert not hasattr(quantities.base, "register")


@pytest.mark.parametrize(
    "package", [kuchka, quantities, quantities.base, registry], ids=lambda p: p.__name__
)
def test_no_public_list_names_the_registration_function(package: object) -> None:
    exported = package.__all__  # type: ignore[attr-defined]  # ty: ignore[unresolved-attribute]
    assert not any("register" in name for name in exported)


def test_the_registry_module_exports_nothing() -> None:
    assert registry.__all__ == []


def test_the_registration_function_is_private_by_name() -> None:
    assert hasattr(registry, "_register")
    assert not hasattr(registry, "register")


# The registry closes when the package has been imported.


def test_the_registry_is_closed_once_the_package_has_imported() -> None:
    assert registry._closed is True  # noqa: SLF001


def test_a_registration_after_the_close_is_refused() -> None:
    with pytest.raises(RuntimeError, match="registry is closed"):
        registry._register(TIME, Second.__class__)  # type: ignore[arg-type]  # noqa: SLF001  # ty: ignore[invalid-argument-type]


def test_a_new_type_cannot_claim_a_dimension_after_the_close() -> None:
    class Newcomer(LinearQuantity):
        dimension = FREQUENCY
        __slots__ = ()

    with pytest.raises(RuntimeError, match="Newcomer"):
        registry._register(FREQUENCY, Newcomer)  # noqa: SLF001


def test_even_re_registering_the_same_type_is_refused_after_the_close() -> None:
    with pytest.raises(RuntimeError, match="registry is closed"):
        registry._register(FREQUENCY, Frequency)  # noqa: SLF001


def test_a_refused_registration_leaves_the_registry_unchanged() -> None:
    before = dict(REGISTERED)
    with pytest.raises(RuntimeError):
        registry._register(FREQUENCY, _Rogue)  # noqa: SLF001
    assert before == REGISTERED


def test_closing_is_one_way() -> None:
    registry._close()  # noqa: SLF001
    assert registry._closed is True  # noqa: SLF001


# The rules of registration, applied while the registry is open.


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


@pytest.mark.usefixtures("open_registry")
def test_a_second_type_for_a_registered_dimension_is_refused() -> None:
    with pytest.raises(TypeError, match="already registered"):
        registry._register(FREQUENCY, _Rogue)  # noqa: SLF001


@pytest.mark.usefixtures("open_registry")
def test_registering_the_same_type_again_is_not_an_error() -> None:
    registry._register(FREQUENCY, Frequency)  # noqa: SLF001


@pytest.mark.usefixtures("open_registry")
def test_a_refused_second_type_leaves_the_first_in_place() -> None:
    with pytest.raises(TypeError):
        registry._register(FREQUENCY, _Rogue)  # noqa: SLF001
    assert registry._DIMENSION_REGISTRY[FREQUENCY] is Frequency  # noqa: SLF001


@pytest.mark.usefixtures("open_registry")
def test_an_open_registry_accepts_a_new_dimension() -> None:
    novel = FREQUENCY * FREQUENCY

    class PerSecondSquared(LinearQuantity):
        dimension = novel
        __slots__ = ()

    registry._register(novel, PerSecondSquared)  # noqa: SLF001
    assert registry._DIMENSION_REGISTRY[novel] is PerSecondSquared  # noqa: SLF001
    assert novel not in REGISTERED


# What the registry holds.


def test_the_registry_is_populated() -> None:
    assert len(REGISTERED) > 15  # noqa: PLR2004 -- a floor, so it cannot silently empty


@pytest.mark.parametrize("dimension", list(REGISTERED), ids=repr)
def test_a_registered_type_names_the_dimension_it_is_registered_for(
    dimension: object,
) -> None:
    quantity_type = REGISTERED[dimension]  # type: ignore[index]  # ty: ignore[invalid-argument-type]
    assert quantity_type.dimension == dimension


@pytest.mark.parametrize("dimension", list(REGISTERED), ids=repr)
def test_a_registered_type_is_a_complete_concrete_linear_type(
    dimension: object,
) -> None:
    quantity_type = REGISTERED[dimension]  # type: ignore[index]  # ty: ignore[invalid-argument-type]
    assert quantity_type in CONCRETE_QUANTITY_TYPES
    assert issubclass(quantity_type, LinearQuantity)
    assert quantity_type._canonical_unit.dimension == dimension  # noqa: SLF001


def test_no_planned_dimension_is_also_registered() -> None:
    assert not set(registry._PLANNED_DIMENSIONS) & set(REGISTERED)  # noqa: SLF001


def test_each_registered_type_is_registered_once() -> None:
    types = list(REGISTERED.values())
    assert len(types) == len(set(types))


def test_the_dimension_shared_by_the_rate_types_belongs_to_the_general_one() -> None:
    assert REGISTERED[FREQUENCY] is Frequency
    assert quantities.SampleRate not in REGISTERED.values()
    assert quantities.BaudRate not in REGISTERED.values()


def test_the_dimension_shared_by_time_types_belongs_to_the_general_one() -> None:
    assert REGISTERED[TIME] is quantities.Time
    assert quantities.SamplingPeriod not in REGISTERED.values()


# Arithmetic resolves through the registry.


def test_a_product_comes_back_as_the_registered_type() -> None:
    assert isinstance(Volt(2) * Ampere(3), Power)


def test_a_reciprocal_comes_back_as_the_registered_type() -> None:
    assert isinstance(1 / Second(4), Frequency)
    assert 1 / Second(4) == Hertz(1) / 4
