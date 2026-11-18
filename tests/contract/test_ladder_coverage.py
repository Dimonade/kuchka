"""Every quantity type whose size picks a unit has a ladder, or a reason for none.

A type that is not listed in either place fails here, so adding a quantity is a
deliberate decision about its ladder.
Shapes whose magnitude is no size, the modular and the logarithmic, have no ladders.
The types are the ones the library publishes.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.support.kinds import QUANTITY_TYPES

BASELINE = Path(__file__).with_name("ladder_baseline.txt")
MINIMUM_LADDER = 2

NO_LADDER = {
    "Instant": "a point in time, whose unit starts away from zero",
}
"""The types that cannot have a ladder, and why."""


def baseline() -> set[str]:
    """Return the names of the types that have no ladder yet."""
    lines = (line.strip() for line in BASELINE.read_text(encoding="utf-8").splitlines())
    return {line for line in lines if line and not line.startswith("#")}


def has_ladders(cls: type) -> bool:
    """Return whether `cls` binds ladders of its own."""
    return bool(vars(cls).get("_ladders"))


SIZED = [cls for cls in QUANTITY_TYPES if cls._scales_by_size]
SIZED_IDS = [cls.__name__ for cls in SIZED]
LADDERED = [cls for cls in SIZED if has_ladders(cls)]
LADDERED_IDS = [cls.__name__ for cls in LADDERED]
UNSIZED = [cls for cls in QUANTITY_TYPES if not cls._scales_by_size]
UNSIZED_IDS = [cls.__name__ for cls in UNSIZED]
LISTED = [cls for cls in SIZED if cls.__name__ in baseline()]
LISTED_IDS = [cls.__name__ for cls in LISTED]


@pytest.mark.parametrize("cls", SIZED, ids=SIZED_IDS)
def test_a_type_has_a_ladder_or_is_listed(cls: type) -> None:
    name = cls.__name__
    assert has_ladders(cls) or name in NO_LADDER or name in baseline(), (
        f"{name} has no ladder: bind one, or give the reason in NO_LADDER"
    )


@pytest.mark.parametrize("cls", LISTED, ids=LISTED_IDS)
def test_a_type_in_the_baseline_still_has_no_ladder(cls: type) -> None:
    assert not has_ladders(cls), (
        f"{cls.__name__} has a ladder: remove it from the baseline"
    )


def test_the_baseline_lists_only_types_that_need_a_ladder() -> None:
    assert baseline() <= {cls.__name__ for cls in SIZED}
    assert baseline().isdisjoint(NO_LADDER)


@pytest.mark.parametrize("name", sorted(NO_LADDER))
def test_a_type_with_a_reason_has_no_ladder(name: str) -> None:
    (cls,) = (cls for cls in SIZED if cls.__name__ == name)
    assert not has_ladders(cls)


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
        assert len(ladder) >= MINIMUM_LADDER
        assert all(cls._ladder_of[unit] == ladder for unit in ladder)
        scales = [unit.scale for unit in ladder]
        assert scales == sorted(set(scales))
        assert all(getattr(unit, "offset", 0) == 0 for unit in ladder)
