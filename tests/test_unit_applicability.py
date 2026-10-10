"""A unit belongs to the quantity types that display in it.

Two quantity types can share a dimension without sharing units: `Frequency` has the
hertz, `BaudRate` the baud, and `SampleRate` the sample per second, all of dimension
time to the minus one.
Each concrete type binds the units it displays in, from its own `*_UNITS` table, and
both its constructor and `.to()` refuse any other, including a unit of a type with the
same dimension.
A unit may belong to several types: the second is a unit of `Time` and of
`SamplingPeriod`.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any

import pytest

import kuchka.units as published
from kuchka import BaudRate
from kuchka import Frequency
from kuchka import Hertz
from kuchka import InvalidConversionError
from kuchka import InvalidMeasurementError
from kuchka import Millisecond
from kuchka import SampleRate
from kuchka import SamplingPeriod
from kuchka import Second
from kuchka import Time
from kuchka import Volt
from kuchka import Voltage
from kuchka.dimensions import VOLTAGE
from kuchka.internal.unit_table import UnitTable
from kuchka.internal.unit_table import units_of
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.units import bind_units
from kuchka.units import BAUD
from kuchka.units import HERTZ
from kuchka.units import INSTANT_SECOND
from kuchka.units import MILLISECOND
from kuchka.units import SAMPLES_PER_SECOND
from kuchka.units import SECOND
from kuchka.units import VOLT
from tests.quantity_families import CONCRETE_QUANTITY_TYPES
from tests.quantity_families import sample_of

TABLES = {
    name: getattr(published, name)
    for name in sorted(published.__all__)
    if isinstance(getattr(published, name), UnitTable)
}
TABLE_OF = {type(next(iter(table.values()))(1)): table for table in TABLES.values()}


def _type_id(cls: type) -> str:
    return str(cls.__name__)


TYPES: list[Any] = list(CONCRETE_QUANTITY_TYPES)


def _shared_dimension_pairs() -> list[tuple[Any, Any]]:
    return [
        (first, second)
        for first in TYPES
        for second in TYPES
        if first is not second and first.dimension == second.dimension
    ]


PAIRS = _shared_dimension_pairs()
PAIR_IDS = [f"{a.__name__}-{b.__name__}" for a, b in PAIRS]


# Every concrete type is bound.


@pytest.mark.parametrize("cls", TYPES, ids=_type_id)
def test_every_concrete_type_binds_its_units(cls: type[Any]) -> None:
    assert "_applicable_units" in vars(cls), f"{cls.__name__} has no bound units"
    assert cls._applicable_units


@pytest.mark.parametrize("cls", TYPES, ids=_type_id)
def test_the_bound_units_are_of_the_kind_and_dimension_of_the_type(
    cls: type[Any],
) -> None:
    for unit in cls._applicable_units:
        assert isinstance(unit, cls._unit_type)
        if hasattr(unit, "dimension"):
            assert unit.dimension == cls.dimension


@pytest.mark.parametrize("cls", TYPES, ids=_type_id)
def test_the_canonical_unit_is_one_of_the_bound_units(cls: type[Any]) -> None:
    canonical = getattr(cls, "_canonical_unit", None)
    if canonical is not None:
        assert canonical in cls._applicable_units


@pytest.mark.parametrize("cls", TYPES, ids=_type_id)
def test_a_value_of_the_type_displays_in_a_bound_unit(cls: type[Any]) -> None:
    assert sample_of(cls).unit in cls._applicable_units


TABLED: list[Any] = sorted(TABLE_OF, key=lambda cls: str(cls.__name__))


@pytest.mark.parametrize("cls", TABLED, ids=_type_id)
def test_every_constructor_of_a_table_builds_a_value_in_a_bound_unit(
    cls: type[Any],
) -> None:
    for constructor in TABLE_OF[cls].values():
        value = constructor(1)
        assert type(value) is cls
        assert value.unit in cls._applicable_units


@pytest.mark.parametrize(
    "cls",
    [
        c
        for c in sorted(TABLE_OF, key=lambda cls: str(cls.__name__))
        if c.__name__ != "Instant"
    ],
    ids=_type_id,
)
def test_every_unit_of_a_table_is_bound_to_its_type(cls: type[Any]) -> None:
    assert set(units_of(TABLE_OF[cls])) == set(cls._applicable_units)


# A type with the same dimension does not lend its units.


@pytest.mark.parametrize(("first", "second"), PAIRS, ids=PAIR_IDS)
def test_a_unit_only_the_other_type_displays_in_is_refused(
    first: type[Any], second: type[Any]
) -> None:
    only_second = [
        unit
        for unit in second._applicable_units  # noqa: SLF001
        if unit not in first._applicable_units  # noqa: SLF001
        and isinstance(unit, first._unit_type)  # noqa: SLF001
    ]
    for unit in only_second:
        with pytest.raises(InvalidMeasurementError, match="is not a unit of"):
            first(Fraction(1), unit)


def test_the_types_sharing_a_dimension_are_found() -> None:
    names = {frozenset((a.__name__, b.__name__)) for a, b in PAIRS}
    assert frozenset(("Frequency", "BaudRate")) in names
    assert frozenset(("Frequency", "SampleRate")) in names
    assert frozenset(("Time", "SamplingPeriod")) in names


# The reported cases.


def test_a_frequency_is_not_displayed_in_baud() -> None:
    with pytest.raises(InvalidConversionError, match="is not a unit of Frequency"):
        Hertz(1).to(BAUD)


def test_a_frequency_is_not_displayed_in_samples_per_second() -> None:
    with pytest.raises(InvalidConversionError):
        Hertz(1).to(SAMPLES_PER_SECOND)


def test_a_baud_rate_is_not_displayed_in_hertz() -> None:
    with pytest.raises(InvalidConversionError, match="is not a unit of BaudRate"):
        BaudRate(Fraction(1), BAUD).to(HERTZ)


def test_the_class_constructor_refuses_a_unit_of_a_sibling_type() -> None:
    with pytest.raises(InvalidMeasurementError, match="is not a unit of Frequency"):
        Frequency(Fraction(1), BAUD)


def test_the_message_names_the_type_the_unit_belongs_to() -> None:
    with pytest.raises(InvalidMeasurementError, match="It is a unit of BaudRate"):
        Frequency(Fraction(1), BAUD)
    with pytest.raises(InvalidConversionError, match="It is a unit of Frequency"):
        BaudRate(Fraction(1), BAUD).to(HERTZ)


def test_the_conversion_message_names_both_units() -> None:
    with pytest.raises(InvalidConversionError) as caught:
        Hertz(1).to(BAUD)
    assert "Hz" in str(caught.value)
    assert "Bd" in str(caught.value)


def test_a_unit_that_belongs_to_no_type_names_no_owner() -> None:
    from kuchka.quantities.base import UnitDef

    stray = UnitDef("stray", "st", 1, Frequency.dimension)
    with pytest.raises(InvalidMeasurementError) as caught:
        Frequency(Fraction(1), stray)
    assert str(caught.value) == "stray (st) is not a unit of Frequency."


# A shared unit is a unit of every type that binds it.


def test_the_second_is_a_unit_of_time_and_of_sampling_period() -> None:
    assert SECOND in Time._applicable_units  # noqa: SLF001
    assert SECOND in SamplingPeriod._applicable_units  # noqa: SLF001


def test_a_time_and_a_sampling_period_display_in_milliseconds() -> None:
    assert Second(1).to(MILLISECOND).value_in(MILLISECOND) == Fraction(1000)
    period = Second(1).to_sampling_period()
    assert period.to(MILLISECOND).value_in(MILLISECOND) == Fraction(1000)


def test_an_instant_displays_only_in_the_instant_second() -> None:
    from kuchka import Instant

    assert Instant._applicable_units == frozenset({INSTANT_SECOND})  # noqa: SLF001


# Everything that worked still works.


def test_a_unit_of_the_type_converts_as_before() -> None:
    assert Volt(5).to(published.MILLIVOLT).value_in(published.MILLIVOLT) == 5000  # noqa: PLR2004
    assert Hertz(1000).to(published.KILOHERTZ).value_in(published.KILOHERTZ) == 1


def test_a_foreign_dimension_still_reports_incompatible_dimensions() -> None:
    with pytest.raises(InvalidMeasurementError, match="incompatible dimensions"):
        Frequency(Fraction(1), VOLT)
    with pytest.raises(InvalidConversionError, match="incompatible dimensions"):
        Hertz(1).to(VOLT)


# `bind_units`.


def _fresh_type() -> type[LinearQuantity]:
    class Fresh(LinearQuantity):
        dimension = VOLTAGE
        __slots__ = ()

    return Fresh


def test_binding_sets_the_applicable_units() -> None:
    fresh = _fresh_type()
    bind_units(fresh, [VOLT])
    assert fresh._applicable_units == frozenset({VOLT})  # noqa: SLF001


def test_a_type_binds_once() -> None:
    fresh = _fresh_type()
    bind_units(fresh, [VOLT])
    with pytest.raises(TypeError, match="already has its units bound"):
        bind_units(fresh, [VOLT])


def test_binding_nothing_is_refused() -> None:
    with pytest.raises(TypeError, match="at least one unit"):
        bind_units(_fresh_type(), [])


def test_binding_a_unit_of_another_dimension_is_refused() -> None:
    with pytest.raises(TypeError, match="dimension"):
        bind_units(_fresh_type(), [HERTZ])


def test_binding_a_unit_of_another_kind_is_refused() -> None:
    with pytest.raises(TypeError, match="the kind of unit"):
        bind_units(_fresh_type(), [INSTANT_SECOND])


def test_two_types_may_bind_the_same_unit() -> None:
    first, second = _fresh_type(), _fresh_type()
    bind_units(first, [VOLT])
    bind_units(second, [VOLT])
    assert VOLT in first._applicable_units  # noqa: SLF001
    assert VOLT in second._applicable_units  # noqa: SLF001


def test_a_type_that_is_not_yet_bound_checks_only_kind_and_dimension() -> None:
    fresh = _fresh_type()
    assert fresh(Fraction(1), VOLT).magnitude == Fraction(1)


def test_the_published_voltage_type_is_unchanged_by_the_throwaway_types() -> None:
    assert VOLT in Voltage._applicable_units  # noqa: SLF001
    assert Volt(1).unit is VOLT


def test_units_of_refuses_a_table_that_is_not_built_by_unit_table() -> None:
    with pytest.raises(TypeError, match="not a table built by unit_table"):
        units_of({"V": Volt})


def test_sample_rate_and_frequency_do_not_exchange_units_through_to() -> None:
    rate = SampleRate(Fraction(44100), SAMPLES_PER_SECOND)
    with pytest.raises(InvalidConversionError):
        rate.to(HERTZ)


def test_millisecond_constructor_still_builds_a_time() -> None:
    assert Millisecond(5) == Second(Fraction(5, 1000))
