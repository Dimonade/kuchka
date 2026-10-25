"""`bind_table` binds the table that reads the text of a unit into a type, once."""

from __future__ import annotations

import pytest

from kuchka import Voltage
from kuchka.dimensions import VOLTAGE
from kuchka.internal.unit_table import unit_table
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.units import bind_table
from kuchka.units.electromagnetics import voltage
from tests.units.table_fixtures import TABLE


def _fresh_type() -> type[LinearQuantity]:
    class Fresh(LinearQuantity):
        dimension = VOLTAGE
        __slots__ = ()

    return Fresh


def test_binding_sets_the_table_of_the_type() -> None:
    fresh = _fresh_type()
    bind_table(fresh, TABLE)
    assert fresh._unit_table is TABLE  # noqa: SLF001


def test_a_type_binds_its_table_once() -> None:
    fresh = _fresh_type()
    bind_table(fresh, TABLE)
    with pytest.raises(TypeError, match="already has its table bound"):
        bind_table(fresh, TABLE)


@pytest.mark.parametrize("not_a_table", [{}, {"V": voltage.Volt}, [], None, "V"])
def test_something_that_unit_table_did_not_build_is_refused(
    not_a_table: object,
) -> None:
    with pytest.raises(TypeError, match="not a table built by unit_table"):
        bind_table(_fresh_type(), not_a_table)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_a_type_of_the_library_has_the_published_table_of_its_units() -> None:
    assert Voltage._unit_table is voltage.VOLTAGE_UNITS  # noqa: SLF001


def test_each_type_binds_its_own_table_and_not_the_table_of_a_parent() -> None:
    fresh = _fresh_type()
    assert "_unit_table" not in vars(fresh)
    bind_table(fresh, unit_table("EMPTY_UNITS", {}))
    assert "_unit_table" in vars(fresh)
