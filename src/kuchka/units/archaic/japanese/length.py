"""Japanese shakkan-hō units of length.

The shakkan-hō (尺貫法) is the traditional Japanese system of measurement.
Its length scale is based on the shaku (尺), which was fixed by statute in
1891 at exactly 10/33 metre.

The relationships represented here use exact rational arithmetic. Although
10/33 has no finite decimal expansion, conversions between shaku-based units
and metres introduce no rounding into the unit definitions.

Length
------

=============  ===========  ============  ==============
Unit           Romanised    Kanji         Size
=============  ===========  ============  ==============
`Mo`           Mō           毛, 毫        1/10,000 shaku
`Rin`          Rin          厘, 釐        1/1,000 shaku
`Bu`           Bu           分            1/100 shaku
`Sun`          Sun          寸            1/10 shaku
`Shaku`        Shaku        尺            10/33 m
`Ken`          Ken, Hiro    間, 尋        6 shaku
`Jo`           Jō           丈            10 shaku
`Cho`          Chō          町            60 ken
`Ri`           Ri           里            36 cho
=============  ===========  ============  ==============

The shaku and sun are particularly familiar in traditional Japanese
carpentry. Ken describes a structural interval in traditional architecture,
while cho and ri provide larger scales for surveying and travel.
Hiro (尋), the fathom of outstretched arms, is another name of ken and builds the
same unit.

Examples
--------
The shakuhachi is traditionally associated with a nominal length of one shaku
and eight sun. Its name itself reflects this measurement:

>>> flute_length = Shaku(1) + Sun(8)
>>> flute_length
1.8 shaku

A carpenter restoring a traditional timber-framed machiya prepares a floor
plan 33 shaku long and 16 shaku plus 5 sun wide. The standardized dimensions
produce a ten-by-five-metre footprint:

>>> from kuchka.units.length import METRE
>>> room_length = Shaku(33)
>>> room_width = Shaku(16) + Sun(5)
>>> room_area = room_length * room_width
>>> room_area
50 m²

A Meiji-era survey records an 11-ri section of proposed railway track.
Under the standardized shakkan-hō definition, that distance is exactly
43.2 kilometres:

>>> from kuchka.units.length import KILOMETRE
>>> surveyed_route = Ri(11)
>>> surveyed_route.to(KILOMETRE)
43.2 km

Notes
-----
The principal relationships are:

``1 shaku = 10/33 m``
``1 bu = 1/100 shaku``
``1 sun = 1/10 shaku``
``1 ken = 6 shaku``
``1 jo = 10 shaku``
``1 cho = 60 ken = 360 shaku``
``1 ri = 36 cho = 12,960 shaku``

These are the standardized definitions this module represents.
Historical and regional Japanese conventions varied, and each deserves its own
calibration.

`JAPANESE_LENGTH_UNITS` maps each unit symbol, such as ``"shaku"`` or
``"ri"``, to its constructor. It is intended for boundary code that reads
measurements from configuration files, catalogues, architectural records,
or other external sources.

For historical background, see:
https://en.wikipedia.org/wiki/Japanese_units_of_measurement

See Also
--------
~kuchka.quantities.Length
    Quantity type representing length.
~kuchka.quantities.Area
    Area derived from multiplying two lengths.
~kuchka.units.length
    Modern metric and selected non-SI length constructors.

"""

from __future__ import annotations

from fractions import Fraction
from typing import TYPE_CHECKING

from kuchka.dimensions import LENGTH
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Length
from kuchka.quantities import UnitDef
from kuchka.quantities.base.units import extend_units

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping


_SHAKU = Fraction(10, 33)

_SHAKU = Fraction(10, 33)

MO = UnitDef(
    "mo",
    "mo",
    _SHAKU / 10_000,
    LENGTH,
    aliases=("毛", "毫", "mō"),
)
RIN = UnitDef(
    "rin",
    "rin",
    _SHAKU / 1_000,
    LENGTH,
    aliases=("厘", "釐"),
)
BU = UnitDef("bu", "bu", _SHAKU / 100, LENGTH, aliases=("分",))
SUN = UnitDef("sun", "sun", _SHAKU / 10, LENGTH, aliases=("寸",))
SHAKU = UnitDef("shaku", "shaku", _SHAKU, LENGTH, aliases=("尺",))
KEN = UnitDef("ken", "ken", 6 * _SHAKU, LENGTH, aliases=("間", "尋"), words=("hiro",))
JO = UnitDef("jo", "jo", 10 * _SHAKU, LENGTH, aliases=("丈",))
CHO = UnitDef("cho", "cho", 60 * KEN.scale, LENGTH, aliases=("町",))
RI = UnitDef("ri", "ri", 36 * CHO.scale, LENGTH, aliases=("里",))

HIRO = KEN


def Mo(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in mō.

    Parameters
    ----------
    value : Numeric
        Length magnitude in mō.

    Returns
    -------
    Length
        Length represented in mō.

    Notes
    -----
    One mō is 1/10,000 shaku, or exactly 1/33,000 metre.

    Examples
    --------
    An Edo-period woodblock-print workshop prepares a fine registration mark for
    aligning successive colour blocks.
    A 165-mō interval is exactly five millimetres under the standardized definition:

    >>> from kuchka.units.length import MILLIMETRE
    >>> registration_mark = Mo(165)
    >>> registration_mark.to(MILLIMETRE)
    5 mm

    """
    return Length(to_exact(value) * MO.scale, MO)


def Rin(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in rin.

    Parameters
    ----------
    value : Numeric
        Length magnitude in rin.

    Returns
    -------
    Length
        Length represented in rin.

    Notes
    -----
    One rin is 1/1,000 shaku, or exactly 1/3,300 metre.

    Examples
    --------
    A craftsperson restoring a fine inlay on a traditional lacquer box records a
    twenty-millimetre section as 66 rin:

    >>> from kuchka.units.length import MILLIMETRE
    >>> inlay_section = Rin(66)
    >>> inlay_section.to(MILLIMETRE)
    20 mm

    """
    return Length(to_exact(value) * RIN.scale, RIN)


def Bu(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in bu.

    Parameters
    ----------
    value : Numeric
        Length magnitude in bu.

    Returns
    -------
    Length
        Length represented in bu.

    Notes
    -----
    One bu is 1/100 shaku, or 1/10 sun.

    Examples
    --------
    A lacquer artisan lays out three fine decorative rails, each 33 bu long.
    The combined length is exactly 30 centimetres:

    >>> from kuchka.units.length import CENTIMETRE
    >>> rail = Bu(33)
    >>> (rail * 3).to(CENTIMETRE)
    30 cm

    """
    return Length(to_exact(value) * BU.scale, BU)


def Sun(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in sun.

    Parameters
    ----------
    value : Numeric
        Length magnitude in sun.

    Returns
    -------
    Length
        Length represented in sun.

    Notes
    -----
    One sun is 1/10 shaku.

    Examples
    --------
    A traditional joiner specifies a tenon projection of two sun beyond
    the end of a one-shaku timber member:

    >>> member = Shaku(1)
    >>> projection = Sun(2)
    >>> (member + projection).to(SHAKU)
    1.2 shaku

    """
    return Length(to_exact(value) * SUN.scale, SUN)


def Shaku(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in shaku.

    Parameters
    ----------
    value : Numeric
        Length magnitude in shaku.

    Returns
    -------
    Length
        Length represented in shaku.

    Notes
    -----
    One shaku is exactly 10/33 m.

    Examples
    --------
    The nominal length associated with a shakuhachi is one shaku and
    eight sun:

    >>> flute_length = Shaku(1) + Sun(8)
    >>> flute_length
    1.8 shaku

    """
    return Length(to_exact(value) * SHAKU.scale, SHAKU)


def Ken(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in ken.

    Parameters
    ----------
    value : Numeric
        Length magnitude in ken.

    Returns
    -------
    Length
        Length represented in ken.

    Notes
    -----
    One ken is six shaku, or exactly 20/11 m under the standardized definition.

    Examples
    --------
    A timber survey records a long covered walkway as 33 ken. Its standardized
    length is exactly 60 metres:

    >>> from kuchka.units.length import METRE
    >>> walkway = Ken(33)
    >>> walkway.to(METRE)
    60 m

    """
    return Length(to_exact(value) * KEN.scale, KEN)


def Jo(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in jo.

    Parameters
    ----------
    value : Numeric
        Length magnitude in jo.

    Returns
    -------
    Length
        Length represented in jo.

    Notes
    -----
    One jo is ten shaku, or exactly 100/33 m.

    Examples
    --------
    A festival workshop builds a ten-metre tower for a traditional
    Japanese celebration. Its target height can be expressed as one jo
    plus another 23 shaku:

    >>> from kuchka.units.length import METRE
    >>> tower_height = Jo(1) + Shaku(23)
    >>> tower_height.to(METRE)
    10 m

    """
    return Length(to_exact(value) * JO.scale, JO)


def Cho(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in cho.

    Parameters
    ----------
    value : Numeric
        Length magnitude in cho.

    Returns
    -------
    Length
        Length represented in cho.

    Notes
    -----
    One cho is 60 ken, or 360 shaku.

    Examples
    --------
    A Meiji-era survey records an irrigation channel extending for
    eleven cho along the edge of a rice-growing district:

    >>> from kuchka.units.length import KILOMETRE
    >>> channel_length = Cho(11)
    >>> channel_length.to(KILOMETRE)
    1.2 km

    """
    return Length(to_exact(value) * CHO.scale, CHO)


def Ri(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in ri.

    Parameters
    ----------
    value : Numeric
        Length magnitude in ri.

    Returns
    -------
    Length
        Length represented in ri.

    Notes
    -----
    One ri is 36 cho, or 12,960 shaku.

    Examples
    --------
    A Meiji-era railway survey records an eleven-ri section of proposed
    track through the countryside:

    >>> from kuchka.units.length import KILOMETRE
    >>> surveyed_route = Ri(11)
    >>> surveyed_route.to(KILOMETRE)
    43.2 km

    """
    return Length(to_exact(value) * RI.scale, RI)


Hiro = Ken


JAPANESE_LENGTH_UNITS: Mapping[str, Callable[[Numeric], Length]] = unit_table(
    "JAPANESE_LENGTH_UNITS",
    {
        MO: Mo,
        RIN: Rin,
        BU: Bu,
        SUN: Sun,
        SHAKU: Shaku,
        KEN: Ken,
        JO: Jo,
        CHO: Cho,
        RI: Ri,
    },
)
"""Length constructors by symbol, for configuration files and external interfaces."""


# Importing this module makes Length display in the units of its table.
extend_units(Length, JAPANESE_LENGTH_UNITS)


__all__ = [
    "BU",
    "CHO",
    "HIRO",
    "JAPANESE_LENGTH_UNITS",
    "JO",
    "KEN",
    "MO",
    "RI",
    "RIN",
    "SHAKU",
    "SUN",
    "Bu",
    "Cho",
    "Hiro",
    "Jo",
    "Ken",
    "Mo",
    "Ri",
    "Rin",
    "Shaku",
    "Sun",
]
