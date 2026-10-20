"""The German miles are split into principal and regional tiers that join cleanly."""

from __future__ import annotations

from kuchka.internal.unit_table import units_of
from kuchka.units.archaic.german.length import meile
from kuchka.units.archaic.german.length import regional_meilen as regional


def test_the_principal_and_regional_tiers_share_no_unit() -> None:
    principal = set(units_of(meile.GERMAN_MEILE_UNITS))
    regionals = set(units_of(regional.GERMAN_REGIONAL_MEILE_UNITS))
    assert not principal & regionals


def test_the_joint_table_is_the_union_of_the_tiers() -> None:
    principal = set(units_of(meile.GERMAN_MEILE_UNITS))
    regionals = set(units_of(regional.GERMAN_REGIONAL_MEILE_UNITS))
    assert set(units_of(regional.GERMAN_MEILE_UNITS_ALL)) == principal | regionals


def test_the_principal_miles_are_the_four_recurring_ones() -> None:
    names = {unit.name for unit in units_of(meile.GERMAN_MEILE_UNITS)}
    assert names == {
        "geographische_meile",
        "preussische_landmeile",
        "reichsmeile",
        "oesterreichische_meile",
    }


def test_a_bare_meile_names_no_unit() -> None:
    for spelling in ("Meile", "Landmeile"):
        for table in (meile.GERMAN_MEILE_UNITS, regional.GERMAN_MEILE_UNITS_ALL):
            try:
                table[spelling]
            except KeyError:
                continue
            raise AssertionError(spelling)
