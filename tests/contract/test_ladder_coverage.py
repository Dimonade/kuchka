"""Every quantity type whose size picks a unit has ladders, or a reason for none.

A type that is in neither place fails here, so adding a quantity is a deliberate
decision about its ladders.
The ladders of a type are its families of prefixed units, found from the symbols:
a family that is not a ladder, or a ladder that is no family, fails here as well.
Shapes whose magnitude is no size, the modular and the logarithmic, have no ladders.
The types are the ones the library publishes.
"""

from __future__ import annotations

import pytest

from tests.support.kinds import QUANTITY_TYPES
from tests.support.prefix_families import binary_families
from tests.support.prefix_families import decimal_families

MINIMUM_FAMILY = 2

NOT_PREFIXED = "its units are not prefixed in steps of a thousand"
BY_A_MILLION = "its prefixed units step by a million or more"
NO_LADDER = {
    "AngularAcceleration": NOT_PREFIXED,
    "AngularDisplacement": NOT_PREFIXED,
    "AngularJerk": NOT_PREFIXED,
    "AngularMomentum": NOT_PREFIXED,
    "AngularVelocity": NOT_PREFIXED,
    "AngularVelocitySquared": NOT_PREFIXED,
    "Area": BY_A_MILLION,
    "EntitiesPerAmount": NOT_PREFIXED,
    "FirstMomentOfMass": NOT_PREFIXED,
    "HeatingRate": NOT_PREFIXED,
    "Instant": "a point in time, whose unit starts away from zero",
    "KinematicViscosity": BY_A_MILLION,
    "LuminousEfficacy": NOT_PREFIXED,
    "LuminousEnergy": NOT_PREFIXED,
    "LuminousIntensity": NOT_PREFIXED,
    "MolarVolume": NOT_PREFIXED,
    "Momentum": NOT_PREFIXED,
    "Proportion": NOT_PREFIXED,
    "TimeCubed": BY_A_MILLION,
    "TimeFourthPower": BY_A_MILLION,
    "TimeSquared": BY_A_MILLION,
    "Velocity": NOT_PREFIXED,
    "VelocitySquared": BY_A_MILLION,
}
"""The types without ladders, and why."""


def has_ladders(cls: type) -> bool:
    """Return whether `cls` binds ladders of its own."""
    return bool(vars(cls).get("_ladders"))


def prefix_families(cls: type) -> list[set]:
    """Return the sets of units of `cls` that form a family of two or more."""
    found = [
        {*family.values()}
        for family in (
            *decimal_families(cls._applicable_units).values(),
            *binary_families(cls._applicable_units).values(),
        )
    ]
    return [members for members in found if len(members) >= MINIMUM_FAMILY]


SIZED = [cls for cls in QUANTITY_TYPES if cls._scales_by_size]
SIZED_IDS = [cls.__name__ for cls in SIZED]
LADDERED = [cls for cls in SIZED if has_ladders(cls)]
LADDERED_IDS = [cls.__name__ for cls in LADDERED]
UNSIZED = [cls for cls in QUANTITY_TYPES if not cls._scales_by_size]
UNSIZED_IDS = [cls.__name__ for cls in UNSIZED]
REASONED = [cls for cls in SIZED if cls.__name__ in NO_LADDER]
REASONED_IDS = [cls.__name__ for cls in REASONED]


@pytest.mark.parametrize("cls", SIZED, ids=SIZED_IDS)
def test_a_type_has_ladders_or_a_reason(cls: type) -> None:
    assert has_ladders(cls) or cls.__name__ in NO_LADDER, (
        f"{cls.__name__} has no ladder: bind one, or give the reason in NO_LADDER"
    )


def test_the_reasons_name_only_types_that_need_one() -> None:
    assert set(NO_LADDER) <= {cls.__name__ for cls in SIZED}


@pytest.mark.parametrize("cls", REASONED, ids=REASONED_IDS)
def test_a_type_with_a_reason_has_no_ladder_and_no_family(cls: type) -> None:
    assert not has_ladders(cls), f"{cls.__name__} has ladders: drop its reason"
    if cls.__name__ != "Instant":
        assert not prefix_families(cls), (
            f"{cls.__name__} has a family of prefixed units: bind a ladder for it"
        )


@pytest.mark.parametrize("cls", UNSIZED, ids=UNSIZED_IDS)
def test_a_shape_whose_magnitude_is_no_size_has_no_ladder(cls: type) -> None:
    assert not has_ladders(cls)


@pytest.mark.parametrize("cls", LADDERED, ids=LADDERED_IDS)
def test_the_ladders_of_a_type_hold_only_its_own_units(cls: type) -> None:
    on_a_ladder = [unit for ladder in cls._ladders for unit in ladder]
    assert len(on_a_ladder) == len(set(on_a_ladder))
    assert set(on_a_ladder) == set(cls._ladder_of)
    assert set(on_a_ladder) <= cls._applicable_units
    for ladder in cls._ladders:
        assert len(ladder) >= MINIMUM_FAMILY
        assert all(cls._ladder_of[unit] == ladder for unit in ladder)
        scales = [unit.scale for unit in ladder]
        assert scales == sorted(set(scales))
        assert all(getattr(unit, "offset", 0) == 0 for unit in ladder)


@pytest.mark.parametrize("cls", LADDERED, ids=LADDERED_IDS)
def test_the_ladders_of_a_type_are_its_families_of_prefixed_units(cls: type) -> None:
    families = prefix_families(cls)
    for ladder in cls._ladders:
        assert any(set(ladder) <= family for family in families), (
            f"{cls.__name__}: {[unit.symbol for unit in ladder]} is no family"
        )
    on_a_ladder = set(cls._ladder_of)
    for family in families:
        left_out = {
            unit for unit in family - on_a_ladder if getattr(unit, "offset", 0) == 0
        }
        assert not left_out, (
            f"{cls.__name__}: {sorted(unit.symbol for unit in left_out)} are in a "
            "family of prefixed units but on no ladder"
        )
