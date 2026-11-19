"""The clock units of a type are bound units that shrink, and a type binds them once.

The types here are made up, so that each rule is broken in a way the library's own
units never do.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka.dimensions import LENGTH
from kuchka.dimensions import TEMPERATURE_DELTA
from kuchka.quantities.base import AffineQuantity
from kuchka.quantities.base import AffineUnitDef
from kuchka.quantities.base import UnitDef
from kuchka.quantities.base.units import bind_clock_units
from kuchka.quantities.base.units import bind_units
from tests.support.synthetic import linear_kind

LEAGUE = UnitDef("league", "lg", 4000, LENGTH)
FURLONG = UnitDef("furlong", "fur", 200, LENGTH)
SHELL = UnitDef("shell", "sh", Fraction(3, 100), LENGTH)
ZERO_KELVIN = AffineUnitDef("warm_kelvin", "wK", 1, 0)
OFFSET_DEGREE = AffineUnitDef("warm_degree", "w°", 1, Fraction(27315, 100))


def clock_units_of(cls: type) -> tuple[UnitDef, ...]:
    """Return the clock units a type binds."""
    return cls._clock_units


def made_up() -> type:
    """Return a new linear type with its units bound."""
    kind = linear_kind("Leagues", LENGTH)
    bind_units(kind, (LEAGUE, FURLONG, SHELL))
    return kind


def test_a_type_binds_its_clock_units_largest_first() -> None:
    kind = made_up()
    bind_clock_units(kind, [LEAGUE, FURLONG, SHELL])
    assert clock_units_of(kind) == (LEAGUE, FURLONG, SHELL)


def test_a_type_binds_its_clock_units_once() -> None:
    kind = made_up()
    bind_clock_units(kind, [LEAGUE, FURLONG])
    with pytest.raises(TypeError, match="already has its clock units bound"):
        bind_clock_units(kind, [LEAGUE, FURLONG])


def test_clock_units_are_built_from_bound_units() -> None:
    with pytest.raises(TypeError, match="no bound units"):
        bind_clock_units(linear_kind("Unbound", LENGTH), [LEAGUE, FURLONG])


def test_a_single_clock_unit_is_refused() -> None:
    with pytest.raises(TypeError, match="at least two units"):
        bind_clock_units(made_up(), [LEAGUE])


def test_a_unit_the_type_does_not_display_in_is_refused() -> None:
    stranger = UnitDef("stranger", "str", 7, LENGTH)
    with pytest.raises(TypeError, match="is not a unit of Leagues"):
        bind_clock_units(made_up(), [LEAGUE, stranger])


@pytest.mark.parametrize(
    "units",
    [[FURLONG, LEAGUE], [LEAGUE, LEAGUE], [LEAGUE, SHELL, FURLONG]],
    ids=["growing", "equal", "dips"],
)
def test_units_that_do_not_shrink_are_refused(units: list[UnitDef]) -> None:
    with pytest.raises(TypeError, match="shrink from each unit"):
        bind_clock_units(made_up(), units)


def test_a_unit_that_starts_away_from_zero_is_refused() -> None:
    kind = type(
        "Warmth",
        (AffineQuantity,),
        {"dimension": TEMPERATURE_DELTA, "__slots__": ()},
    )
    bind_units(kind, (ZERO_KELVIN, OFFSET_DEGREE))
    with pytest.raises(TypeError, match="starts its scale away from zero"):
        bind_clock_units(kind, [OFFSET_DEGREE, ZERO_KELVIN])
