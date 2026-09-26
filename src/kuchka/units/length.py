"""Length quantities and constructors for metric and selected exact imperial units.

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

Notes
-----
Metric prefixes represent exact powers of ten.

Imperial units implemented by this module are exact by definition, not measured
approximations. This means comparisons such as

>>> Inch(1) == Millimetre(25.4)
True

hold exactly.

`LENGTH_UNITS` maps symbols such as ``"mm"``, ``"km"``, and ``"in"`` to their
constructors for configuration files and other external interfaces.

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
from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import LENGTH
from kuchka.internal import prefixes
from kuchka.internal.prefixes import prefixed_unit
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Length
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

METRE_NAME = "metre"
METRE_SYMBOL = "m"

PICOMETRE = prefixed_unit(prefixes.PICO, METRE_NAME, METRE_SYMBOL, LENGTH)
NANOMETRE = prefixed_unit(prefixes.NANO, METRE_NAME, METRE_SYMBOL, LENGTH)
MICROMETRE = prefixed_unit(prefixes.MICRO, METRE_NAME, METRE_SYMBOL, LENGTH)
MILLIMETRE = prefixed_unit(prefixes.MILLI, METRE_NAME, METRE_SYMBOL, LENGTH)
CENTIMETRE = prefixed_unit(prefixes.CENTI, METRE_NAME, METRE_SYMBOL, LENGTH)
DECIMETRE = prefixed_unit(prefixes.DECI, METRE_NAME, METRE_SYMBOL, LENGTH)
METRE = prefixed_unit(prefixes.UNIT, METRE_NAME, METRE_SYMBOL, LENGTH)
KILOMETRE = prefixed_unit(prefixes.KILO, METRE_NAME, METRE_SYMBOL, LENGTH)

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

INCH = UnitDef("inch", "in", Decimal("0.0254"), LENGTH)


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


FOOT = UnitDef("foot", "ft", Decimal("0.3048"), LENGTH)


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


MILE = UnitDef("mile", "mi.", Decimal("1_609.344"), LENGTH)


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
    [8 km, 5 mi.]

    """
    return Length(to_exact(value) * MILE.scale, MILE)


NAUTICAL_MILE = UnitDef("nautical mile", "M", 1_852, LENGTH)


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


LENGTH_UNITS: Mapping[str, Callable[[Numeric], Length]] = MappingProxyType(
    {
        PICOMETRE.symbol: Picometre,
        NANOMETRE.symbol: Nanometre,
        MICROMETRE.symbol: Micrometre,
        MILLIMETRE.symbol: Millimetre,
        CENTIMETRE.symbol: Centimetre,
        DECIMETRE.symbol: Decimetre,
        METRE.symbol: Metre,
        KILOMETRE.symbol: Kilometre,
        INCH.symbol: Inch,
        FOOT.symbol: Foot,
        YARD.symbol: Yard,
        MILE.symbol: Mile,
        NAUTICAL_MILE.symbol: NauticalMile,
    }
)

__all__ = [
    "CENTIMETER",
    "CENTIMETRE",
    "DECIMETER",
    "DECIMETRE",
    "FOOT",
    "INCH",
    "KILOMETER",
    "KILOMETRE",
    "LENGTH_UNITS",
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
    "PICOMETER",
    "PICOMETRE",
    "YARD",
    "Centimeter",
    "Centimetre",
    "Decimeter",
    "Decimetre",
    "Foot",
    "Inch",
    "Kilometer",
    "Kilometre",
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
    "Picometer",
    "Picometre",
    "Yard",
]
