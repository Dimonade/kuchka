"""Historical regional miles (Meilen) of the German-speaking lands.

Beyond the principal miles, nearly every German state, free city, and Swiss canton
fixed a mile of its own.
Each entry here is a named calibration of one of those, a published metric equivalent
kept as an exact rational scale.

+-------------------------------+--------------------------------------------+-----------------------------------+------------------------------------------+
| Unit                          | German name                                | Translation                       | Size / relationship                      |
+===============================+============================================+===================================+==========================================+
| `BreslauerMeile`              | Breslauer Meile                            | Breslau mile                      | 6,700 m                                  |
| `BayerischeMeile`             | bayerische Meile                           | Bavarian mile                     | 25,406 Bavarian feet = 7,415 m           |
| `WuerttembergischeMeile`      | württembergische Meile                     | Württemberg mile                  | 26,000 Württemberg feet = 7,449 m        |
| `AnhaltischeMeile`            | anhaltische Meile                          | Anhalt mile                       | 7,532 m                                  |
| `SaechsischeMeile`            | sächsische Meile (späte Kalibrierung)      | Saxon mile, later calibration     | 7,500 m (later metric calibration)       |
| `AlteSaechsischeMeile`        | alte sächsische Meile                      | older Saxon mile                  | 32,000 Saxon feet = 9,062 m              |
| `SchleswigHolsteinischeMeile` | schleswig-holsteinische Meile              | Schleswig-Holstein mile           | 8,803 m                                  |
| `BadischeMeile`               | badische Meile (späte Kalibrierung)        | Baden mile, later calibration     | 8,000 m                                  |
| `BadischeMeileVor1810`        | badische Meile (vor 1810)                  | Baden mile before 1810            | 8,889 m                                  |
| `BadischeMeile1810Bis1871`    | badische Meile (1810-1871)                 | Baden mile, 1810-1871             | 8,944 m                                  |
| `HessischeMeile`              | hessische Meile (Hessen-Kassel)            | Hesse-Kassel mile                 | 9,206 m                                  |
| `LippeDetmolderMeile`         | Lippe-Detmolder Meile                      | Lippe-Detmold mile                | 9,264 m                                  |
| `WestfaelischeMeile`          | westfälische Meile (lange Variante)        | Westphalian mile, long variant    | 11,100 m                                 |
| `WestfaelischeMeileKurz`      | westfälische Meile (kurze Variante)        | Westphalian mile, shorter variant | 9,250 m                                  |
| `OldenburgerMeile`            | Oldenburger Meile                          | Oldenburg mile                    | 9,894 m                                  |
| `RheinlaendischeMeile`        | rheinländische Meile                       | Rhineland mile                    | 4,119 m                                  |
| `PfaelzischeMeile`            | pfälzische Meile                           | Palatinate mile                   | 4,630 m                                  |
| `OsnabrueckerMeile`           | Osnabrücker Meile                          | Osnabrück mile                    | 5,160 m                                  |
| `WiesbadenerMeile`            | Wiesbadener Meile                          | Wiesbaden mile                    | 1,000 m                                  |
| `OesterreichischePostmeile`   | österreichische Postmeile                  | Austrian post / police mile       | 3,910 Viennese Klafter = 7,415.2518144 m |
| `HelvetischeMeile`            | helvetische Meile (Konkordatsmaß)          | Helvetic mile, concordat standard | 2 Wegstunden = 9,600 m                   |
| `ZuercherMeile`               | Zürcher Meile (ältere lokale Kalibrierung) | older Zurich mile                 | older local calibration = 10,800 m       |
| `BernerMeile`                 | Berner Meile (ältere lokale Kalibrierung)  | older Bernese mile                | older local calibration = 10,560 m       |
+-------------------------------+--------------------------------------------+-----------------------------------+------------------------------------------+

The Bavarian, Württemberg, Saxon, Baden, and other regional values stay separate even
where their scales match.
For example, the later Saxon mile and the Reichsmeile are both 7,500 m, and the
historical names keep distinct definitions.
Different Baden periods and the two Westphalian values are separate units as well.

The Austrian post mile is its own entry.
A source for the 3,910-Klafter post / police / geographic mile gives 7,415.2518144 m,
and `OesterreichischeMeile`, of 4,000 Klafter, is the principal Austrian mile.
In Switzerland, the 1838 concordat measure gave a 4.8 km Wegstunde and a
two-Wegstunden Helvetic mile.
Older Zurich and Bern calibrations are separate entries.

Examples
--------
A Silesian post rider's six-mile stage converts without reading the historical road
log as modern miles:

>>> from kuchka.units.length import KILOMETRE
>>> BreslauerMeile(6).to(KILOMETRE)
40.2 km

A mapmaker comparing Saxon road systems quantifies a three-mile itinerary under the
older calibration:

>>> AlteSaechsischeMeile(3).to(KILOMETRE)
27.186 km

A Habsburg-era survey compares the 3,910-Klafter post-mile convention with the
principal Austrian mile:

>>> OesterreichischePostmeile(2).to(KILOMETRE)
14.8305036288 km

A Swiss itinerary from the concordat era uses two Helvetic miles, each defined as two
4.8 km Wegstunden:

>>> HelvetischeMeile(2).to(KILOMETRE)
19.2 km

Notes
-----
`GERMAN_REGIONAL_MEILE_UNITS` is a read-only `UnitTable` of the regional miles, and
`GERMAN_MEILE_UNITS_ALL` joins them with the principal miles of
`kuchka.units.archaic.german.length.meile`, so one table covers every spelling.
A spelling that two miles claim raises when the table is built.

For regional miles whose historical definition is a local foot or Klafter, the figures
here keep the published metric calibration.

Importing this module lets `Length` display in the regional miles and the principal
ones.

Sources
-------

- https://en.wikipedia.org/wiki/German_units_of_measurement
- https://de.wikipedia.org/wiki/Meile
- https://en.wikipedia.org/wiki/Obsolete_Austrian_units_of_measurement
- https://de.wikipedia.org/wiki/Alte_Ma%C3%9Fe_und_Gewichte_%28%C3%96sterreich%29
- https://hls-dhs-dss.ch/de/articles/013751/2011-03-31/
- https://www.e-periodica.ch/cntmng?pid=bhk-001%3A1995%3A4%3A%3A139

See Also
--------
~kuchka.quantities.Length
    The quantity every constructor in this module builds.
~kuchka.units.archaic.german.length.meile
    The principal German and Austrian miles.

"""

from __future__ import annotations

from fractions import Fraction
from typing import TYPE_CHECKING

from kuchka.dimensions import LENGTH
from kuchka.internal.unit_table import unit_table
from kuchka.internal.unit_table import units_of
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Length
from kuchka.quantities import UnitDef
from kuchka.quantities.base.units import extend_units
from kuchka.units.archaic.german.length.meile import GEOGRAPHISCHE_MEILE
from kuchka.units.archaic.german.length.meile import OESTERREICHISCHE_MEILE
from kuchka.units.archaic.german.length.meile import PREUSSISCHE_LANDMEILE
from kuchka.units.archaic.german.length.meile import REICHSMEILE
from kuchka.units.archaic.german.length.meile import GeographischeMeile
from kuchka.units.archaic.german.length.meile import OesterreichischeMeile
from kuchka.units.archaic.german.length.meile import PreussischeLandmeile
from kuchka.units.archaic.german.length.meile import Reichsmeile
from kuchka.units.length import METRE

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping


# Nominal scale from the historical source: 6,700 m.
BRESLAUER_MEILE = UnitDef(
    "breslauer_meile",
    "Breslauer Meile",
    Fraction(6700, 1) * METRE.scale,
    LENGTH,
    words=(
        "Breslauer Meile",
        "Breslauer Landmeile",
        "Silesian mile",
        "Breslau mile",
    ),
)

# Nominal scale from the historical source: 25,406 Bavarian feet = 7,415 m.
BAYERISCHE_MEILE = UnitDef(
    "bayerische_meile",
    "bayerische Meile",
    Fraction(7415, 1) * METRE.scale,
    LENGTH,
    words=(
        "bayerische Meile",
        "bairische Meile",
        "Bavarian mile",
    ),
)

# Nominal scale from the historical source: 26,000 Württemberg feet = 7,449 m.
WUERTTEMBERGISCHE_MEILE = UnitDef(
    "wuerttembergische_meile",
    "württembergische Meile",
    Fraction(7449, 1) * METRE.scale,
    LENGTH,
    words=(
        "württembergische Meile",
        "wuerttembergische Meile",
        "Württemberg mile",
        "Wuerttemberg mile",
    ),
)

# Nominal scale from the historical source: 7,532 m.
ANHALTISCHE_MEILE = UnitDef(
    "anhaltische_meile",
    "anhaltische Meile",
    Fraction(7532, 1) * METRE.scale,
    LENGTH,
    words=(
        "anhaltische Meile",
        "Anhalt mile",
    ),
)

# Nominal scale from the historical source: 7,500 m (later metric calibration).
SAECHSISCHE_MEILE = UnitDef(
    "saechsische_meile",
    "sächsische Meile (späte Kalibrierung)",
    Fraction(7500, 1) * METRE.scale,
    LENGTH,
    words=(
        "sächsische Meile",
        "saechsische Meile",
        "Saxon mile (later calibration)",
    ),
)

# Nominal scale from the historical source: 32,000 Saxon feet = 9,062 m.
ALTE_SAECHSISCHE_MEILE = UnitDef(
    "alte_saechsische_meile",
    "alte sächsische Meile",
    Fraction(9062, 1) * METRE.scale,
    LENGTH,
    words=(
        "alte sächsische Meile",
        "alte saechsische Meile",
        "Saxon mile (32,000 Saxon feet)",
        "older Saxon mile",
    ),
)

# Nominal scale from the historical source: 8,803 m.
SCHLESWIG_HOLSTEINISCHE_MEILE = UnitDef(
    "schleswig_holsteinische_meile",
    "schleswig-holsteinische Meile",
    Fraction(8803, 1) * METRE.scale,
    LENGTH,
    words=(
        "schleswig-holsteinische Meile",
        "Schleswig-Holstein mile",
    ),
)

# Nominal scale from the historical source: 8,000 m.
BADISCHE_MEILE = UnitDef(
    "badische_meile",
    "badische Meile (späte Kalibrierung)",
    Fraction(8000, 1) * METRE.scale,
    LENGTH,
    words=(
        "badische Meile",
        "Badische Meile (8 km)",
        "Baden mile (later calibration)",
    ),
)

# Nominal scale from the historical source: 8,889 m.
BADISCHE_MEILE_VOR_1810 = UnitDef(
    "badische_meile_vor1810",
    "badische Meile (vor 1810)",
    Fraction(8889, 1) * METRE.scale,
    LENGTH,
    words=(
        "badische Meile vor 1810",
        "badische Meile (vor 1810)",
        "Baden mile before 1810",
    ),
)

# Nominal scale from the historical source: 8,944 m.
BADISCHE_MEILE_1810_BIS_1871 = UnitDef(
    "badische_meile1810_bis1871",
    "badische Meile (1810-1871)",
    Fraction(8944, 1) * METRE.scale,
    LENGTH,
    words=(
        "badische Meile 1810-1871",
        "badische Meile (1810 bis 1871)",
        "Baden mile 1810-1871",
    ),
)

# Nominal scale from the historical source: 9,206 m.
HESSISCHE_MEILE = UnitDef(
    "hessische_meile",
    "hessische Meile (Hessen-Kassel)",
    Fraction(9206, 1) * METRE.scale,
    LENGTH,
    words=(
        "hessische Meile",
        "Hessen-Kasseler Meile",
        "Hesse-Kassel mile",
    ),
)

# Nominal scale from the historical source: 9,264 m.
LIPPE_DETMOLDER_MEILE = UnitDef(
    "lippe_detmolder_meile",
    "Lippe-Detmolder Meile",
    Fraction(9264, 1) * METRE.scale,
    LENGTH,
    words=(
        "Lippe-Detmolder Meile",
        "Lippe-Detmold mile",
    ),
)

# Nominal scale from the historical source: 11,100 m.
WESTFAELISCHE_MEILE = UnitDef(
    "westfaelische_meile",
    "westfälische Meile (lange Variante)",
    Fraction(11100, 1) * METRE.scale,
    LENGTH,
    words=(
        "westfälische Meile (11,100 m)",
        "westfaelische Meile (11,100 m)",
        "Westphalian mile (long variant)",
    ),
)

# Nominal scale from the historical source: 9,250 m.
WESTFAELISCHE_MEILE_KURZ = UnitDef(
    "westfaelische_meile_kurz",
    "westfälische Meile (kurze Variante)",
    Fraction(9250, 1) * METRE.scale,
    LENGTH,
    words=(
        "westfälische Meile (9,250 m)",
        "westfaelische Meile (9,250 m)",
        "Westphalian mile (short variant)",
    ),
)

# Nominal scale from the historical source: 9,894 m.
OLDENBURGER_MEILE = UnitDef(
    "oldenburger_meile",
    "Oldenburger Meile",
    Fraction(9894, 1) * METRE.scale,
    LENGTH,
    words=(
        "Oldenburger Meile",
        "Oldenburg mile",
    ),
)

# Nominal scale from the historical source: 4,119 m.
RHEINLAENDISCHE_MEILE = UnitDef(
    "rheinlaendische_meile",
    "rheinländische Meile",
    Fraction(4119, 1) * METRE.scale,
    LENGTH,
    words=(
        "rheinländische Meile",
        "rheinlaendische Meile",
        "Rhineland mile",
    ),
)

# Nominal scale from the historical source: 4,630 m.
PFAELZISCHE_MEILE = UnitDef(
    "pfaelzische_meile",
    "pfälzische Meile",
    Fraction(4630, 1) * METRE.scale,
    LENGTH,
    words=(
        "pfälzische Meile",
        "pfaelzische Meile",
        "Palatinate mile",
        "Pfalz mile",
    ),
)

# Nominal scale from the historical source: 5,160 m.
OSNABRUECKER_MEILE = UnitDef(
    "osnabruecker_meile",
    "Osnabrücker Meile",
    Fraction(5160, 1) * METRE.scale,
    LENGTH,
    words=(
        "Osnabrücker Meile",
        "Osnabruecker Meile",
        "Osnabrück mile",
        "Osnabruck mile",
    ),
)

# Nominal scale from the historical source: 1,000 m.
WIESBADENER_MEILE = UnitDef(
    "wiesbadener_meile",
    "Wiesbadener Meile",
    Fraction(1000, 1) * METRE.scale,
    LENGTH,
    words=(
        "Wiesbadener Meile",
        "Wiesbaden mile",
    ),
)

# Nominal scale from the historical source: 3,910 Viennese Klafter = 7,415.2518144 m.
OESTERREICHISCHE_POSTMEILE = UnitDef(
    "oesterreichische_postmeile",
    "österreichische Postmeile",
    Fraction(579316548, 78125) * METRE.scale,
    LENGTH,
    words=(
        "österreichische Postmeile",
        "oesterreichische Postmeile",
        "österreichische Polizeimeile",
        "oesterreichische Polizeimeile",
        "österreichische geographische Meile",
        "oesterreichische geographische Meile",
        "Austrian post mile",
        "Austrian police mile",
        "Austrian geographical mile",
    ),
)

# Nominal scale from the historical source: 2 Wegstunden = 9,600 m.
HELVETISCHE_MEILE = UnitDef(
    "helvetische_meile",
    "helvetische Meile (Konkordatsmaß)",
    Fraction(9600, 1) * METRE.scale,
    LENGTH,
    words=(
        "helvetische Meile",
        "helvetische Meile (Konkordatsmaß)",
        "helvetische Meile (Konkordatsmass)",
        "Helvetic mile (concordat standard)",
    ),
)

# Nominal scale from the historical source: older local calibration = 10,800 m.
ZUERCHER_MEILE = UnitDef(
    "zuercher_meile",
    "Zürcher Meile (ältere lokale Kalibrierung)",
    Fraction(10800, 1) * METRE.scale,
    LENGTH,
    words=(
        "Zürcher Meile",
        "Zuercher Meile",
        "Zürcher helvetische Meile",
        "Zurich mile (older calibration)",
    ),
)

# Nominal scale from the historical source: older local calibration = 10,560 m.
BERNER_MEILE = UnitDef(
    "berner_meile",
    "Berner Meile (ältere lokale Kalibrierung)",
    Fraction(10560, 1) * METRE.scale,
    LENGTH,
    words=(
        "Berner Meile",
        "Bernese mile",
        "Berner helvetische Meile",
        "Bernese mile (older calibration)",
    ),
)


def BreslauerMeile(value: Numeric) -> Length:
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
    Reported as used throughout Silesia.

    Examples
    --------
    A Silesian post rider has six Breslau miles between dispatch stations:

    >>> distance = BreslauerMeile(6)
    >>> from kuchka.units.length import KILOMETRE
    >>> distance.to(KILOMETRE)
    40.2 km

    """
    return Length(to_exact(value) * BRESLAUER_MEILE.scale, BRESLAUER_MEILE)


def BayerischeMeile(value: Numeric) -> Length:
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
    The historical table relates this value to 25,406 Bavarian feet and
    approximately one fifteenth of an equatorial degree.

    Examples
    --------
    A Bavarian survey party marks a four-mile leg between market towns:

    >>> distance = BayerischeMeile(4)
    >>> from kuchka.units.length import KILOMETRE
    >>> distance.to(KILOMETRE)
    29.66 km

    """
    return Length(to_exact(value) * BAYERISCHE_MEILE.scale, BAYERISCHE_MEILE)


def WuerttembergischeMeile(value: Numeric) -> Length:
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
    The listed metric equivalent for the Württemberg mile is 7,449 m.

    Examples
    --------
    A Württemberg travel journal records three miles between overnight inns:

    >>> distance = WuerttembergischeMeile(3)
    >>> from kuchka.units.length import KILOMETRE
    >>> distance.to(KILOMETRE)
    22.347 km

    """
    return Length(
        to_exact(value) * WUERTTEMBERGISCHE_MEILE.scale, WUERTTEMBERGISCHE_MEILE
    )


def AnhaltischeMeile(value: Numeric) -> Length:
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
    The regional table reports 7,532 m.

    Examples
    --------
    An Anhalt estate map labels a boundary road as five miles long:

    >>> distance = AnhaltischeMeile(5)
    >>> from kuchka.units.length import KILOMETRE
    >>> distance.to(KILOMETRE)
    37.66 km

    """
    return Length(to_exact(value) * ANHALTISCHE_MEILE.scale, ANHALTISCHE_MEILE)


def SaechsischeMeile(value: Numeric) -> Length:
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
    Saxony used a 7,500 m mile in a later period; this is distinct from the older
    32,000-Saxon-foot calibration.

    Examples
    --------
    A later Saxon route register records eight miles from one postal district to the
    next:

    >>> distance = SaechsischeMeile(8)
    >>> from kuchka.units.length import KILOMETRE
    >>> distance.to(KILOMETRE)
    60 km

    """
    return Length(to_exact(value) * SAECHSISCHE_MEILE.scale, SAECHSISCHE_MEILE)


def AlteSaechsischeMeile(value: Numeric) -> Length:
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
    The older Saxon value is reported as 32,000 Saxon feet, approximately 9,062 m.

    Examples
    --------
    A historian reconstructs a three-mile itinerary from an eighteenth-century Saxon
    register:

    >>> distance = AlteSaechsischeMeile(3)
    >>> from kuchka.units.length import KILOMETRE
    >>> distance.to(KILOMETRE)
    27.186 km

    """
    return Length(
        to_exact(value) * ALTE_SAECHSISCHE_MEILE.scale, ALTE_SAECHSISCHE_MEILE
    )


def SchleswigHolsteinischeMeile(value: Numeric) -> Length:
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
    The regional table reports 8,803 m.

    Examples
    --------
    A coastal courier schedule allows four local miles between relay posts:

    >>> distance = SchleswigHolsteinischeMeile(4)
    >>> from kuchka.units.length import KILOMETRE
    >>> distance.to(KILOMETRE)
    35.212 km

    """
    return Length(
        to_exact(value) * SCHLESWIG_HOLSTEINISCHE_MEILE.scale,
        SCHLESWIG_HOLSTEINISCHE_MEILE,
    )


def BadischeMeile(value: Numeric) -> Length:
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
    The listed later Baden value is 8,000 m; older values are kept as separate
    constructors.

    Examples
    --------
    A Baden road ledger in the later calibration adds up three miles of repaired
    road:

    >>> distance = BadischeMeile(3)
    >>> from kuchka.units.length import KILOMETRE
    >>> distance.to(KILOMETRE)
    24 km

    """
    return Length(to_exact(value) * BADISCHE_MEILE.scale, BADISCHE_MEILE)


def BadischeMeileVor1810(value: Numeric) -> Length:
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
    The source gives 8,889 m for the earlier Baden calibration, before 1810.

    Examples
    --------
    A pre-1810 Baden itinerary lists two miles between customs houses:

    >>> distance = BadischeMeileVor1810(2)
    >>> from kuchka.units.length import KILOMETRE
    >>> distance.to(KILOMETRE)
    17.778 km

    """
    return Length(
        to_exact(value) * BADISCHE_MEILE_VOR_1810.scale, BADISCHE_MEILE_VOR_1810
    )


def BadischeMeile1810Bis1871(value: Numeric) -> Length:
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
    The source gives 8,944 m for the Baden calibration between the 1810 and 1871
    changes.

    Examples
    --------
    A nineteenth-century Baden coach log totals two miles between staging inns:

    >>> distance = BadischeMeile1810Bis1871(2)
    >>> from kuchka.units.length import KILOMETRE
    >>> distance.to(KILOMETRE)
    17.888 km

    """
    return Length(
        to_exact(value) * BADISCHE_MEILE_1810_BIS_1871.scale,
        BADISCHE_MEILE_1810_BIS_1871,
    )


def HessischeMeile(value: Numeric) -> Length:
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
    The regional table reports 9,206 m for Hesse-Kassel.

    Examples
    --------
    A Hesse-Kassel courier changes horses after a three-mile stage:

    >>> distance = HessischeMeile(3)
    >>> from kuchka.units.length import KILOMETRE
    >>> distance.to(KILOMETRE)
    27.618 km

    """
    return Length(to_exact(value) * HESSISCHE_MEILE.scale, HESSISCHE_MEILE)


def LippeDetmolderMeile(value: Numeric) -> Length:
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
    The regional table reports 9,264 m.

    Examples
    --------
    An archivist converts a two-mile passage from a Lippe-Detmold itinerary:

    >>> distance = LippeDetmolderMeile(2)
    >>> from kuchka.units.length import KILOMETRE
    >>> distance.to(KILOMETRE)
    18.528 km

    """
    return Length(to_exact(value) * LIPPE_DETMOLDER_MEILE.scale, LIPPE_DETMOLDER_MEILE)


def WestfaelischeMeile(value: Numeric) -> Length:
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
    One source lists a long Westphalian variant of 11,100 m.

    Examples
    --------
    A Westphalian stagecoach route measures two long miles between major towns:

    >>> distance = WestfaelischeMeile(2)
    >>> from kuchka.units.length import KILOMETRE
    >>> distance.to(KILOMETRE)
    22.2 km

    """
    return Length(to_exact(value) * WESTFAELISCHE_MEILE.scale, WESTFAELISCHE_MEILE)


def WestfaelischeMeileKurz(value: Numeric) -> Length:
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
    The same regional table also records a shorter Westphalian variant of 9,250 m.

    Examples
    --------
    A local Westphalian route book uses the shorter value for two stages:

    >>> distance = WestfaelischeMeileKurz(2)
    >>> from kuchka.units.length import KILOMETRE
    >>> distance.to(KILOMETRE)
    18.5 km

    """
    return Length(
        to_exact(value) * WESTFAELISCHE_MEILE_KURZ.scale, WESTFAELISCHE_MEILE_KURZ
    )


def OldenburgerMeile(value: Numeric) -> Length:
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
    The regional table reports 9,894 m.

    Examples
    --------
    A surveyor translates three Oldenburg miles from a boundary description:

    >>> distance = OldenburgerMeile(3)
    >>> from kuchka.units.length import KILOMETRE
    >>> distance.to(KILOMETRE)
    29.682 km

    """
    return Length(to_exact(value) * OLDENBURGER_MEILE.scale, OLDENBURGER_MEILE)


def RheinlaendischeMeile(value: Numeric) -> Length:
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
    The regional table reports 4,119 m; this is much shorter than the geographic
    mile.

    Examples
    --------
    A Rhineland market route recorded as four miles is converted for a modern map:

    >>> distance = RheinlaendischeMeile(4)
    >>> from kuchka.units.length import KILOMETRE
    >>> distance.to(KILOMETRE)
    16.476 km

    """
    return Length(to_exact(value) * RHEINLAENDISCHE_MEILE.scale, RHEINLAENDISCHE_MEILE)


def PfaelzischeMeile(value: Numeric) -> Length:
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
    The regional table reports 4,630 m.

    Examples
    --------
    A Palatinate tax record describes a five-mile road between villages:

    >>> distance = PfaelzischeMeile(5)
    >>> from kuchka.units.length import KILOMETRE
    >>> distance.to(KILOMETRE)
    23.15 km

    """
    return Length(to_exact(value) * PFAELZISCHE_MEILE.scale, PFAELZISCHE_MEILE)


def OsnabrueckerMeile(value: Numeric) -> Length:
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
    The English-language table gives 5,160 m for the Osnabrück/France entry.

    Examples
    --------
    A travelling merchant converts two Osnabrück miles into kilometres:

    >>> distance = OsnabrueckerMeile(2)
    >>> from kuchka.units.length import KILOMETRE
    >>> distance.to(KILOMETRE)
    10.32 km

    """
    return Length(to_exact(value) * OSNABRUECKER_MEILE.scale, OSNABRUECKER_MEILE)


def WiesbadenerMeile(value: Numeric) -> Length:
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
    The regional table lists this unusually short Wiesbaden measure as 1,000 m.

    Examples
    --------
    A Wiesbaden municipal note records three local miles of roadworks:

    >>> distance = WiesbadenerMeile(3)
    >>> from kuchka.units.length import KILOMETRE
    >>> distance.to(KILOMETRE)
    3 km

    """
    return Length(to_exact(value) * WIESBADENER_MEILE.scale, WIESBADENER_MEILE)


def OesterreichischePostmeile(value: Numeric) -> Length:
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
    A separate Austrian entry gives the post, police, and Austrian geographic mile
    as 3,910 Viennese Klafter. It is kept separate from the 4,000-Klafter Austrian
    mile.

    Examples
    --------
    A post route described in the 3,910-Klafter convention covers two such miles:

    >>> distance = OesterreichischePostmeile(2)
    >>> from kuchka.units.length import KILOMETRE
    >>> distance.to(KILOMETRE)
    14.8305036288 km

    """
    return Length(
        to_exact(value) * OESTERREICHISCHE_POSTMEILE.scale, OESTERREICHISCHE_POSTMEILE
    )


def HelvetischeMeile(value: Numeric) -> Length:
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
    Under the Swiss concordat system implemented from 1838, a Wegstunde was 16,000
    feet or 4.8 km; the Helvetic mile was two Wegstunden.

    Examples
    --------
    A nineteenth-century Swiss route book records two Helvetic miles between
    cantonal centres:

    >>> distance = HelvetischeMeile(2)
    >>> from kuchka.units.length import KILOMETRE
    >>> distance.to(KILOMETRE)
    19.2 km

    """
    return Length(to_exact(value) * HELVETISCHE_MEILE.scale, HELVETISCHE_MEILE)


def ZuercherMeile(value: Numeric) -> Length:
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
    The historical comparative table gives 10.8 km for the older Zurich helvetic-
    mile calibration; it predates the later concordat standard.

    Examples
    --------
    A Zurich travel ledger uses two miles under the older local measure:

    >>> distance = ZuercherMeile(2)
    >>> from kuchka.units.length import KILOMETRE
    >>> distance.to(KILOMETRE)
    21.6 km

    """
    return Length(to_exact(value) * ZUERCHER_MEILE.scale, ZUERCHER_MEILE)


def BernerMeile(value: Numeric) -> Length:
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
    The historical comparative table gives 10.56 km for the older Bernese helvetic-
    mile calibration; it predates the later concordat standard.

    Examples
    --------
    A Bernese itinerary records two miles under its older local calibration:

    >>> distance = BernerMeile(2)
    >>> from kuchka.units.length import KILOMETRE
    >>> distance.to(KILOMETRE)
    21.12 km

    """
    return Length(to_exact(value) * BERNER_MEILE.scale, BERNER_MEILE)


GERMAN_REGIONAL_MEILE_UNITS: Mapping[str, Callable[[Numeric], Length]] = unit_table(
    "GERMAN_REGIONAL_MEILE_UNITS",
    {
        BRESLAUER_MEILE: BreslauerMeile,
        BAYERISCHE_MEILE: BayerischeMeile,
        WUERTTEMBERGISCHE_MEILE: WuerttembergischeMeile,
        ANHALTISCHE_MEILE: AnhaltischeMeile,
        SAECHSISCHE_MEILE: SaechsischeMeile,
        ALTE_SAECHSISCHE_MEILE: AlteSaechsischeMeile,
        SCHLESWIG_HOLSTEINISCHE_MEILE: SchleswigHolsteinischeMeile,
        BADISCHE_MEILE: BadischeMeile,
        BADISCHE_MEILE_VOR_1810: BadischeMeileVor1810,
        BADISCHE_MEILE_1810_BIS_1871: BadischeMeile1810Bis1871,
        HESSISCHE_MEILE: HessischeMeile,
        LIPPE_DETMOLDER_MEILE: LippeDetmolderMeile,
        WESTFAELISCHE_MEILE: WestfaelischeMeile,
        WESTFAELISCHE_MEILE_KURZ: WestfaelischeMeileKurz,
        OLDENBURGER_MEILE: OldenburgerMeile,
        RHEINLAENDISCHE_MEILE: RheinlaendischeMeile,
        PFAELZISCHE_MEILE: PfaelzischeMeile,
        OSNABRUECKER_MEILE: OsnabrueckerMeile,
        WIESBADENER_MEILE: WiesbadenerMeile,
        OESTERREICHISCHE_POSTMEILE: OesterreichischePostmeile,
        HELVETISCHE_MEILE: HelvetischeMeile,
        ZUERCHER_MEILE: ZuercherMeile,
        BERNER_MEILE: BernerMeile,
    },
)
"""The regional miles by spelling, for configuration files and external interfaces."""

GERMAN_MEILE_UNITS_ALL: Mapping[str, Callable[[Numeric], Length]] = unit_table(
    "GERMAN_MEILE_UNITS_ALL",
    {
        GEOGRAPHISCHE_MEILE: GeographischeMeile,
        BRESLAUER_MEILE: BreslauerMeile,
        BAYERISCHE_MEILE: BayerischeMeile,
        WUERTTEMBERGISCHE_MEILE: WuerttembergischeMeile,
        REICHSMEILE: Reichsmeile,
        ANHALTISCHE_MEILE: AnhaltischeMeile,
        PREUSSISCHE_LANDMEILE: PreussischeLandmeile,
        SAECHSISCHE_MEILE: SaechsischeMeile,
        ALTE_SAECHSISCHE_MEILE: AlteSaechsischeMeile,
        SCHLESWIG_HOLSTEINISCHE_MEILE: SchleswigHolsteinischeMeile,
        BADISCHE_MEILE: BadischeMeile,
        BADISCHE_MEILE_VOR_1810: BadischeMeileVor1810,
        BADISCHE_MEILE_1810_BIS_1871: BadischeMeile1810Bis1871,
        HESSISCHE_MEILE: HessischeMeile,
        LIPPE_DETMOLDER_MEILE: LippeDetmolderMeile,
        WESTFAELISCHE_MEILE: WestfaelischeMeile,
        WESTFAELISCHE_MEILE_KURZ: WestfaelischeMeileKurz,
        OLDENBURGER_MEILE: OldenburgerMeile,
        RHEINLAENDISCHE_MEILE: RheinlaendischeMeile,
        PFAELZISCHE_MEILE: PfaelzischeMeile,
        OSNABRUECKER_MEILE: OsnabrueckerMeile,
        WIESBADENER_MEILE: WiesbadenerMeile,
        OESTERREICHISCHE_MEILE: OesterreichischeMeile,
        OESTERREICHISCHE_POSTMEILE: OesterreichischePostmeile,
        HELVETISCHE_MEILE: HelvetischeMeile,
        ZUERCHER_MEILE: ZuercherMeile,
        BERNER_MEILE: BernerMeile,
    },
)
"""The principal and the regional miles by spelling in one table."""

# Importing this module makes Length display in the units of its tables.
extend_units(Length, units_of(GERMAN_MEILE_UNITS_ALL))


__all__ = [
    "ALTE_SAECHSISCHE_MEILE",
    "ANHALTISCHE_MEILE",
    "BADISCHE_MEILE",
    "BADISCHE_MEILE_1810_BIS_1871",
    "BADISCHE_MEILE_VOR_1810",
    "BAYERISCHE_MEILE",
    "BERNER_MEILE",
    "BRESLAUER_MEILE",
    "GERMAN_MEILE_UNITS_ALL",
    "GERMAN_REGIONAL_MEILE_UNITS",
    "HELVETISCHE_MEILE",
    "HESSISCHE_MEILE",
    "LIPPE_DETMOLDER_MEILE",
    "OESTERREICHISCHE_POSTMEILE",
    "OLDENBURGER_MEILE",
    "OSNABRUECKER_MEILE",
    "PFAELZISCHE_MEILE",
    "RHEINLAENDISCHE_MEILE",
    "SAECHSISCHE_MEILE",
    "SCHLESWIG_HOLSTEINISCHE_MEILE",
    "WESTFAELISCHE_MEILE",
    "WESTFAELISCHE_MEILE_KURZ",
    "WIESBADENER_MEILE",
    "WUERTTEMBERGISCHE_MEILE",
    "ZUERCHER_MEILE",
    "AlteSaechsischeMeile",
    "AnhaltischeMeile",
    "BadischeMeile",
    "BadischeMeile1810Bis1871",
    "BadischeMeileVor1810",
    "BayerischeMeile",
    "BernerMeile",
    "BreslauerMeile",
    "HelvetischeMeile",
    "HessischeMeile",
    "LippeDetmolderMeile",
    "OesterreichischePostmeile",
    "OldenburgerMeile",
    "OsnabrueckerMeile",
    "PfaelzischeMeile",
    "RheinlaendischeMeile",
    "SaechsischeMeile",
    "SchleswigHolsteinischeMeile",
    "WestfaelischeMeile",
    "WestfaelischeMeileKurz",
    "WiesbadenerMeile",
    "WuerttembergischeMeile",
    "ZuercherMeile",
]
