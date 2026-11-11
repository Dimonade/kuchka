"""Pressure constructors: pascals, bar, atmospheres, and pounds per square inch.

`Pressure` is force spread over an area, and the pascal (one newton per square metre)
is its canonical unit.
The module provides the pascal with its SI prefixes, the `Bar` and `Millibar`, the
standard `Atmosphere`, and the US customary `PoundPerSquareInch` and
`KilopoundPerSquareInch`:

>>> from kuchka import Bar
>>> from kuchka import Pascal
>>> from kuchka import PoundPerSquareInch
>>> tyre = Bar(2.2)
>>> tank_rating = PoundPerSquareInch(3000)

Everyday pressures cover ten orders of magnitude, and each part of the range has its
own habitual unit.
The air around us sits at hectopascals and kilopascals, tyres and gas cylinders are
read in bar or psi, hydraulic systems and structural steel work in megapascals, and
the interior of a planet is quoted in gigapascals.

Examples
--------
A diver's gauge reads the pressure above the surrounding atmosphere.
Ten metres of seawater (about 1025 kg per cubic metre, so a column of 10 250 kg above
each square metre) add about one bar, and the pressure on the diver is that column plus
the atmosphere above it:

>>> from kuchka import Atmosphere
>>> from kuchka import Kilogram
>>> from kuchka import MetrePerSecondSquared
>>> from kuchka import SquareMetre
>>> from kuchka.units import BAR
>>> gravity = MetrePerSecondSquared(9.80665)
>>> column = Kilogram(10_250) * gravity / SquareMetre(1)
>>> f"{column.to(BAR):.2f}"
'1.01 bar'
>>> f"{(Atmosphere(1) + column).to(BAR):.2f}"
'2.02 bar'

A pressure over a day is a difference of two pressures, and it stays a `Pressure`.
A front lowers the sea-level pressure from 1013.25 hPa to 990 hPa:

>>> from kuchka import Hectopascal
>>> from kuchka.units import KILOPASCAL
>>> fall = Hectopascal(1013.25) - Hectopascal(990)
>>> fall
23.25 hPa
>>> fall.to(KILOPASCAL)
2.325 kPa

A pressure is a different quantity from a force, so the two refuse to mix, and the
relation between them is the area:

>>> from kuchka import Newton
>>> Pascal(1) + Newton(1)  # doctest: +ELLIPSIS
Traceback (most recent call last):
...
kuchka.errors.IncompatibleDimensionError: ...

Notes
-----
A pressure value carries no reference.
A gauge reading (relative to the surrounding atmosphere) and an absolute reading are
both `Pressure`, and adding the atmosphere to a gauge reading gives the absolute one,
as the diver's example shows.

The pascal is defined as one newton per square metre.
`Bar` is exactly 100 000 Pa, `Millibar` exactly 100 Pa, and the standard `Atmosphere`
exactly 101 325 Pa.
`PoundPerSquareInch` is a pound-force on a square inch, so its scale follows from the
exact scales of both and is exact (6894.757293168... Pa).
`KilopoundPerSquareInch` is a thousand of those.

`Millibar` and `Hectopascal` share the scale 100 Pa.
They are two naming traditions, meteorological and SI-prefixed, that agree numerically.

`Gigapascal` and `KilopoundPerSquareInch` (`GPa`, `ksi`) are the units that the
strength and stiffness of materials are quoted in.
They serve `Stress` as well, which reads every unit of this module, and
`Pressure.to_stress()` takes a pressure reading as a stress.

`PRESSURE_UNITS` maps each symbol to its constructor, for boundary code that reads a
unit as a string from outside the application.

References
----------
NIST, Guide for the Use of the International System of Units, Appendix B.8, factors
for units listed alphabetically:
https://www.nist.gov/node/777676

BIPM, The International System of Units (SI Brochure):
https://www.bipm.org/en/publications/si-brochure

See Also
--------
~kuchka.quantities.Stress
    Internal force per area in a loaded solid, which reads the same units.
~kuchka.quantities.Force
    Pressure times area is a force.
~kuchka.quantities.Area
    The surface a pressure acts over.
~kuchka.quantities.Energy
    Pressure times volume is energy, as in the work of a gas against a constant
    pressure.

"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from kuchka.dimensions import PRESSURE
from kuchka.internal import prefixes
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Pressure
from kuchka.quantities import UnitDef
from kuchka.units.geometry.area import SQUARE_INCH
from kuchka.units.mechanics.force import POUND_FORCE

if TYPE_CHECKING:
    from kuchka.internal.unit_table import UnitTable

PASCAL_NAME = "pascal"
PASCAL_SYMBOL = "Pa"

PASCAL = prefixed_unit(prefixes.UNIT, PASCAL_NAME, PASCAL_SYMBOL, PRESSURE)
HECTOPASCAL = prefixed_unit(prefixes.HECTO, PASCAL_NAME, PASCAL_SYMBOL, PRESSURE)
KILOPASCAL = prefixed_unit(prefixes.KILO, PASCAL_NAME, PASCAL_SYMBOL, PRESSURE)
MEGAPASCAL = prefixed_unit(prefixes.MEGA, PASCAL_NAME, PASCAL_SYMBOL, PRESSURE)
GIGAPASCAL = prefixed_unit(prefixes.GIGA, PASCAL_NAME, PASCAL_SYMBOL, PRESSURE)

Pressure._canonical_unit = PASCAL  # noqa: SLF001 -- this module owns Pressure's canonical unit


def Pascal(value: Numeric) -> Pressure:
    """Construct a Pressure from a magnitude expressed in pascals.

    Parameters
    ----------
    value : Numeric
        Pressure magnitude in pascals.

    Returns
    -------
    Pressure
        Pressure represented in pascals.

    Examples
    --------
    The standard atmosphere is exactly 101 325 Pa:

    >>> standard = Pascal(101_325)
    >>> standard
    101325 Pa
    >>> from kuchka import Atmosphere
    >>> standard == Atmosphere(1)
    True

    The weight of 80 g/m² office paper, spread over one square metre of sheet, presses
    with under one pascal:

    >>> from kuchka import Gram
    >>> from kuchka import MetrePerSecondSquared
    >>> from kuchka import SquareMetre
    >>> weight = Gram(80) * MetrePerSecondSquared(9.80665)
    >>> f"{weight / SquareMetre(1):.2f}"
    '0.78 Pa'

    A pressure that arrives as text enters through `parse`:

    >>> from kuchka import Pressure
    >>> from kuchka import parse
    >>> parse("101325 Pa", Pressure) == standard
    True

    """
    return Pressure(to_exact(value) * PASCAL.scale, PASCAL)


def Hectopascal(value: Numeric) -> Pressure:
    """Construct a Pressure from a magnitude expressed in hectopascals.

    Parameters
    ----------
    value : Numeric
        Pressure magnitude in hectopascals.

    Returns
    -------
    Pressure
        Pressure represented in hectopascals.

    Examples
    --------
    A weather station reports the sea-level pressure in hectopascals:

    >>> station = Hectopascal(1013.25)
    >>> station
    1013.25 hPa

    That reading is the standard atmosphere, exactly:

    >>> from kuchka import Atmosphere
    >>> station == Atmosphere(1)
    True

    """
    return Pressure(to_exact(value) * HECTOPASCAL.scale, HECTOPASCAL)


def Kilopascal(value: Numeric) -> Pressure:
    """Construct a Pressure from a magnitude expressed in kilopascals.

    Parameters
    ----------
    value : Numeric
        Pressure magnitude in kilopascals.

    Returns
    -------
    Pressure
        Pressure represented in kilopascals.

    Examples
    --------
    The air pressure at 1000 m above sea level is about 90 kPa:

    >>> highland = Kilopascal(90)
    >>> highland
    90 kPa

    A gas that expands by 2 L against a constant pressure of 100 kPa does work equal to
    pressure times volume:

    >>> from kuchka import Litre
    >>> Kilopascal(100) * Litre(2)
    200 J

    """
    return Pressure(to_exact(value) * KILOPASCAL.scale, KILOPASCAL)


def Megapascal(value: Numeric) -> Pressure:
    """Construct a Pressure from a magnitude expressed in megapascals.

    Parameters
    ----------
    value : Numeric
        Pressure magnitude in megapascals.

    Returns
    -------
    Pressure
        Pressure represented in megapascals.

    Examples
    --------
    A hydraulic circuit is commonly set to 20 MPa:

    >>> line = Megapascal(20)
    >>> line
    20 MPa

    Acting on a 50 cm² piston, that pressure pushes with a force of 100 kN:

    >>> from kuchka import SquareCentimetre
    >>> from kuchka.units import KILONEWTON
    >>> (line * SquareCentimetre(50)).to(KILONEWTON)
    100 kN

    A gauge on the same line is graduated in bar:

    >>> from kuchka.units import BAR
    >>> line.to(BAR)
    200 bar

    """
    return Pressure(to_exact(value) * MEGAPASCAL.scale, MEGAPASCAL)


def Gigapascal(value: Numeric) -> Pressure:
    """Construct a Pressure from a magnitude expressed in gigapascals.

    Parameters
    ----------
    value : Numeric
        Pressure magnitude in gigapascals.

    Returns
    -------
    Pressure
        Pressure represented in gigapascals.

    Examples
    --------
    The pressure at the centre of the Earth is about 360 GPa:

    >>> core = Gigapascal(360)
    >>> core
    360 GPa

    In atmospheres, that is a few million:

    >>> from kuchka.units import ATMOSPHERE
    >>> f"{core.to(ATMOSPHERE):.3e}"
    '3.553e+6 atm'

    """
    return Pressure(to_exact(value) * GIGAPASCAL.scale, GIGAPASCAL)


# Non-SI units.

BAR = UnitDef("bar", "bar", Decimal(100_000), PRESSURE)
MILLIBAR = UnitDef("millibar", "mbar", Decimal(100), PRESSURE)
ATMOSPHERE = UnitDef("atmosphere", "atm", Decimal(101_325), PRESSURE)
POUND_PER_SQUARE_INCH = UnitDef(
    "pound_per_square_inch",
    "psi",
    POUND_FORCE.scale / SQUARE_INCH.scale,
    PRESSURE,
)
KILOPOUND_PER_SQUARE_INCH = UnitDef(
    "kilopound_per_square_inch",
    "ksi",
    1000 * POUND_PER_SQUARE_INCH.scale,
    PRESSURE,
)


def Bar(value: Numeric) -> Pressure:
    """Construct a Pressure from a magnitude expressed in bar.

    Parameters
    ----------
    value : Numeric
        Pressure magnitude in bar.

    Returns
    -------
    Pressure
        Pressure represented in bar.

    Notes
    -----
    Exact: a bar is defined as precisely 100 000 Pa.

    Examples
    --------
    A passenger car's tyres are inflated to about 2.2 bar, which a tyre gauge also
    shows in psi:

    >>> tyre = Bar(2.2)
    >>> from kuchka.units import POUND_PER_SQUARE_INCH
    >>> f"{tyre.to(POUND_PER_SQUARE_INCH):.1f}"
    '31.9 psi'

    The bar is a decimal multiple of the pascal:

    >>> from kuchka import Pascal
    >>> Bar(1) == Pascal(100_000)
    True

    """
    return Pressure(to_exact(value) * BAR.scale, BAR)


def Millibar(value: Numeric) -> Pressure:
    """Construct a Pressure from a magnitude expressed in millibar.

    Parameters
    ----------
    value : Numeric
        Pressure magnitude in millibar.

    Returns
    -------
    Pressure
        Pressure represented in millibar.

    Notes
    -----
    Exact: a millibar is defined as precisely 100 Pa, the scale of the hectopascal.

    Examples
    --------
    The central pressure of a deep tropical cyclone is about 900 mbar:

    >>> storm = Millibar(900)
    >>> storm
    900 mbar

    A weather map that moves from millibar to hectopascal changes the label and keeps
    every value, because the two units are the same size:

    >>> from kuchka import Hectopascal
    >>> from kuchka.units import HECTOPASCAL
    >>> storm.to(HECTOPASCAL)
    900 hPa
    >>> Millibar(1013.25) == Hectopascal(1013.25)
    True

    """
    return Pressure(to_exact(value) * MILLIBAR.scale, MILLIBAR)


def Atmosphere(value: Numeric) -> Pressure:
    """Construct a Pressure from a magnitude expressed in standard atmospheres.

    Parameters
    ----------
    value : Numeric
        Pressure magnitude in standard atmospheres.

    Returns
    -------
    Pressure
        Pressure represented in standard atmospheres.

    Notes
    -----
    Exact: the standard atmosphere is defined as precisely 101 325 Pa.

    Examples
    --------
    Air pressure near the summit of Mount Everest is about a third of the sea-level
    value:

    >>> summit = Atmosphere(0.33)
    >>> from kuchka.units import KILOPASCAL
    >>> f"{summit.to(KILOPASCAL):.1f}"
    '33.4 kPa'

    One atmosphere in the units of a tyre gauge and of the SI:

    >>> from kuchka.units import PASCAL
    >>> from kuchka.units import POUND_PER_SQUARE_INCH
    >>> Atmosphere(1).to(PASCAL)
    101325 Pa
    >>> f"{Atmosphere(1).to(POUND_PER_SQUARE_INCH):.2f}"
    '14.70 psi'

    """
    return Pressure(to_exact(value) * ATMOSPHERE.scale, ATMOSPHERE)


def PoundPerSquareInch(value: Numeric) -> Pressure:
    """Construct a Pressure from a magnitude expressed in pounds per square inch.

    Parameters
    ----------
    value : Numeric
        Pressure magnitude in pounds per square inch.

    Returns
    -------
    Pressure
        Pressure represented in pounds per square inch.

    Notes
    -----
    Exact: a pound-force acting on a square inch, from the exact scales of both.

    Examples
    --------
    A scuba cylinder is rated for 3000 psi.
    Filling it at a dive shop to 200 bar stays inside the rating, since the rating is
    about 207 bar:

    >>> from kuchka import Bar
    >>> from kuchka.units import BAR
    >>> rating = PoundPerSquareInch(3000)
    >>> f"{rating.to(BAR):.0f}"
    '207 bar'
    >>> Bar(200) < rating
    True

    The unit is also read from text, as an instrument or a datasheet writes it:

    >>> from kuchka import Pressure
    >>> from kuchka import parse
    >>> parse("14.7 psi", Pressure)
    14.7 psi

    """
    return Pressure(
        to_exact(value) * POUND_PER_SQUARE_INCH.scale,
        POUND_PER_SQUARE_INCH,
    )


def KilopoundPerSquareInch(value: Numeric) -> Pressure:
    """Construct a Pressure from a magnitude expressed in kilopounds per square inch.

    Parameters
    ----------
    value : Numeric
        Pressure magnitude in kilopounds per square inch.

    Returns
    -------
    Pressure
        Pressure represented in kilopounds per square inch.

    Notes
    -----
    Exact: a thousand times `POUND_PER_SQUARE_INCH`.

    Examples
    --------
    Structural steel of grade A36 has a minimum yield strength of 36 ksi, which metric
    specifications round to 250 MPa:

    >>> yield_strength = KilopoundPerSquareInch(36)
    >>> from kuchka.units import MEGAPASCAL
    >>> f"{yield_strength.to(MEGAPASCAL):.0f}"
    '248 MPa'

    A strength is a stress in a loaded solid, and the pressure reading becomes one
    explicitly:

    >>> yield_strength.to_stress()
    36 ksi

    The kilopound is a decimal multiple of the pound:

    >>> from kuchka import PoundPerSquareInch
    >>> KilopoundPerSquareInch(1) == PoundPerSquareInch(1000)
    True

    """
    return Pressure(
        to_exact(value) * KILOPOUND_PER_SQUARE_INCH.scale,
        KILOPOUND_PER_SQUARE_INCH,
    )


PRESSURE_UNITS: UnitTable[Pressure] = unit_table(
    "PRESSURE_UNITS",
    {
        PASCAL: Pascal,
        HECTOPASCAL: Hectopascal,
        KILOPASCAL: Kilopascal,
        MEGAPASCAL: Megapascal,
        GIGAPASCAL: Gigapascal,
        BAR: Bar,
        MILLIBAR: Millibar,
        ATMOSPHERE: Atmosphere,
        POUND_PER_SQUARE_INCH: PoundPerSquareInch,
        KILOPOUND_PER_SQUARE_INCH: KilopoundPerSquareInch,
    },
)

__all__ = [
    "ATMOSPHERE",
    "BAR",
    "GIGAPASCAL",
    "HECTOPASCAL",
    "KILOPASCAL",
    "KILOPOUND_PER_SQUARE_INCH",
    "MEGAPASCAL",
    "MILLIBAR",
    "PASCAL",
    "POUND_PER_SQUARE_INCH",
    "PRESSURE_UNITS",
    "Atmosphere",
    "Bar",
    "Gigapascal",
    "Hectopascal",
    "Kilopascal",
    "KilopoundPerSquareInch",
    "Megapascal",
    "Millibar",
    "Pascal",
    "PoundPerSquareInch",
]
