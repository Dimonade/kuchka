"""Historical German and Austrian principal miles (Meilen).

The unqualified word *Meile* named no single length.
Depending on period and place, a mile was a geographic mile, a land or post mile, or a
regional measure that differed by several kilometres from its neighbours.
This module therefore provides named calibrations, and no universal ``Meile``
constructor.
The four calibrations here recur across sources and maps; the many regional miles
are collected in `kuchka.units.archaic.german.length.regional_meilen`.

+-------------------------+-----------------------+--------------------+---------------------------------------+
| Unit                    | German name           | Translation        | Size / relationship                   |
+=========================+=======================+====================+=======================================+
| `GeographischeMeile`    | geographische Meile   | geographical mile  | 1/15 equatorial degree = 7,420.439 m  |
| `Reichsmeile`           | Reichsmeile           | imperial mile      | 7,500 m (later metric calibration)    |
| `PreussischeLandmeile`  | preußische Landmeile  | Prussian land mile | 24,000 Prussian feet = 7,532.5 m      |
| `OesterreichischeMeile` | österreichische Meile | Austrian mile      | 24,000 Viennese feet = 7,585.935360 m |
+-------------------------+-----------------------+--------------------+---------------------------------------+

The geographic mile is one fifteenth of an equatorial degree.
The detailed table in the German-language article gives 7,420.439 m for the corrected
German geographic mile, and its prose rounds this to 7,420.44 m.
This is the value associated with Friedrich Wilhelm Bessel's 1841 recalculation of
Georg Simon Klügel's earlier estimate of 7,428.013 m.
The English-language article gives 7,420.54 m, a difference of 0.101 m that ordinary
rounding leaves unexplained.
`GeographischeMeile` follows the more detailed German historical account.

The Prussian land mile is 24,000 Prussian feet, 7,532.5 m, and the Reichsmeile is the
round 7,500 m of the metric era.
Both are exact rational scales, so a sum or ratio of them carries no rounding.
The Austrian mile is 24,000 Viennese feet (4,000 Viennese Klafter), 7,585.935360 m in
the cited standard.

Examples
--------
A cartographer reconstructing an equatorial chart uses fifteen geographical miles per
degree of arc.
The source's metric calibration makes the full arc:

>>> from kuchka.units.length import KILOMETRE
>>> equatorial_degree = GeographischeMeile(15)
>>> equatorial_degree.to(KILOMETRE)
111.306585 km

A Prussian post road is surveyed at four land miles between two stations:

>>> PreussischeLandmeile(4).to(KILOMETRE)
30.13 km

The metric-era Reichsmeile makes the same itinerary a round figure:

>>> Reichsmeile(10).to(KILOMETRE)
75 km

A Habsburg-era survey of a district road records two Austrian miles:

>>> OesterreichischeMeile(2).to(KILOMETRE)
15.17187072 km

Notes
-----
`GERMAN_MEILE_UNITS` is a read-only `UnitTable` mapping each qualified display symbol,
registered spelling, or name to its constructor.
Each calibration is reached by its qualified name.
The bare spellings ``Meile`` and ``Landmeile`` raise `KeyError`, because they name more
than one scale.

Importing this module lets `Length` display in these miles.

Sources
-------

- https://en.wikipedia.org/wiki/German_units_of_measurement
- https://de.wikipedia.org/wiki/Meile
- https://en.wikipedia.org/wiki/Obsolete_Austrian_units_of_measurement
- https://de.wikipedia.org/wiki/Alte_Ma%C3%9Fe_und_Gewichte_%28%C3%96sterreich%29

See Also
--------
~kuchka.quantities.Length
    The quantity every constructor in this module builds.
~kuchka.units.archaic.german.length.regional_meilen
    The regional miles of the German-speaking lands.

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
from kuchka.units.length import METRE

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping


# Corrected German geographic mile, following Bessel (1841): 7,420.439 m.
GEOGRAPHISCHE_MEILE = UnitDef(
    "geographische_meile",
    "geographische Meile",
    Fraction(7420439, 1000) * METRE.scale,
    LENGTH,
    words=(
        "geographische Meile",
        "geografische Meile",
        "deutsche geographische Meile",
        "German geographical mile",
        "German geographic mile",
    ),
)

# Nominal scale from the historical source: 7,500 m (later metric calibration).
REICHSMEILE = UnitDef(
    "reichsmeile",
    "Reichsmeile",
    Fraction(7500, 1) * METRE.scale,
    LENGTH,
    words=(
        "Reichsmeile",
        "Reichs-Meile",
        "imperial mile",
        "metric-era German mile",
    ),
)

# Nominal scale from the historical source: 24,000 Prussian feet = 7,532.5 m.
PREUSSISCHE_LANDMEILE = UnitDef(
    "preussische_landmeile",
    "preußische Landmeile",
    Fraction(15065, 2) * METRE.scale,
    LENGTH,
    words=(
        "preußische Landmeile",
        "preussische Landmeile",
        "dänisch-preußische Landmeile",
        "daenisch-preussische Landmeile",
        "Preußische Meile",
        "Preussische Meile",
        "Prussian mile",
        "Danish-Prussian land mile",
    ),
)

# Nominal scale from the historical source: 24,000 Viennese feet = 7,585.935360 m.
OESTERREICHISCHE_MEILE = UnitDef(
    "oesterreichische_meile",
    "österreichische Meile",
    Fraction(23706048, 3125) * METRE.scale,
    LENGTH,
    words=(
        "österreichische Meile",
        "oesterreichische Meile",
        "Austrian mile",
        "Viennese-standard mile",
    ),
)


def GeographischeMeile(value: Numeric) -> Length:
    """Construct a length expressed in this historical mile.

    Parameters
    ----------
    value : Numeric
        Length magnitude in this historical mile.

    Returns
    -------
    Length
        Length represented in the selected historical mile.

    Notes
    -----
    Defined as one fifteenth of an equatorial degree. This constructor uses the
    corrected German geographic mile of 7,420.439 m, associated with Bessel's 1841
    recalculation. The German article rounds this to 7,420.44 m; the English article
    gives 7,420.54 m, a difference that ordinary rounding leaves unexplained.

    Examples
    --------
    A mapmaker lays out a 1-degree equatorial arc as fifteen geographic miles and
    checks the length of the full arc:

    >>> distance = GeographischeMeile(15)
    >>> from kuchka.units.length import KILOMETRE
    >>> distance.to(KILOMETRE)
    111.306585 km

    """
    return Length(to_exact(value) * GEOGRAPHISCHE_MEILE.scale, GEOGRAPHISCHE_MEILE)


def Reichsmeile(value: Numeric) -> Length:
    """Construct a length expressed in this historical mile.

    Parameters
    ----------
    value : Numeric
        Length magnitude in this historical mile.

    Returns
    -------
    Length
        Length represented in the selected historical mile.

    Notes
    -----
    The metric-era mile was fixed at 7,500 m; the English-language source reports
    that its use was prohibited by law in 1908.

    Examples
    --------
    A road engineer budgets twelve Reichsmeilen for a post road:

    >>> distance = Reichsmeile(12)
    >>> from kuchka.units.length import KILOMETRE
    >>> distance.to(KILOMETRE)
    90 km

    """
    return Length(to_exact(value) * REICHSMEILE.scale, REICHSMEILE)


def PreussischeLandmeile(value: Numeric) -> Length:
    """Construct a length expressed in this historical mile.

    Parameters
    ----------
    value : Numeric
        Length magnitude in this historical mile.

    Returns
    -------
    Length
        Length represented in the selected historical mile.

    Notes
    -----
    In 1816, Frederick William III adopted the Danish mile for Prussia, reported in
    the German-language article as 7,532.5 m or 24,000 Prussian feet. The English-
    language table rounds this to 7,532 m.

    Examples
    --------
    A Prussian postal itinerary counts two landmeilen between district offices:

    >>> distance = PreussischeLandmeile(2)
    >>> from kuchka.units.length import KILOMETRE
    >>> distance.to(KILOMETRE)
    15.065 km

    """
    return Length(to_exact(value) * PREUSSISCHE_LANDMEILE.scale, PREUSSISCHE_LANDMEILE)


def OesterreichischeMeile(value: Numeric) -> Length:
    """Construct a length expressed in this historical mile.

    Parameters
    ----------
    value : Numeric
        Length magnitude in this historical mile.

    Returns
    -------
    Length
        Length represented in the selected historical mile.

    Notes
    -----
    The Austrian standard is 24,000 Viennese feet or 4,000 Klafter, giving
    7,585.935360 m under that standard.

    Examples
    --------
    A Habsburg-era itinerary marks two Austrian miles between district towns:

    >>> distance = OesterreichischeMeile(2)
    >>> from kuchka.units.length import KILOMETRE
    >>> distance.to(KILOMETRE)
    15.17187072 km

    """
    return Length(
        to_exact(value) * OESTERREICHISCHE_MEILE.scale, OESTERREICHISCHE_MEILE
    )


# Orthographic aliases share the same constructor and UnitDef.
GeografischeMeile = GeographischeMeile
PreussischeMeile = PreussischeLandmeile


GERMAN_MEILE_UNITS: Mapping[str, Callable[[Numeric], Length]] = unit_table(
    "GERMAN_MEILE_UNITS",
    {
        GEOGRAPHISCHE_MEILE: GeographischeMeile,
        REICHSMEILE: Reichsmeile,
        PREUSSISCHE_LANDMEILE: PreussischeLandmeile,
        OESTERREICHISCHE_MEILE: OesterreichischeMeile,
    },
)
"""The principal miles by spelling, for configuration files and external interfaces."""

# Importing this module makes Length display in the units of its table.
extend_units(Length, GERMAN_MEILE_UNITS)


__all__ = [
    "GEOGRAPHISCHE_MEILE",
    "GERMAN_MEILE_UNITS",
    "OESTERREICHISCHE_MEILE",
    "PREUSSISCHE_LANDMEILE",
    "REICHSMEILE",
    "GeografischeMeile",
    "GeographischeMeile",
    "OesterreichischeMeile",
    "PreussischeLandmeile",
    "PreussischeMeile",
    "Reichsmeile",
]
