"""A ladder is a run of bound units that grow, and a type binds its ladders once.

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
from kuchka.quantities.base.units import bind_ladders
from kuchka.quantities.base.units import bind_units
from tests.support.synthetic import linear_kind
from tests.support.synthetic import modular_kind

SHELL = UnitDef("shell", "sh", Fraction(3, 100), LENGTH)
KILOSHELL = UnitDef("kiloshell", "ksh", 30, LENGTH)
MEGASHELL = UnitDef("megashell", "Msh", 30_000, LENGTH)
ZERO_KELVIN = AffineUnitDef("warm_kelvin", "wK", 1, 0)
OFFSET_DEGREE = AffineUnitDef("warm_degree", "w°", 1, Fraction(27315, 100))


def ladders_of(cls: type) -> tuple[tuple[UnitDef, ...], ...]:
    """Return the ladders a type binds."""
    return cls._ladders


def ladder_of(cls: type) -> dict[object, tuple[UnitDef, ...]]:
    """Return the ladder each unit of a type stands on."""
    return cls._ladder_of


def made_up_linear() -> type:
    """Return a new linear type with its units bound."""
    kind = linear_kind("Shells", LENGTH)
    bind_units(kind, (SHELL, KILOSHELL, MEGASHELL))
    return kind


def test_a_type_binds_its_ladders_and_each_unit_knows_its_ladder() -> None:
    kind = made_up_linear()
    bind_ladders(kind, [(SHELL, KILOSHELL)])
    assert ladders_of(kind) == ((SHELL, KILOSHELL),)
    assert ladder_of(kind)[SHELL] == (SHELL, KILOSHELL)
    assert ladder_of(kind)[KILOSHELL] == (SHELL, KILOSHELL)
    assert MEGASHELL not in ladder_of(kind)


def test_a_type_has_several_ladders_that_share_no_unit() -> None:
    half = UnitDef("half_shell", "hsh", Fraction(1, 2), LENGTH)
    kind = linear_kind("Fishes", LENGTH)
    bind_units(kind, (SHELL, KILOSHELL, half, MEGASHELL))
    bind_ladders(kind, [(SHELL, KILOSHELL), (half, MEGASHELL)])
    assert ladder_of(kind)[half] == (half, MEGASHELL)
    assert ladder_of(kind)[SHELL] == (SHELL, KILOSHELL)


def test_a_type_binds_its_ladders_once() -> None:
    kind = made_up_linear()
    bind_ladders(kind, [(SHELL, KILOSHELL)])
    with pytest.raises(TypeError, match="already has its ladders bound"):
        bind_ladders(kind, [(SHELL, KILOSHELL)])


def test_ladders_are_built_from_bound_units() -> None:
    kind = linear_kind("Unbound", LENGTH)
    with pytest.raises(TypeError, match="no bound units"):
        bind_ladders(kind, [(SHELL, KILOSHELL)])


def test_a_type_needs_a_ladder() -> None:
    with pytest.raises(TypeError, match="at least one ladder"):
        bind_ladders(made_up_linear(), [])


def test_a_ladder_of_one_unit_is_refused() -> None:
    with pytest.raises(TypeError, match="at least two units"):
        bind_ladders(made_up_linear(), [(SHELL,)])


def test_a_unit_the_type_does_not_display_in_is_refused() -> None:
    stranger = UnitDef("stranger", "str", 7, LENGTH)
    with pytest.raises(TypeError, match="is not a unit of Shells"):
        bind_ladders(made_up_linear(), [(SHELL, stranger)])


@pytest.mark.parametrize(
    "ladder",
    [(KILOSHELL, SHELL), (SHELL, SHELL), (SHELL, MEGASHELL, KILOSHELL)],
    ids=["descending", "equal", "dips"],
)
def test_a_ladder_that_does_not_grow_is_refused(ladder: tuple[UnitDef, ...]) -> None:
    kind = made_up_linear()
    with pytest.raises(TypeError, match=r"more than one ladder|grows from each unit"):
        bind_ladders(kind, [ladder])


def test_a_unit_on_two_ladders_is_refused() -> None:
    with pytest.raises(TypeError, match="more than one ladder"):
        bind_ladders(made_up_linear(), [(SHELL, KILOSHELL), (KILOSHELL, MEGASHELL)])


def test_a_shape_whose_magnitude_is_no_size_has_no_ladders() -> None:
    kind = modular_kind("Turns", LENGTH)
    bind_units(kind, (SHELL, KILOSHELL))
    with pytest.raises(TypeError, match="no ladders"):
        bind_ladders(kind, [(SHELL, KILOSHELL)])


def test_a_unit_that_starts_away_from_zero_is_refused() -> None:
    kind = type(
        "Warmth",
        (AffineQuantity,),
        {"dimension": TEMPERATURE_DELTA, "__slots__": ()},
    )
    bind_units(kind, (ZERO_KELVIN, OFFSET_DEGREE))
    with pytest.raises(TypeError, match="starts its scale away from zero"):
        bind_ladders(kind, [(ZERO_KELVIN, OFFSET_DEGREE)])
