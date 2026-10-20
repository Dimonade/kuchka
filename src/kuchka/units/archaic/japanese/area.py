"""Japanese traditional units of area.

These units belong to the shakkan-hō (尺貫法) measurement tradition.
The *tsubo* (坪) is the principal reference unit for this area scale:
one tsubo is equivalent to a square *ken* (間), or 36 square shaku (尺).
The smaller unit written 勺 is also romanised *shaku*, but it is a distinct area unit
equal to 1/100 tsubo, which makes it a unit of its own and leaves the square shaku
unnamed.

Japanese area units appear in two especially familiar settings.
The *jō* (畳 or 帖) is used when discussing tatami-based floor plans, while *tsubo* is
common in real-estate descriptions.
Agricultural records use *bu* (歩) as another name for a tsubo and use larger units such
as *se*, *tan*, and *chōbu* for fields and landholdings.

Area
----

================= ========== ======= ============ =====================
Unit              Romanised  Kanji   Tsubo        Exact area
================= ========== ======= ============ =====================
Shaku             Shaku      勺      1/100        4/121 m²
Go                Gō         合      1/10         40/121 m²
Jo                Jō         畳, 帖  1/2          200/121 m²
Tsubo             Tsubo      坪      1            400/121 m²
Bu                Bu         歩      1            400/121 m²
Se                Se         畝      30           12,000/121 m²
Tan               Tan        段, 反  300          120,000/121 m²
Chobu             Chōbu      町歩    3,000        1,200,000/121 m²
================= ========== ======= ============ =====================

The scales are exact fractions.
In this standardized table, one *jō* is half a tsubo, but actual tatami mats have
varied by region and building convention.
A count of physical mats can therefore differ from the area computed with ``Jo``.

Examples
--------
A machiya floor plan has an eight-jō room joined to a six-jō room.
A one-jō alcove is reserved for a tokonoma, leaving the remaining floor area for use:

>>> rooms = Jo(8) + Jo(6)
>>> alcove = Jo(1)
>>> usable_floor = (rooms - alcove).to(TSUBO)
>>> usable_floor
6.5 tsubo

A land ledger lists a parcel as 121 tsubo.
Under the standardized conversion, that is exactly 400 square metres, which makes the
old and metric records straightforward to reconcile:

>>> from kuchka.units.area import SQUARE_METRE
>>> cadastral_area = Tsubo(121)
>>> cadastral_area.to(SQUARE_METRE)
400 m²

A village estate of one chōbu reserves one tan for a shared waterway.
The remaining land is divided equally among three households:

>>> estate = Chobu(1)
>>> waterway = Tan(1)
>>> household_plot = ((estate - waterway) / 3).to(TAN)
>>> household_plot
3 tan

Notes
-----
These are selected standardized definitions; historic and regional conventions used
values of their own.

``JAPANESE_AREA_UNITS`` maps unit symbols such as ``"tsubo"``, ``"tan"``, and ``"町歩"``
to their constructors.
It is intended for boundary code that reads measurements from records, catalogues,
configuration files, or other external sources.

For historical background, see:
https://en.wikipedia.org/wiki/Japanese_units_of_measurement

See Also
--------
~kuchka.quantities.Area
    Quantity type representing area.
~kuchka.units.area
    Metric and other area constructors, including square metres and hectares.
~kuchka.units.japanese.length
    Japanese length units, including shaku and ken.

"""

from __future__ import annotations

from fractions import Fraction
from typing import TYPE_CHECKING

from kuchka.dimensions import AREA
from kuchka.internal.unit_table import unit_table
from kuchka.internal.unit_table import units_of
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Area
from kuchka.quantities import UnitDef
from kuchka.quantities.base.units import extend_units

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping


TSUBO = UnitDef(
    "tsubo",
    "tsubo",
    Fraction(400, 121),
    AREA,
    aliases=("坪",),
)
SHAKU = UnitDef(
    "shaku",
    "shaku",
    TSUBO.scale / 100,
    AREA,
    aliases=("勺",),
)
GO = UnitDef(
    "go",
    "go",
    TSUBO.scale / 10,
    AREA,
    aliases=("合", "gō"),
)
JO = UnitDef(
    "jo",
    "jo",
    TSUBO.scale / 2,
    AREA,
    aliases=("畳", "帖", "jō"),
)
BU = UnitDef(
    "bu",
    "bu",
    TSUBO.scale,
    AREA,
    aliases=("歩",),
)
SE = UnitDef(
    "se",
    "se",
    30 * TSUBO.scale,
    AREA,
    aliases=("畝",),
)
TAN = UnitDef(
    "tan",
    "tan",
    300 * TSUBO.scale,
    AREA,
    aliases=("段", "反"),
)
CHOBU = UnitDef(
    "chobu",
    "chobu",
    3000 * TSUBO.scale,
    AREA,
    aliases=("町歩", "chōbu"),
)


def Shaku(value: Numeric) -> Area:
    """Construct area from a magnitude expressed in shaku (勺).

    Parameters
    ----------
    value : Numeric
        Area magnitude in shaku (勺).

    Returns
    -------
    Area
        Area represented in shaku.

    Notes
    -----
    One shaku (勺) is 1/100 tsubo, or exactly 4/121 square metres.
    Shaku (尺), the length unit, is a different unit, and one square shaku is another
    area again.

    Examples
    --------
    A garden ledger records a stone apron and its adjoining threshold separately.
    Together their 175 and 25 shaku make two tsubo:

    >>> apron = Shaku(175)
    >>> threshold = Shaku(25)
    >>> (apron + threshold).to(TSUBO)
    2 tsubo

    """
    return Area(to_exact(value) * SHAKU.scale, SHAKU)


def Go(value: Numeric) -> Area:
    """Construct area from a magnitude expressed in gō (合).

    Parameters
    ----------
    value : Numeric
        Area magnitude in gō.

    Returns
    -------
    Area
        Area represented in gō.

    Notes
    -----
    One gō is 1/10 tsubo, or exactly 40/121 square metres.

    Examples
    --------
    A townhouse entrance has four gō of stone landing and six gō of drainage apron.
    Together they occupy one tsubo:

    >>> landing = Go(4)
    >>> drainage_apron = Go(6)
    >>> (landing + drainage_apron).to(TSUBO)
    1 tsubo

    """
    return Area(to_exact(value) * GO.scale, GO)


def Jo(value: Numeric) -> Area:
    """Construct area from a magnitude expressed in jō (畳 or 帖).

    Parameters
    ----------
    value : Numeric
        Area magnitude in jō.

    Returns
    -------
    Area
        Area represented in jō.

    Notes
    -----
    In the standardized scale, one jō is half a tsubo, or exactly 200/121 square metres.
    Physical tatami dimensions vary, so this constructor models the nominal area unit,
    which stands for any mat of that standard.

    Examples
    --------
    A pair of rooms measures eight and six jō.
    After reserving one jō for a tokonoma alcove, the remaining floor area is 6.5 tsubo:

    >>> rooms = Jo(8) + Jo(6)
    >>> (rooms - Jo(1)).to(TSUBO)
    6.5 tsubo

    """
    return Area(to_exact(value) * JO.scale, JO)


def Tsubo(value: Numeric) -> Area:
    """Construct area from a magnitude expressed in tsubo (坪).

    Parameters
    ----------
    value : Numeric
        Area magnitude in tsubo.

    Returns
    -------
    Area
        Area represented in tsubo.

    Notes
    -----
    One tsubo is the area of a square ken, conventionally described as
    36 square shaku (尺).
    Its standardized exact area is 400/121 square metres.

    Examples
    --------
    A property listing gives a 45-tsubo lot.
    After accounting for an 18-tsubo building footprint and three tsubo for the
    entrance and drive, the remaining garden is 24 tsubo:

    >>> lot = Tsubo(45)
    >>> footprint = Tsubo(18)
    >>> entrance_and_drive = Tsubo(3)
    >>> lot - footprint - entrance_and_drive
    24 tsubo

    """
    return Area(to_exact(value) * TSUBO.scale, TSUBO)


def Bu(value: Numeric) -> Area:
    """Construct area from a magnitude expressed in bu (歩).

    Parameters
    ----------
    value : Numeric
        Area magnitude in bu.

    Returns
    -------
    Area
        Area represented in bu.

    Notes
    -----
    In agricultural records, bu is another name for tsubo.
    This constructor preserves the notation 歩; one bu is exactly 400/121 square metres.

    Examples
    --------
    A farm ledger records 240 bu, of which 30 bu are set aside as a seedling bed.
    The remaining cultivated area is seven se:

    >>> cultivated = Bu(240) - Bu(30)
    >>> cultivated.to(SE)
    7 se

    """
    return Area(to_exact(value) * BU.scale, BU)


def Se(value: Numeric) -> Area:
    """Construct area from a magnitude expressed in se (畝).

    Parameters
    ----------
    value : Numeric
        Area magnitude in se.

    Returns
    -------
    Area
        Area represented in se.

    Notes
    -----
    One se is 30 tsubo, or exactly 12,000/121 square metres.

    Examples
    --------
    Three vegetable plots occupy two, three, and four se.
    A drainage channel takes one se from the combined area, leaving eight se under
    cultivation:

    >>> vegetable_plots = Se(2) + Se(3) + Se(4)
    >>> vegetable_plots - Se(1)
    8 se

    """
    return Area(to_exact(value) * SE.scale, SE)


def Tan(value: Numeric) -> Area:
    """Construct area from a magnitude expressed in tan (段 or 反).

    Parameters
    ----------
    value : Numeric
        Area magnitude in tan.

    Returns
    -------
    Area
        Area represented in tan.

    Notes
    -----
    One tan is 300 tsubo, or exactly 120,000/121 square metres.

    Examples
    --------
    A two-tan paddy reserves three se for a seedling nursery.
    The remainder is recorded as seventeen se:

    >>> paddy = Tan(2)
    >>> nursery = Se(3)
    >>> (paddy - nursery).to(SE)
    17 se

    """
    return Area(to_exact(value) * TAN.scale, TAN)


def Chobu(value: Numeric) -> Area:
    """Construct area from a magnitude expressed in chōbu (町歩).

    Parameters
    ----------
    value : Numeric
        Area magnitude in chōbu.

    Returns
    -------
    Area
        Area represented in chōbu.

    Notes
    -----
    One chōbu is 3,000 tsubo, or exactly 1,200,000/121 square metres.
    The spelling chōbu identifies the area unit; the plain 町 can also denote a unit of
    length, so the area unit is reached through 町歩.

    Examples
    --------
    A two-chōbu estate transfers one tan beside an irrigation canal.
    The remaining land is recorded as nineteen tan:

    >>> (Chobu(2) - Tan(1)).to(TAN)
    19 tan

    """
    return Area(to_exact(value) * CHOBU.scale, CHOBU)


JAPANESE_AREA_UNITS: Mapping[str, Callable[[Numeric], Area]] = unit_table(
    "JAPANESE_AREA_UNITS",
    {
        SHAKU: Shaku,
        GO: Go,
        JO: Jo,
        TSUBO: Tsubo,
        BU: Bu,
        SE: Se,
        TAN: Tan,
        CHOBU: Chobu,
    },
)
"""Area constructors by symbol, for configuration files and external interfaces."""


# Importing this module makes Area display in the units of its table.
extend_units(Area, units_of(JAPANESE_AREA_UNITS))


__all__ = [
    "BU",
    "CHOBU",
    "GO",
    "JAPANESE_AREA_UNITS",
    "JO",
    "SE",
    "SHAKU",
    "TAN",
    "TSUBO",
    "Bu",
    "Chobu",
    "Go",
    "Jo",
    "Se",
    "Shaku",
    "Tan",
    "Tsubo",
]
