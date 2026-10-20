"""`extend_units` adds units to a bound type, with the checks `bind_units` applies."""

from fractions import Fraction

import pytest

from kuchka.dimensions import VOLTAGE
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.units import bind_units
from kuchka.quantities.base.units import extend_units
from kuchka.units import frequency
from kuchka.units import instant
from kuchka.units import voltage


def _bound_type() -> type[LinearQuantity]:
    class Fresh(LinearQuantity):
        dimension = VOLTAGE
        __slots__ = ()

    bind_units(Fresh, [voltage.VOLT])
    return Fresh


def test_extending_adds_the_units_beside_the_bound_ones() -> None:
    fresh = _bound_type()
    extend_units(fresh, [voltage.MILLIVOLT])
    assert fresh._applicable_units == {voltage.VOLT, voltage.MILLIVOLT}  # noqa: SLF001


def test_the_added_units_are_recorded_apart_from_the_bound_ones() -> None:
    fresh = _bound_type()
    extend_units(fresh, [voltage.VOLT, voltage.MILLIVOLT])
    assert fresh._extension_units == {voltage.MILLIVOLT}  # noqa: SLF001


def test_extending_twice_with_the_same_units_changes_nothing() -> None:
    fresh = _bound_type()
    extend_units(fresh, [voltage.MILLIVOLT])
    extend_units(fresh, [voltage.MILLIVOLT])
    assert fresh._applicable_units == {voltage.VOLT, voltage.MILLIVOLT}  # noqa: SLF001
    assert fresh._extension_units == {voltage.MILLIVOLT}  # noqa: SLF001


def test_a_type_displays_in_an_added_unit() -> None:
    fresh = _bound_type()
    extend_units(fresh, [voltage.MILLIVOLT])
    assert fresh(Fraction(1), voltage.MILLIVOLT).unit == voltage.MILLIVOLT


def test_extending_a_type_without_bound_units_is_refused() -> None:
    class Unbound(LinearQuantity):
        dimension = VOLTAGE
        __slots__ = ()

    with pytest.raises(TypeError, match="no bound units to extend"):
        extend_units(Unbound, [voltage.MILLIVOLT])


def test_extending_with_nothing_is_refused() -> None:
    with pytest.raises(TypeError, match="at least one unit"):
        extend_units(_bound_type(), [])


def test_extending_with_a_unit_of_another_dimension_is_refused() -> None:
    with pytest.raises(TypeError, match="dimension"):
        extend_units(_bound_type(), [frequency.HERTZ])


def test_extending_with_a_unit_of_another_kind_is_refused() -> None:
    with pytest.raises(TypeError, match="the kind of unit"):
        extend_units(_bound_type(), [instant.INSTANT_SECOND])


def test_a_refused_extension_leaves_the_type_as_it_was() -> None:
    fresh = _bound_type()
    with pytest.raises(TypeError, match="dimension"):
        extend_units(fresh, [voltage.MILLIVOLT, frequency.HERTZ])
    assert fresh._applicable_units == {voltage.VOLT}  # noqa: SLF001
    assert not hasattr(fresh, "_extension_units")
