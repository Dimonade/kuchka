"""What the registry holds, and how arithmetic resolves through it."""

from __future__ import annotations

import pytest

from kuchka import Frequency
from kuchka import Power
from kuchka import quantities
from kuchka.dimensions import FREQUENCY
from kuchka.dimensions import TIME
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base import registry
from kuchka.units import current
from kuchka.units.electromagnetics import voltage
from kuchka.units.temporal import frequency
from kuchka.units.temporal import time
from tests.support.kinds import QUANTITY_TYPES

REGISTERED = registry._DIMENSION_REGISTRY  # noqa: SLF001 -- inspected, never modified


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
    assert quantity_type in QUANTITY_TYPES
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


def test_a_product_comes_back_as_the_registered_type() -> None:
    assert isinstance(voltage.Volt(2) * current.Ampere(3), Power)


def test_a_reciprocal_comes_back_as_the_registered_type() -> None:
    assert isinstance(1 / time.Second(4), Frequency)
    assert 1 / time.Second(4) == frequency.Hertz(1) / 4
