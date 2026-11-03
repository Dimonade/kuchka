"""Length quantities and constructors for engineering, science, and space.

`Length` represents one-dimensional distance. The metre is the canonical SI base unit,
while the constructors in this module provide convenient entry points from metric
prefixes and a small set of exact non-SI units.

`Metre` is the canonical spelling adopted by the BIPM.
American spellings (`Meter`, `Millimeter`, `Kilometer`, ...) are true aliases of the
same objects, not wrappers or duplicate implementations.
Both spellings display using the same SI symbols.

Every imperial unit implemented here is an **exact** decimal multiple of the metre.
Since the 1959 international yard and pound agreement, conversions such as
`1 in = 25.4 mm` and `1 ft = 0.3048 m` are exact, so they preserve the same `Decimal`
precision guarantees as SI prefixes.

The astronomical unit and light-year extend the same `Length` quantity to astronomical
scales. The astronomical unit (`au`) is an exact conventional length, while the
light-year (`ly`) is the exact distance light travels in a Julian year.
The parsec (`pc`) is defined as exactly 648000/pi astronomical units, the distance at
which one astronomical unit subtends one arcsecond.
Pi is irrational, so kuchka holds a parsec as that quotient with pi to 100 decimal
places (`kuchka.internal.constants.PI`), the same pi `Radian` uses: the parsec is within
one part in 1E+100 of its defined length, and the parsecs, kiloparsecs, and megaparsecs
among themselves stay exact.

Examples
--------
A machined enclosure combines metric tolerances with an imperial connector:

>>> panel_width = Millimetre(120)
>>> connector_cutout = Inch(0.5)
>>> remaining_material = panel_width - connector_cutout
>>> remaining_material
107.3 mm

The same `Length` quantity naturally spans microscopy and manufacturing.
A human hair is roughly 70 µm thick:

>>> hair_diameter = Micrometre(70)

Modern semiconductor processes are measured in nanometres:

>>> transistor_node = Nanometre(3)

Large distances remain the same quantity.
A marathon is 42.195 km:

>>> marathon = Kilometre(42.195)

Aviation and marine navigation traditionally use nautical miles.
Flying 120 NM corresponds to exactly 222.24 km:

>>> flight_leg = NauticalMile(120)
>>> equivalent = Kilometre(222.24)
>>> flight_leg == equivalent
True

The Apollo 11 landing site is about 384,400 km from Earth on average:

>>> earth_to_moon = Kilometre(384400)

The astronomical unit moves the same quantity into planetary-scale distances.
One astronomical unit is the conventional Earth-Sun distance scale:

>>> earth_sun_distance = AstronomicalUnit(1)
>>> earth_sun_distance.to(KILOMETRE)
149597870.7 km

Light-years extend `Length` from the Solar System to interstellar space.
A distance of 4.25 light-years is a useful representative stellar scale:

>>> stellar_neighborhood = LightYear(Decimal("4.25"))
>>> stellar_neighborhood.to(KILOMETRE)
40208104508468.4 km

It is also possible to be cheesy and correct at the same time.
"I love you to the moon and back" is, at least dimensionally, a well-formed `Length`:

>>> distance_to_moon = Kilometre(384_400)
>>> 2 * distance_to_moon
768800 km

Notes
-----
Metric prefixes represent exact powers of ten.

Imperial units implemented by this module are exact by definition, not measured
approximations. This means comparisons such as

>>> Inch(1) == Millimetre(25.4)
True

hold exactly.

The astronomical unit is defined exactly as:

    1 au = 149597870700 m

The parsec is defined by the IAU (2015, resolution B2) as:

    1 pc = 648000 / pi au = 3.0856775814913672789139...e16 m

The light-year is defined from the exact speed of light and the Julian year of
365.25 days:

    1 ly = 9460730472580800 m

`LENGTH_UNITS` maps symbols such as ``"mm"``, ``"km"``, ``"in"``, ``"au"``,
``"ly"``, and ``"pc"`` to their constructors for configuration files and other
external interfaces.

See Also
--------
~kuchka.quantities.Area
    Surface quantities derived from length.
~kuchka.quantities.Volume
    Volumes derived from cubic length.
~kuchka.quantities.Velocity
    Distance travelled per unit time.

"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from typing import TYPE_CHECKING

from kuchka.dimensions import LENGTH
from kuchka.internal import prefixes
from kuchka.internal import symbols
from kuchka.internal.constants import PI
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.prefixes import with_prefix
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Length
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

METRE_NAME = "metre"
METRE_SYMBOL = "m"
METRE_WORDS = ("meter",)
"""The American spelling, which prefixed names follow: `kilometer`."""

PICOMETRE = prefixed_unit(
    prefixes.PICO, METRE_NAME, METRE_SYMBOL, LENGTH, base_words=METRE_WORDS
)
NANOMETRE = prefixed_unit(
    prefixes.NANO, METRE_NAME, METRE_SYMBOL, LENGTH, base_words=METRE_WORDS
)
MICROMETRE = prefixed_unit(
    prefixes.MICRO,
    METRE_NAME,
    METRE_SYMBOL,
    LENGTH,
    base_words=METRE_WORDS,
    words=("micron",),
)
MILLIMETRE = prefixed_unit(
    prefixes.MILLI, METRE_NAME, METRE_SYMBOL, LENGTH, base_words=METRE_WORDS
)
CENTIMETRE = prefixed_unit(
    prefixes.CENTI, METRE_NAME, METRE_SYMBOL, LENGTH, base_words=METRE_WORDS
)
DECIMETRE = prefixed_unit(
    prefixes.DECI, METRE_NAME, METRE_SYMBOL, LENGTH, base_words=METRE_WORDS
)
METRE = prefixed_unit(
    prefixes.UNIT, METRE_NAME, METRE_SYMBOL, LENGTH, base_words=METRE_WORDS
)
KILOMETRE = prefixed_unit(
    prefixes.KILO, METRE_NAME, METRE_SYMBOL, LENGTH, base_words=METRE_WORDS
)

PICOMETER = PICOMETRE
NANOMETER = NANOMETRE
MICROMETER = MICROMETRE
MILLIMETER = MILLIMETRE
CENTIMETER = CENTIMETRE
DECIMETER = DECIMETRE
METER = METRE
KILOMETER = KILOMETRE


Length._canonical_unit = METRE  # noqa: SLF001 -- this module owns Length's canonical unit


def Picometre(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in picometres.

    Parameters
    ----------
    value : Numeric
        Length magnitude in picometres.

    Returns
    -------
    Length
        Length represented in picometres.

    Examples
    --------
    A typical covalent bond is about 154 pm long:

    >>> carbon_bond = Picometre(154)

    """
    return Length(to_exact(value) * PICOMETRE.scale, PICOMETRE)


def Nanometre(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in nanometres.

    Parameters
    ----------
    value : Numeric
        Length magnitude in nanometres.

    Returns
    -------
    Length
        Length represented in nanometres.

    Examples
    --------
    A modern 3 nm transistor process is measured on the nanometre scale:

    >>> process_node = Nanometre(3)

    """
    return Length(to_exact(value) * NANOMETRE.scale, NANOMETRE)


def Micrometre(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in micrometres.

    Parameters
    ----------
    value : Numeric
        Length magnitude in micrometres.

    Returns
    -------
    Length
        Length represented in micrometres.

    Examples
    --------
    A human hair is approximately 70 µm thick:

    >>> hair = Micrometre(70)

    """
    return Length(to_exact(value) * MICROMETRE.scale, MICROMETRE)


def Millimetre(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in millimetres.

    Parameters
    ----------
    value : Numeric
        Length magnitude in millimetres.

    Returns
    -------
    Length
        Length represented in millimetres.

    Examples
    --------
    Two machined parts with a 0.2 mm clearance produce a precise assembly gap:

    >>> shaft = Millimetre(12)
    >>> bore = Millimetre(12.2)
    >>> clearance = bore - shaft
    >>> clearance
    0.2 mm

    """
    return Length(to_exact(value) * MILLIMETRE.scale, MILLIMETRE)


def Centimetre(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in centimetres.

    Parameters
    ----------
    value : Numeric
        Length magnitude in centimetres.

    Returns
    -------
    Length
        Length represented in centimetres.

    Examples
    --------
    A postcard is about 15 cm wide:

    >>> postcard_width = Centimetre(15)

    """
    return Length(to_exact(value) * CENTIMETRE.scale, CENTIMETRE)


def Decimetre(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in decimetres.

    Parameters
    ----------
    value : Numeric
        Length magnitude in decimetres.

    Returns
    -------
    Length
        Length represented in decimetres.

    Examples
    --------
    A 6 dm ruler is exactly 60 cm long:

    >>> drafting_ruler = Decimetre(6)

    """
    return Length(to_exact(value) * DECIMETRE.scale, DECIMETRE)


def Metre(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in metres.

    Parameters
    ----------
    value : Numeric
        Length magnitude in metres.

    Returns
    -------
    Length
        Length represented in metres.

    Examples
    --------
    The high jump world-class bar height is around two and a half metres:

    >>> high_jump_bar = Metre(2.45)

    """
    return Length(to_exact(value) * METRE.scale, METRE)


def Kilometre(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in kilometres.

    Parameters
    ----------
    value : Numeric
        Length magnitude in kilometres.

    Returns
    -------
    Length
        Length represented in kilometres.

    Examples
    --------
    The official marathon distance is 42.195 km:

    >>> marathon = Kilometre(42.195)

    """
    return Length(to_exact(value) * KILOMETRE.scale, KILOMETRE)


Picometer = Picometre
Nanometer = Nanometre
Micrometer = Micrometre
Millimeter = Millimetre
Centimeter = Centimetre
Decimeter = Decimetre
Meter = Metre
Kilometer = Kilometre


# Non-SI units.

INCH = UnitDef(
    "inch",
    "in",
    Decimal("0.0254"),
    LENGTH,
    aliases=('"', symbols.DOUBLE_PRIME, "''"),
    words=("inches",),
)


def Inch(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in inches.

    Parameters
    ----------
    value : Numeric
        Length magnitude in inches.

    Returns
    -------
    Length
        Length represented in inches.

    Notes
    -----
    One inch is defined as exactly 25.4 millimetres.

    Examples
    --------
    A 3D printer enclosure may combine imperial hardware with metric sheet metal:

    >>> screw_spacing = Inch(2)
    >>> panel_width = Millimetre(80)
    >>> usable_width = panel_width - screw_spacing
    >>> usable_width
    29.2 mm

    """
    return Length(to_exact(value) * INCH.scale, INCH)


FOOT = UnitDef(
    "foot",
    "ft",
    Decimal("0.3048"),
    LENGTH,
    aliases=("'", symbols.PRIME),
    words=("feet",),
)


def Foot(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in feet.

    Parameters
    ----------
    value : Numeric
        Length magnitude in feet.

    Returns
    -------
    Length
        Length represented in feet.

    Examples
    --------
    A standard basketball hoop is 10 ft above the floor:

    >>> hoop_height = Foot(10)

    """
    return Length(to_exact(value) * FOOT.scale, FOOT)


YARD = UnitDef("yard", "yd", Decimal("0.9144"), LENGTH)


def Yard(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in yards.

    Parameters
    ----------
    value : Numeric
        Length magnitude in yards.

    Returns
    -------
    Length
        Length represented in yards.

    Examples
    --------
    The width of an American football field is 53 and 1/3 yards:

    >>> field_width = Yard(53.3333333333)

    """
    return Length(to_exact(value) * YARD.scale, YARD)


MILE = UnitDef("mile", "mi", Decimal("1_609.344"), LENGTH)


def Mile(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in miles.

    Parameters
    ----------
    value : Numeric
        Length magnitude in miles.

    Returns
    -------
    Length
        Length represented in miles.

    Examples
    --------
    A 5-mile training run can be compared directly with metric distances:

    >>> morning_run = Mile(5)
    >>> race_distance = Kilometre(8)
    >>> sorted([morning_run, race_distance])
    [8 km, 5 mi]

    """
    return Length(to_exact(value) * MILE.scale, MILE)


NAUTICAL_MILE = UnitDef("nautical_mile", "M", 1_852, LENGTH, aliases=("nmi",))


def NauticalMile(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in nautical miles.

    Parameters
    ----------
    value : Numeric
        Length magnitude in nautical miles.

    Returns
    -------
    Length
        Length represented in nautical miles.

    Notes
    -----
    One nautical mile is defined as exactly 1852 metres.

    Examples
    --------
    A ship travelling 120 nautical miles covers exactly 222.24 km:

    >>> voyage = NauticalMile(120)
    >>> equivalent = Kilometre(222.24)
    >>> voyage == equivalent
    True

    """
    return Length(to_exact(value) * NAUTICAL_MILE.scale, NAUTICAL_MILE)


# Astronomy and space.

ASTRONOMICAL_UNIT = UnitDef(
    "astronomical_unit",
    "au",
    Decimal(149597870700),
    LENGTH,
    aliases=("AU", "ua"),
)
LIGHT_YEAR = UnitDef(
    "light_year",
    "ly",
    Decimal(9460730472580800),
    LENGTH,
    aliases=("lyr", "l.y."),
    words=("light-year", "lightyear"),
)
PARSEC = UnitDef(
    "parsec",
    "pc",
    Fraction(648000) * ASTRONOMICAL_UNIT.scale / PI,
    LENGTH,
    words=("parsec",),
)
"""The parsec: exactly 648000/pi astronomical units, with pi to 100 decimal places."""
KILOPARSEC = with_prefix(prefixes.KILO, PARSEC)
MEGAPARSEC = with_prefix(prefixes.MEGA, PARSEC)
GIGAPARSEC = with_prefix(prefixes.GIGA, PARSEC)


def AstronomicalUnit(value: Numeric) -> Length:
    """Construct a Length from a magnitude expressed in astronomical units.

    Parameters
    ----------
    value : Numeric
        Length magnitude in astronomical units.

    Returns
    -------
    Length
        Length represented in astronomical units.

    Examples
    --------
    The astronomical unit is useful for expressing distances within the Solar System:

    >>> earth_sun_distance = AstronomicalUnit(1)
    >>> earth_sun_distance.to(KILOMETRE) == Kilometre(Decimal("149597870.7"))
    True

    """
    return Length(to_exact(value) * ASTRONOMICAL_UNIT.scale, ASTRONOMICAL_UNIT)


def LightYear(value: Numeric) -> Length:
    """Construct a Length from a magnitude expressed in light-years.

    Parameters
    ----------
    value : Numeric
        Length magnitude in light-years.

    Returns
    -------
    Length
        Length represented in light-years.

    Examples
    --------
    A light-year is the distance travelled by light during one Julian year.
    Its exact SI conversion is:

    >>> distance = LightYear(1)
    >>> distance.to(KILOMETRE)
    9460730472580.8 km

    """
    return Length(to_exact(value) * LIGHT_YEAR.scale, LIGHT_YEAR)


def Parsec(value: Numeric) -> Length:
    """Construct a Length from a magnitude expressed in parsecs.

    Parameters
    ----------
    value : Numeric
        Length magnitude in parsecs.

    Returns
    -------
    Length
        Length represented in parsecs.

    Notes
    -----
    A parsec is exactly 648000/pi astronomical units.
    kuchka holds pi to 100 decimal places, so a parsec is within one part in 1E+100 of
    that length, and the kiloparsec, megaparsec, and gigaparsec are exact multiples of
    it.

    Examples
    --------
    A parsec is about 3.26 light-years:

    >>> from kuchka.units.length import LIGHT_YEAR
    >>> Parsec(1).to(LIGHT_YEAR)
    3.261563777167433562138639707 ly

    A parsec is the distance at which an astronomical unit subtends one arcsecond:

    >>> from kuchka.units.angular import RADIAN, ArcSecond
    >>> Parsec(1).value_in(ASTRONOMICAL_UNIT) * ArcSecond(1).value_in(RADIAN) == 1
    True

    """
    return Length(to_exact(value) * PARSEC.scale, PARSEC)


def Kiloparsec(value: Numeric) -> Length:
    """Construct a Length from a magnitude expressed in kiloparsecs.

    Parameters
    ----------
    value : Numeric
        Length magnitude in kiloparsecs.

    Returns
    -------
    Length
        Length represented in kiloparsecs.

    """
    return Length(to_exact(value) * KILOPARSEC.scale, KILOPARSEC)


def Megaparsec(value: Numeric) -> Length:
    """Construct a Length from a magnitude expressed in megaparsecs.

    Parameters
    ----------
    value : Numeric
        Length magnitude in megaparsecs.

    Returns
    -------
    Length
        Length represented in megaparsecs.

    Examples
    --------
    The Andromeda galaxy is about 0.78 Mpc away:

    >>> Megaparsec(0.78).to(KILOPARSEC)
    780 kpc

    """
    return Length(to_exact(value) * MEGAPARSEC.scale, MEGAPARSEC)


def Gigaparsec(value: Numeric) -> Length:
    """Construct a Length from a magnitude expressed in gigaparsecs.

    Parameters
    ----------
    value : Numeric
        Length magnitude in gigaparsecs.

    Returns
    -------
    Length
        Length represented in gigaparsecs.

    """
    return Length(to_exact(value) * GIGAPARSEC.scale, GIGAPARSEC)


LENGTH_UNITS: Mapping[str, Callable[[Numeric], Length]] = unit_table(
    "LENGTH_UNITS",
    {
        PICOMETRE: Picometre,
        NANOMETRE: Nanometre,
        MICROMETRE: Micrometre,
        MILLIMETRE: Millimetre,
        CENTIMETRE: Centimetre,
        DECIMETRE: Decimetre,
        METRE: Metre,
        KILOMETRE: Kilometre,
        INCH: Inch,
        FOOT: Foot,
        YARD: Yard,
        MILE: Mile,
        NAUTICAL_MILE: NauticalMile,
        ASTRONOMICAL_UNIT: AstronomicalUnit,
        LIGHT_YEAR: LightYear,
        PARSEC: Parsec,
        KILOPARSEC: Kiloparsec,
        MEGAPARSEC: Megaparsec,
        GIGAPARSEC: Gigaparsec,
    },
)

__all__ = [
    "ASTRONOMICAL_UNIT",
    "CENTIMETER",
    "CENTIMETRE",
    "DECIMETER",
    "DECIMETRE",
    "FOOT",
    "GIGAPARSEC",
    "INCH",
    "KILOMETER",
    "KILOMETRE",
    "KILOPARSEC",
    "LENGTH_UNITS",
    "LIGHT_YEAR",
    "MEGAPARSEC",
    "METER",
    "METRE",
    "MICROMETER",
    "MICROMETRE",
    "MILE",
    "MILLIMETER",
    "MILLIMETRE",
    "NANOMETER",
    "NANOMETRE",
    "NAUTICAL_MILE",
    "PARSEC",
    "PICOMETER",
    "PICOMETRE",
    "YARD",
    "AstronomicalUnit",
    "Centimeter",
    "Centimetre",
    "Decimeter",
    "Decimetre",
    "Foot",
    "Gigaparsec",
    "Inch",
    "Kilometer",
    "Kilometre",
    "Kiloparsec",
    "LightYear",
    "Megaparsec",
    "Meter",
    "Metre",
    "Micrometer",
    "Micrometre",
    "Mile",
    "Millimeter",
    "Millimetre",
    "Nanometer",
    "Nanometre",
    "NauticalMile",
    "Parsec",
    "Picometer",
    "Picometre",
    "Yard",
]
