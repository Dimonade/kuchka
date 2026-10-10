"""Historical Russian units of length.

The imperial Russian system was fixed to the English inch, so every unit here is an
exact multiple of `Inch`:

===========  ==============  =====================
Unit         Translation     Size
===========  ==============  =====================
`Tochka`     point           1/100 inch
`Liniya`     line            1/10 inch
`Dyuym`      inch (perst)    1 inch
`Vershok`    tip             1 3/4 inches
`Ladon`      palm            3 inches
`Pyad`       span (quarter)  7 inches
`Fut`        foot            12 inches (1 ft)
`Lokot`      elbow, cubit    18 inches (1.5 ft)
`Shag`       step            28 inches (2 1/3 ft)
`Arshin`     yard            28 inches (2 1/3 ft)
`Sazhen`     fathom          84 inches (7 ft)
`Versta`     verst           500 sazhens (3500 ft)
===========  ==============  =====================

`Perst` is another name for `Dyuym`, and `Chetvert` for `Pyad`.
Both are aliases of the same objects.
`Shag` and `Arshin` share one size and keep their own names, symbols, and unit
definitions.

Examples
--------
Seven English feet make one sazhen:

>>> Sazhen(1) == Foot(7)
True

A verst is 500 sazhens, or exactly 1.0668 km:

>>> Versta(1) == Kilometre(1.0668)
True

Notes
-----
`RUSSIAN_LENGTH_UNITS` maps every symbol, such as ``"arshin"``, to its constructor.

Notes
-----

For detailed information, the following page was consulted:
https://en.wikipedia.org/wiki/Historical_Russian_units_of_measurement

See Also
--------

~kuchka.quantities.Length
    The quantity every constructor in this module builds.

"""

from __future__ import annotations

from fractions import Fraction
from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import LENGTH
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Length
from kuchka.quantities import UnitDef
from kuchka.units.length import INCH

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

TOCHKA = UnitDef("tochka", "tochka", INCH.scale / 100, LENGTH)
LINIYA = UnitDef("liniya", "liniya", INCH.scale / 10, LENGTH)
DYUYM = UnitDef("dyuym", "dyuym", INCH.scale, LENGTH)
VERSHOK = UnitDef("vershok", "vershok", Fraction(7, 4) * INCH.scale, LENGTH)
LADON = UnitDef("ladon", "ladon", 3 * INCH.scale, LENGTH)
PYAD = UnitDef("pyad", "pyad", 7 * INCH.scale, LENGTH)
FUT = UnitDef("fut", "fut", 12 * INCH.scale, LENGTH)
LOKOT = UnitDef("lokot", "lokot", 18 * INCH.scale, LENGTH)
SHAG = UnitDef("shag", "shag", 28 * INCH.scale, LENGTH)
ARSHIN = UnitDef("arshin", "arshin", 28 * INCH.scale, LENGTH)
SAZHEN = UnitDef("sazhen", "sazhen", 84 * INCH.scale, LENGTH)
VERSTA = UnitDef("versta", "versta", 500 * SAZHEN.scale, LENGTH)

PERST = DYUYM
CHETVERT = PYAD


def Tochka(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in points (tochki).

    Parameters
    ----------
    value : Numeric
        Length magnitude in points (tochki).

    Returns
    -------
    Length
        Length represented in points (tochki).

    Notes
    -----
    One tochka is 1/100 inch, or exactly 0.254 mm.

    Examples
    --------
    A hundred points make one inch:

    >>> Tochka(100) == Inch(1)
    True

    """
    return Length(to_exact(value) * TOCHKA.scale, TOCHKA)


def Liniya(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in lines (linii).

    Parameters
    ----------
    value : Numeric
        Length magnitude in lines (linii).

    Returns
    -------
    Length
        Length represented in lines (linii).

    Notes
    -----
    One liniya is 1/10 inch, or exactly 2.54 mm.

    Examples
    --------
    Ten lines make one inch:

    >>> Liniya(10) == Inch(1)
    True

    """
    return Length(to_exact(value) * LINIYA.scale, LINIYA)


def Dyuym(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in inches (dyuymy).

    Parameters
    ----------
    value : Numeric
        Length magnitude in inches (dyuymy).

    Returns
    -------
    Length
        Length represented in inches (dyuymy).

    Notes
    -----
    One dyuym, also called a perst, is exactly 2.54 cm.

    Examples
    --------
    The Russian inch equals the English inch:

    >>> Dyuym(1) == Inch(1)
    True

    """
    return Length(to_exact(value) * DYUYM.scale, DYUYM)


def Vershok(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in vershoks.

    Parameters
    ----------
    value : Numeric
        Length magnitude in vershoks.

    Returns
    -------
    Length
        Length represented in vershoks.

    Notes
    -----
    One vershok is 1 3/4 inches, or exactly 4.445 cm.

    Examples
    --------
    Sixteen vershoks make one arshin:

    >>> Vershok(16) == Arshin(1)
    True

    """
    return Length(to_exact(value) * VERSHOK.scale, VERSHOK)


def Ladon(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in palms (ladoni).

    Parameters
    ----------
    value : Numeric
        Length magnitude in palms (ladoni).

    Returns
    -------
    Length
        Length represented in palms (ladoni).

    Notes
    -----
    One ladon is 3 inches, or exactly 7.62 cm.

    Examples
    --------
    Four palms make one foot:

    >>> Ladon(4) == Fut(1)
    True

    """
    return Length(to_exact(value) * LADON.scale, LADON)


def Pyad(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in spans (pyadi).

    Parameters
    ----------
    value : Numeric
        Length magnitude in spans (pyadi).

    Returns
    -------
    Length
        Length represented in spans (pyadi).

    Notes
    -----
    One pyad, also called a chetvert, is 7 inches: a quarter of an arshin.

    Examples
    --------
    Four spans make one arshin:

    >>> Pyad(4) == Arshin(1)
    True

    """
    return Length(to_exact(value) * PYAD.scale, PYAD)


def Fut(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in feet (futy).

    Parameters
    ----------
    value : Numeric
        Length magnitude in feet (futy).

    Returns
    -------
    Length
        Length represented in feet (futy).

    Notes
    -----
    One fut is 12 inches, equal to the English foot.

    Examples
    --------
    The Russian foot equals the English foot:

    >>> Fut(1) == Foot(1)
    True

    """
    return Length(to_exact(value) * FUT.scale, FUT)


def Lokot(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in elbows (lokti).

    Parameters
    ----------
    value : Numeric
        Length magnitude in elbows (lokti).

    Returns
    -------
    Length
        Length represented in elbows (lokti).

    Notes
    -----
    One lokot is 18 inches, or exactly 45.72 cm.

    Examples
    --------
    An elbow is one and a half feet:

    >>> Lokot(2) == Fut(3)
    True

    """
    return Length(to_exact(value) * LOKOT.scale, LOKOT)


def Shag(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in steps (shagi).

    Parameters
    ----------
    value : Numeric
        Length magnitude in steps (shagi).

    Returns
    -------
    Length
        Length represented in steps (shagi).

    Notes
    -----
    One shag is 28 inches, or exactly 71.12 cm.

    Examples
    --------
    A step is the length of an arshin:

    >>> Shag(1) == Arshin(1)
    True

    """
    return Length(to_exact(value) * SHAG.scale, SHAG)


def Arshin(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in arshins.

    Parameters
    ----------
    value : Numeric
        Length magnitude in arshins.

    Returns
    -------
    Length
        Length represented in arshins.

    Notes
    -----
    One arshin is 28 inches, or exactly 71.12 cm.

    Examples
    --------
    An arshin is 2 1/3 feet:

    >>> Arshin(3) == Fut(7)
    True

    """
    return Length(to_exact(value) * ARSHIN.scale, ARSHIN)


def Sazhen(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in fathoms (sazheni).

    Parameters
    ----------
    value : Numeric
        Length magnitude in fathoms (sazheni).

    Returns
    -------
    Length
        Length represented in fathoms (sazheni).

    Notes
    -----
    One sazhen is 84 inches, or exactly 7 English feet.

    Examples
    --------
    A fathom is three arshins:

    >>> Sazhen(1) == Arshin(3)
    True

    """
    return Length(to_exact(value) * SAZHEN.scale, SAZHEN)


def Versta(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in versts (versty).

    Parameters
    ----------
    value : Numeric
        Length magnitude in versts (versty).

    Returns
    -------
    Length
        Length represented in versts (versty).

    Notes
    -----
    One versta is 500 sazhens, or exactly 1.0668 km.

    Examples
    --------
    A verst is close to one kilometre:

    >>> Versta(1) == Kilometre(1.0668)
    True

    """
    return Length(to_exact(value) * VERSTA.scale, VERSTA)


Perst = Dyuym
Chetvert = Pyad


RUSSIAN_LENGTH_UNITS: Mapping[str, Callable[[Numeric], Length]] = MappingProxyType(
    {
        TOCHKA.symbol: Tochka,
        LINIYA.symbol: Liniya,
        DYUYM.symbol: Dyuym,
        VERSHOK.symbol: Vershok,
        LADON.symbol: Ladon,
        PYAD.symbol: Pyad,
        FUT.symbol: Fut,
        LOKOT.symbol: Lokot,
        SHAG.symbol: Shag,
        ARSHIN.symbol: Arshin,
        SAZHEN.symbol: Sazhen,
        VERSTA.symbol: Versta,
    }
)
"""Constructors by symbol, for configuration files and external interfaces."""


__all__ = [
    "ARSHIN",
    "CHETVERT",
    "DYUYM",
    "FUT",
    "LADON",
    "LINIYA",
    "LOKOT",
    "PERST",
    "PYAD",
    "RUSSIAN_LENGTH_UNITS",
    "SAZHEN",
    "SHAG",
    "TOCHKA",
    "VERSHOK",
    "VERSTA",
    "Arshin",
    "Chetvert",
    "Dyuym",
    "Fut",
    "Ladon",
    "Liniya",
    "Lokot",
    "Perst",
    "Pyad",
    "Sazhen",
    "Shag",
    "Tochka",
    "Vershok",
    "Versta",
]
