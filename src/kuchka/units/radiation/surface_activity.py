"""Surface activity constructors: becquerels, curies, and counts per area.

    from kuchka import BecquerelPerSquareCentimetre
    from kuchka import CuriePerSquareKilometre

    wipe = BecquerelPerSquareCentimetre(4)
    fallout = CuriePerSquareKilometre(15)

`SurfaceActivity` is the activity on each unit of area, `Activity / Area`.
Its canonical unit is the becquerel per square metre (`Bq/m²`).
The module provides it with the kilobecquerel per square metre, the becquerel per
square centimetre that contamination limits use, the disintegration per minute per 100
square centimetres of a wipe test, and the curie per square kilometre of a fallout
map: one curie per square kilometre is exactly 37000 Bq/m².

Examples
--------
A reading of 4 Bq/cm², in the SI unit:

>>> BecquerelPerSquareCentimetre(4).to(KILOBECQUEREL_PER_SQUARE_METRE)
40 kBq/m²

A wipe result of 300 dpm/100 cm², in becquerels per square centimetre:

>>> DpmPer100SquareCentimetre(300).to(BECQUEREL_PER_SQUARE_CENTIMETRE)
0.05 Bq/cm²

`SURFACE_ACTIVITY_UNITS` maps symbols such as ``"Bq/m2"``, ``"Bq/cm2"``, and
``"dpm/100cm2"`` to their constructors for boundary code that reads unit labels from
external data.

"""

from __future__ import annotations

from fractions import Fraction
from typing import TYPE_CHECKING

from kuchka.dimensions import SURFACE_ACTIVITY
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import SurfaceActivity
from kuchka.quantities import UnitDef
from kuchka.units.geometry.area import SQUARE_CENTIMETRE
from kuchka.units.geometry.area import SQUARE_KILOMETRE
from kuchka.units.radiation.activity import BECQUEREL
from kuchka.units.radiation.activity import CURIE

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

BECQUEREL_PER_SQUARE_METRE = UnitDef(
    "becquerel_per_square_metre",
    "Bq/m²",
    1,
    SURFACE_ACTIVITY,
    aliases=("Bq/m2", "Bq/m^2"),
    words=("becquerels per square metre", "becquerels per square meter"),
)
KILOBECQUEREL_PER_SQUARE_METRE = UnitDef(
    "kilobecquerel_per_square_metre",
    "kBq/m²",
    1000,
    SURFACE_ACTIVITY,
    aliases=("kBq/m2", "kBq/m^2"),
    words=("kilobecquerels per square metre", "kilobecquerels per square meter"),
)
BECQUEREL_PER_SQUARE_CENTIMETRE = UnitDef(
    "becquerel_per_square_centimetre",
    "Bq/cm²",
    BECQUEREL.scale / SQUARE_CENTIMETRE.scale,
    SURFACE_ACTIVITY,
    aliases=("Bq/cm2", "Bq/cm^2"),
    words=("becquerels per square centimetre", "becquerels per square centimeter"),
)
DPM_PER_100_SQUARE_CENTIMETRE = UnitDef(
    "dpm_per_100_square_centimetre",
    "dpm/100 cm²",
    Fraction(1, 60) / (100 * SQUARE_CENTIMETRE.scale),
    SURFACE_ACTIVITY,
    aliases=("dpm/100cm²", "dpm/100 cm2", "dpm/100cm2"),
    words=("disintegrations per minute per 100 square centimetres",),
)
CURIE_PER_SQUARE_KILOMETRE = UnitDef(
    "curie_per_square_kilometre",
    "Ci/km²",
    CURIE.scale / SQUARE_KILOMETRE.scale,
    SURFACE_ACTIVITY,
    aliases=("Ci/km2", "Ci/km^2"),
    words=("curies per square kilometre", "curies per square kilometer"),
)

SurfaceActivity._canonical_unit = BECQUEREL_PER_SQUARE_METRE  # noqa: SLF001 -- this module owns SurfaceActivity's canonical unit


def BecquerelPerSquareMetre(value: Numeric) -> SurfaceActivity:
    """Construct a SurfaceActivity from a magnitude in becquerels per square metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in becquerels per square metre.

    Returns
    -------
    SurfaceActivity
        SurfaceActivity represented in becquerels per square metre.

    """
    return SurfaceActivity(
        to_exact(value) * BECQUEREL_PER_SQUARE_METRE.scale, BECQUEREL_PER_SQUARE_METRE
    )


def KilobecquerelPerSquareMetre(value: Numeric) -> SurfaceActivity:
    """Construct a SurfaceActivity from a magnitude in kilobecquerels per square metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in kilobecquerels per square metre.

    Returns
    -------
    SurfaceActivity
        SurfaceActivity represented in kilobecquerels per square metre.

    """
    return SurfaceActivity(
        to_exact(value) * KILOBECQUEREL_PER_SQUARE_METRE.scale,
        KILOBECQUEREL_PER_SQUARE_METRE,
    )


def BecquerelPerSquareCentimetre(value: Numeric) -> SurfaceActivity:
    """Construct a SurfaceActivity from a magnitude in becquerels per square centimetre.

    Parameters
    ----------
    value : Numeric
        Magnitude in becquerels per square centimetre.

    Returns
    -------
    SurfaceActivity
        SurfaceActivity represented in becquerels per square centimetre.

    """
    return SurfaceActivity(
        to_exact(value) * BECQUEREL_PER_SQUARE_CENTIMETRE.scale,
        BECQUEREL_PER_SQUARE_CENTIMETRE,
    )


def DpmPer100SquareCentimetre(value: Numeric) -> SurfaceActivity:
    """Construct a SurfaceActivity in dpm per 100 square centimetres.

    Parameters
    ----------
    value : Numeric
        Magnitude in disintegrations per minute per 100 square centimetres.

    Returns
    -------
    SurfaceActivity
        SurfaceActivity represented in dpm per 100 square centimetres.

    """
    return SurfaceActivity(
        to_exact(value) * DPM_PER_100_SQUARE_CENTIMETRE.scale,
        DPM_PER_100_SQUARE_CENTIMETRE,
    )


def CuriePerSquareKilometre(value: Numeric) -> SurfaceActivity:
    """Construct a SurfaceActivity from a magnitude in curies per square kilometre.

    Parameters
    ----------
    value : Numeric
        Magnitude in curies per square kilometre.

    Returns
    -------
    SurfaceActivity
        SurfaceActivity represented in curies per square kilometre.

    """
    return SurfaceActivity(
        to_exact(value) * CURIE_PER_SQUARE_KILOMETRE.scale, CURIE_PER_SQUARE_KILOMETRE
    )


SURFACE_ACTIVITY_UNITS: Mapping[str, Callable[[Numeric], SurfaceActivity]] = unit_table(
    "SURFACE_ACTIVITY_UNITS",
    {
        BECQUEREL_PER_SQUARE_METRE: BecquerelPerSquareMetre,
        KILOBECQUEREL_PER_SQUARE_METRE: KilobecquerelPerSquareMetre,
        BECQUEREL_PER_SQUARE_CENTIMETRE: BecquerelPerSquareCentimetre,
        DPM_PER_100_SQUARE_CENTIMETRE: DpmPer100SquareCentimetre,
        CURIE_PER_SQUARE_KILOMETRE: CuriePerSquareKilometre,
    },
)

__all__ = [
    "BECQUEREL_PER_SQUARE_CENTIMETRE",
    "BECQUEREL_PER_SQUARE_METRE",
    "CURIE_PER_SQUARE_KILOMETRE",
    "DPM_PER_100_SQUARE_CENTIMETRE",
    "KILOBECQUEREL_PER_SQUARE_METRE",
    "SURFACE_ACTIVITY_UNITS",
    "BecquerelPerSquareCentimetre",
    "BecquerelPerSquareMetre",
    "CuriePerSquareKilometre",
    "DpmPer100SquareCentimetre",
    "KilobecquerelPerSquareMetre",
]
