"""Length constructors: from picometres to gigaparsecs.

`Length` represents one-dimensional distance. The metre is the canonical SI base unit,
while the constructors in this module provide convenient entry points from metric
prefixes and a small set of exact non-SI units.

`Metre` is the canonical spelling adopted by the BIPM.
American spellings (`Meter`, `Millimeter`, `Kilometer`, ...) are aliases of the same
objects, and both spellings display using the same SI symbols.

Every imperial unit implemented here is an exact decimal multiple of the metre.
Since the 1959 international yard and pound agreement, conversions such as
`1 in = 25.4 mm` and `1 ft = 0.3048 m` are exact, so they preserve the same `Decimal`
precision guarantees as SI prefixes.

The astronomical unit and light-year extend the same `Length` quantity to astronomical
scales. The astronomical unit (`au`) is an exact conventional length, while the
light-year (`ly`) is the exact distance light travels in a Julian year.
The parsec (`pc`) is defined as exactly 648000/pi astronomical units, the distance at
which one astronomical unit subtends one arcsecond.
Pi is irrational, so `kuchka` holds a parsec as that quotient with pi to 100 decimal
places, the same pi `Radian` uses: the parsec is within one part in 1E+100 of its
defined length, and the parsecs, kiloparsecs, and megaparsecs among themselves stay
exact.

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

Visible light has wavelengths of hundreds of nanometres:

>>> green_laser = Nanometre(532)

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

Imperial units implemented by this module are exact by definition, so comparisons
such as

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

References
----------
BIPM, The International System of Units (SI Brochure), on the metre and the units
accepted for use with the SI:
https://www.bipm.org/en/publications/si-brochure

IAU 2015 Resolution B2, which defines the parsec and fixes the astronomical unit:
https://arxiv.org/abs/1510.06262

NIST, Guide for the Use of the International System of Units, Appendix B.8, factors
for units listed alphabetically:
https://www.nist.gov/node/777676

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
    A typical covalent bond between two carbon atoms is about 154 pm long:

    >>> carbon_bond = Picometre(154)
    >>> carbon_bond
    154 pm

    Structural biology quotes the same length in nanometres:

    >>> from kuchka.units import NANOMETRE
    >>> carbon_bond.to(NANOMETRE)
    0.154 nm

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
    A green laser pointer emits light with a wavelength of about 532 nm:

    >>> wavelength = Nanometre(532)
    >>> wavelength
    532 nm

    Light travels at the speed of light, so dividing it by the wavelength gives the
    frequency, about 563 THz:

    >>> from kuchka.constants.codata_2022 import SPEED_OF_LIGHT_IN_VACUUM
    >>> from kuchka.units import TERAHERTZ
    >>> f"{(SPEED_OF_LIGHT_IN_VACUUM / wavelength).to(TERAHERTZ):.1f}"
    '563.5 THz'

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
    >>> hair
    70 µm

    A red blood cell is about 7 µm across, so ten of them in a row span a hair:

    >>> red_blood_cell = Micrometre(7)
    >>> round((hair / red_blood_cell).magnitude)
    10

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
    >>> shaft
    12 mm
    >>> bore = Millimetre(12.2)
    >>> clearance = bore - shaft
    >>> clearance
    0.2 mm

    A clearance that arrives as text, as a drawing or a spreadsheet writes it, enters
    through `parse`:

    >>> from kuchka import Length
    >>> from kuchka import parse
    >>> parse("0.2 mm", Length) == clearance
    True

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
    >>> postcard_width
    15 cm

    The same width on an inch ruler is a little under six inches:

    >>> from kuchka.units import INCH
    >>> f"{postcard_width.to(INCH):.2f}"
    '5.91 in'

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
    A 6 dm drafting ruler is exactly 60 cm long:

    >>> drafting_ruler = Decimetre(6)
    >>> drafting_ruler
    6 dm
    >>> from kuchka import Centimetre
    >>> drafting_ruler == Centimetre(60)
    True

    A cube 1 dm on a side holds one litre, which is where the litre comes from:

    >>> from kuchka import Litre
    >>> Decimetre(1) * Decimetre(1) * Decimetre(1) == Litre(1)
    True

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
    The world-class high jump bar height is around two and a half metres:

    >>> high_jump_bar = Metre(2.45)
    >>> high_jump_bar
    2.45 m

    A 100 m sprint in 9.58 s is an average speed of about 37.6 km/h:

    >>> from kuchka import Second
    >>> from kuchka.units import KILOMETRE_PER_HOUR
    >>> sprint = Metre(100) / Second(9.58)
    >>> f"{sprint.to(KILOMETRE_PER_HOUR):.1f}"
    '37.6 km/h'

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
    >>> marathon
    42.195 km

    The same race in the miles that road signs show in the United States:

    >>> from kuchka.units import MILE
    >>> f"{marathon.to(MILE):.3f}"
    '26.219 mi'

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
    A laptop screen is sold by its diagonal of 14 in:

    >>> screen = Inch(14)
    >>> screen
    14 in
    >>> from kuchka.units import CENTIMETRE
    >>> screen.to(CENTIMETRE)
    35.56 cm

    The conversion factor to the millimetre is exact:

    >>> from kuchka import Millimetre
    >>> Inch(1) == Millimetre(25.4)
    True

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
    >>> hoop_height
    10 ft
    >>> from kuchka.units import METRE
    >>> hoop_height.to(METRE)
    3.048 m

    Aviation quotes cruising altitudes in feet, and flight level 350 is 35 000 ft:

    >>> from kuchka.units import KILOMETRE
    >>> Foot(35_000).to(KILOMETRE)
    10.668 km

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
    An American football field is 100 yd between the goal lines:

    >>> field = Yard(100)
    >>> field
    100 yd
    >>> from kuchka.units import METRE
    >>> field.to(METRE)
    91.44 m

    The field is 160 ft wide, which is 53 and 1/3 yd, and an exact fraction keeps it so:

    >>> from fractions import Fraction
    >>> from kuchka import Foot
    >>> Yard(Fraction(160, 3)) == Foot(160)
    True

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
    >>> morning_run
    5 mi
    >>> from kuchka import Kilometre
    >>> race_distance = Kilometre(8)
    >>> sorted([morning_run, race_distance])
    [8 km, 5 mi]

    The mile is an exact length in kilometres:

    >>> from kuchka.units import KILOMETRE
    >>> Mile(1).to(KILOMETRE)
    1.609344 km

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
    >>> voyage
    120 M
    >>> from kuchka import Kilometre
    >>> voyage == Kilometre(222.24)
    True

    A knot is a nautical mile per hour:

    >>> from kuchka import Hour
    >>> from kuchka.units import KNOT
    >>> (NauticalMile(1) / Hour(1)).to(KNOT)
    1 kn

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
    >>> earth_sun_distance
    1 au
    >>> from kuchka.units import KILOMETRE
    >>> earth_sun_distance.to(KILOMETRE)
    149597870.7 km

    Sunlight reaches the Earth after the distance divided by the speed of light, about
    eight minutes and twenty seconds:

    >>> from kuchka.constants.codata_2022 import SPEED_OF_LIGHT_IN_VACUUM
    >>> from kuchka.units import MINUTE
    >>> f"{(earth_sun_distance / SPEED_OF_LIGHT_IN_VACUUM).to(MINUTE):.2f}"
    '8.32 min'

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
    Proxima Centauri, the nearest star beyond the Sun, is about 4.25 ly away:

    >>> from decimal import Decimal
    >>> nearest_star = LightYear(Decimal("4.25"))
    >>> nearest_star
    4.25 ly

    A light-year is the distance light travels in one Julian year, and its exact SI
    conversion is:

    >>> from kuchka.units import KILOMETRE
    >>> LightYear(1).to(KILOMETRE)
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
    The distance between neighbouring stars in the Galactic disc is of the order of a
    parsec:

    >>> separation = Parsec(1)
    >>> separation
    1 pc

    A parsec is about 3.26 light-years:

    >>> from kuchka.units import LIGHT_YEAR
    >>> f"{separation.to(LIGHT_YEAR):.2f}"
    '3.26 ly'

    A parsec is the distance at which an astronomical unit subtends one arcsecond:

    >>> from kuchka.units import ASTRONOMICAL_UNIT
    >>> from kuchka.units import RADIAN
    >>> from kuchka.units import ArcSecond
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

    Examples
    --------
    The Sun lies about 8.2 kpc from the centre of the Milky Way:

    >>> galactic_centre = Kiloparsec(8.2)
    >>> galactic_centre
    8.2 kpc

    That is about twenty-seven thousand light-years:

    >>> from kuchka.units import LIGHT_YEAR
    >>> f"{galactic_centre.to(LIGHT_YEAR):.3e}"
    '2.674e+4 ly'

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

    >>> andromeda = Megaparsec(0.78)
    >>> andromeda
    0.78 Mpc
    >>> from kuchka.units import KILOPARSEC
    >>> andromeda.to(KILOPARSEC)
    780 kpc

    Galaxy catalogues list distances in this unit, and `parse` reads one as text:

    >>> from kuchka import Length
    >>> from kuchka import parse
    >>> parse("0.78 Mpc", Length) == andromeda
    True

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

    Examples
    --------
    The radius of the observable universe is about 14.2 Gpc in comoving distance:

    >>> observable_universe = Gigaparsec(14.2)
    >>> observable_universe
    14.2 Gpc

    In light-years, that is about 46 billion:

    >>> from kuchka.units import LIGHT_YEAR
    >>> f"{observable_universe.to(LIGHT_YEAR):.2e}"
    '4.63e+10 ly'

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

LENGTH_LADDERS: tuple[tuple[UnitDef, ...], ...] = (
    (
        PICOMETRE,
        NANOMETRE,
        MICROMETRE,
        MILLIMETRE,
        METRE,
        KILOMETRE,
    ),
    (
        PARSEC,
        KILOPARSEC,
        MEGAPARSEC,
        GIGAPARSEC,
    ),
)
"""The runs of units `auto_scale` moves a length along.

There is one run for each family of prefixed units, smallest first.
"""

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
    "LENGTH_LADDERS",
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
