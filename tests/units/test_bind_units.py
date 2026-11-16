"""`bind_units` binds the units a type displays in, once, and checks them."""

from fractions import Fraction

import pytest

from kuchka import InvalidConversionError
from kuchka import SampleRate
from kuchka import Voltage
from kuchka.dimensions import VOLTAGE
from kuchka.internal.unit_table import units_of
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.units import bind_units
from kuchka.units.electromagnetics import voltage
from kuchka.units.temporal import frequency
from kuchka.units.temporal import instant
from kuchka.units.temporal import sample_rate
from kuchka.units.temporal import time


def _fresh_type() -> type[LinearQuantity]:
    class Fresh(LinearQuantity):
        dimension = VOLTAGE
        __slots__ = ()

    return Fresh


def test_binding_sets_the_applicable_units() -> None:
    fresh = _fresh_type()
    bind_units(fresh, [voltage.VOLT])
    assert fresh._applicable_units == frozenset({voltage.VOLT})  # noqa: SLF001


def test_a_type_binds_once() -> None:
    fresh = _fresh_type()
    bind_units(fresh, [voltage.VOLT])
    with pytest.raises(TypeError, match="already has its units bound"):
        bind_units(fresh, [voltage.VOLT])


def test_binding_nothing_is_refused() -> None:
    with pytest.raises(TypeError, match="at least one unit"):
        bind_units(_fresh_type(), [])


def test_binding_a_unit_of_another_dimension_is_refused() -> None:
    with pytest.raises(TypeError, match="dimension"):
        bind_units(_fresh_type(), [frequency.HERTZ])


def test_binding_a_unit_of_another_kind_is_refused() -> None:
    with pytest.raises(TypeError, match="the kind of unit"):
        bind_units(_fresh_type(), [instant.INSTANT_SECOND])


def test_two_types_may_bind_the_same_unit() -> None:
    first, second = _fresh_type(), _fresh_type()
    bind_units(first, [voltage.VOLT])
    bind_units(second, [voltage.VOLT])
    assert voltage.VOLT in first._applicable_units  # noqa: SLF001
    assert voltage.VOLT in second._applicable_units  # noqa: SLF001


def test_a_type_that_is_not_yet_bound_checks_only_kind_and_dimension() -> None:
    fresh = _fresh_type()
    assert fresh(Fraction(1), voltage.VOLT).magnitude == Fraction(1)


def test_the_published_voltage_type_is_unchanged_by_the_throwaway_types() -> None:
    assert voltage.VOLT in Voltage._applicable_units  # noqa: SLF001
    assert voltage.Volt(1).unit is voltage.VOLT


def test_units_of_refuses_a_table_that_is_not_built_by_unit_table() -> None:
    with pytest.raises(TypeError, match="not a table built by unit_table"):
        units_of({"V": voltage.Volt})


def test_sample_rate_and_frequency_do_not_exchange_units_through_to() -> None:
    rate = SampleRate(Fraction(44100), sample_rate.SAMPLES_PER_SECOND)
    with pytest.raises(InvalidConversionError):
        rate.to(frequency.HERTZ)


def test_millisecond_constructor_still_builds_a_time() -> None:
    assert time.Millisecond(5) == time.Second(Fraction(5, 1000))
