"""Activity per volume, per mass, and per area: what radon, soil, and wipes report.

The principal kinds take their products with `Activity`, a role, through rules.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import Activity
from kuchka import ActivityConcentration
from kuchka import Gray
from kuchka import Hertz
from kuchka import IncompatibleDimensionError
from kuchka import Kilogram
from kuchka import Metre
from kuchka import SpecificActivity
from kuchka import SurfaceActivity
from kuchka import parse
from kuchka.units.geometry.area import SquareCentimetre
from kuchka.units.geometry.area import SquareMetre
from kuchka.units.geometry.volume import CubicMetre
from kuchka.units.geometry.volume import Litre
from kuchka.units.radiation import activity
from kuchka.units.radiation import activity_concentration as ac
from kuchka.units.radiation import specific_activity as sa
from kuchka.units.radiation import surface_activity as su


def test_an_activity_over_a_volume_is_a_concentration_and_back() -> None:
    radon = activity.Kilobecquerel(9) / CubicMetre(60)
    assert type(radon) is ActivityConcentration
    assert radon == ac.BecquerelPerCubicMetre(150)
    room = radon * CubicMetre(60)
    assert type(room) is Activity
    assert room == activity.Kilobecquerel(9)
    assert CubicMetre(60) * radon == room
    assert activity.Becquerel(300) / radon == CubicMetre(2)


def test_an_activity_over_a_mass_is_a_specific_activity_and_back() -> None:
    soil = activity.Becquerel(200) / Kilogram(0.5)
    assert type(soil) is SpecificActivity
    assert soil == sa.BecquerelPerKilogram(400)
    sample = soil * Kilogram(0.5)
    assert type(sample) is Activity
    assert sample == activity.Becquerel(200)
    assert activity.Becquerel(200) / soil == Kilogram(0.5)


def test_an_activity_over_an_area_is_a_surface_activity_and_back() -> None:
    wipe = activity.Becquerel(40) / SquareCentimetre(10)
    assert type(wipe) is SurfaceActivity
    assert wipe == su.BecquerelPerSquareCentimetre(4)
    bench = wipe * SquareMetre(2)
    assert type(bench) is Activity
    assert bench == activity.Kilobecquerel(80)
    assert activity.Becquerel(40) / wipe == SquareCentimetre(10)


def test_the_units_are_exact() -> None:
    assert ac.PicocuriePerLitre(1) == ac.BecquerelPerCubicMetre(37)
    assert ac.PicocuriePerLitre(4) == ac.BecquerelPerCubicMetre(148)
    assert ac.BecquerelPerLitre(1) == ac.BecquerelPerCubicMetre(1000)
    assert sa.PicocuriePerGram(1) == sa.BecquerelPerKilogram(37)
    assert sa.BecquerelPerGram(1) == sa.KilobecquerelPerKilogram(1)
    assert sa.CuriePerGram(1) == sa.BecquerelPerKilogram(Fraction(37, 1) * 10**12)
    assert su.CuriePerSquareKilometre(1) == su.BecquerelPerSquareMetre(37000)
    assert su.BecquerelPerSquareCentimetre(1) == su.KilobecquerelPerSquareMetre(10)
    assert su.DpmPer100SquareCentimetre(60) == su.BecquerelPerSquareCentimetre(
        Fraction(1, 100)
    )


def test_the_same_activity_per_litre_and_per_cubic_metre_agree() -> None:
    assert activity.Picocurie(4) / Litre(1) == ac.PicocuriePerLitre(4)


def test_a_frequency_per_volume_is_a_concentration() -> None:
    assert type(Hertz(5) / CubicMetre(1)) is ActivityConcentration
    with pytest.raises(IncompatibleDimensionError):
        activity.Becquerel(5) / Metre(1)


def test_an_activity_density_times_another_quantity_is_not_an_activity() -> None:
    with pytest.raises(IncompatibleDimensionError):
        Gray(1) / activity.Becquerel(1)


def test_the_density_texts_are_read_by_the_quantity_they_are_given() -> None:
    assert parse("4 pCi/L", ActivityConcentration) == ac.PicocuriePerLitre(4)
    assert parse("150 Bq/m3", ActivityConcentration) == ac.BecquerelPerCubicMetre(150)
    assert parse("150 Bq/m\u00b3", ActivityConcentration) == (
        ac.BecquerelPerCubicMetre(150)
    )
    assert parse("15 pCi/g", SpecificActivity) == sa.PicocuriePerGram(15)
    assert parse("4 Bq/cm2", SurfaceActivity) == su.BecquerelPerSquareCentimetre(4)
    assert parse("300 dpm/100cm2", SurfaceActivity) == su.DpmPer100SquareCentimetre(300)
