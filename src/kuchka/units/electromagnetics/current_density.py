"""Unit constructors for current density: amperes per area and its multiples.

    from kuchka import AmperePerSquareMillimetre, MilliamperePerSquareCentimetre

    wire = AmperePerSquareMillimetre(4)
    electrode = MilliamperePerSquareCentimetre(10)

`CurrentDensity` is electric current through an area, `Current / Area`.
Its canonical unit is the ampere per square metre (`A/m²`).
The ampere per square millimetre is how the load of a conductor is rated, and the
milliampere per square centimetre is how an electrode is driven.

Examples
--------
A 4 A/mm² conductor of 2.5 mm² carries 10 A:

>>> from kuchka import SquareMillimetre
>>> AmperePerSquareMillimetre(4) * SquareMillimetre(2.5)
10 A

An electrode driven at 10 mA/cm² is driven at 100 A/m²:

>>> MilliamperePerSquareCentimetre(10).to(AMPERE_PER_SQUARE_METRE)
100 A/m²

`CURRENT_DENSITY_UNITS` maps symbols such as ``"A/m2"`` and ``"mA/cm2"`` to their
constructors, for boundary code that reads a unit as a string from outside the
application.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import CURRENT_DENSITY
from kuchka.internal import prefixes
from kuchka.internal.prefixes import with_prefix
from kuchka.internal.spelling import powered
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import CurrentDensity
from kuchka.quantities import UnitDef
from kuchka.units.current import AMPERE
from kuchka.units.geometry.area import SQUARE_CENTIMETRE
from kuchka.units.geometry.area import SQUARE_MILLIMETRE

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

AMPERE_PER_SQUARE_METRE = UnitDef(
    "ampere_per_square_metre",
    "A/m²",
    1,
    CURRENT_DENSITY,
    aliases=powered("A/m", 2),
    words=("amperes per square metre", "amperes per square meter"),
)
MILLIAMPERE_PER_SQUARE_METRE = with_prefix(prefixes.MILLI, AMPERE_PER_SQUARE_METRE)
KILOAMPERE_PER_SQUARE_METRE = with_prefix(prefixes.KILO, AMPERE_PER_SQUARE_METRE)
MEGAAMPERE_PER_SQUARE_METRE = with_prefix(prefixes.MEGA, AMPERE_PER_SQUARE_METRE)
AMPERE_PER_SQUARE_CENTIMETRE = UnitDef(
    "ampere_per_square_centimetre",
    "A/cm²",
    AMPERE.scale / SQUARE_CENTIMETRE.scale,
    CURRENT_DENSITY,
    aliases=powered("A/cm", 2),
    words=("amperes per square centimetre", "amperes per square centimeter"),
)
MILLIAMPERE_PER_SQUARE_CENTIMETRE = with_prefix(
    prefixes.MILLI, AMPERE_PER_SQUARE_CENTIMETRE
)
MICROAMPERE_PER_SQUARE_CENTIMETRE = with_prefix(
    prefixes.MICRO, AMPERE_PER_SQUARE_CENTIMETRE
)
AMPERE_PER_SQUARE_MILLIMETRE = UnitDef(
    "ampere_per_square_millimetre",
    "A/mm²",
    AMPERE.scale / SQUARE_MILLIMETRE.scale,
    CURRENT_DENSITY,
    aliases=powered("A/mm", 2),
    words=("amperes per square millimetre", "amperes per square millimeter"),
)

CurrentDensity._canonical_unit = AMPERE_PER_SQUARE_METRE  # noqa: SLF001 -- this module owns CurrentDensity's canonical unit


def AmperePerSquareMetre(value: Numeric) -> CurrentDensity:
    """Construct a CurrentDensity from amperes per square metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in amperes per square metre.

    Returns
    -------
    CurrentDensity
        CurrentDensity represented in amperes per square metre.

    """
    return CurrentDensity(
        to_exact(value) * AMPERE_PER_SQUARE_METRE.scale, AMPERE_PER_SQUARE_METRE
    )


def MilliamperePerSquareMetre(value: Numeric) -> CurrentDensity:
    """Construct a CurrentDensity from milliamperes per square metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in milliamperes per square metre.

    Returns
    -------
    CurrentDensity
        CurrentDensity represented in milliamperes per square metre.

    """
    return CurrentDensity(
        to_exact(value) * MILLIAMPERE_PER_SQUARE_METRE.scale,
        MILLIAMPERE_PER_SQUARE_METRE,
    )


def KiloamperePerSquareMetre(value: Numeric) -> CurrentDensity:
    """Construct a CurrentDensity from kiloamperes per square metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in kiloamperes per square metre.

    Returns
    -------
    CurrentDensity
        CurrentDensity represented in kiloamperes per square metre.

    """
    return CurrentDensity(
        to_exact(value) * KILOAMPERE_PER_SQUARE_METRE.scale, KILOAMPERE_PER_SQUARE_METRE
    )


def MegaamperePerSquareMetre(value: Numeric) -> CurrentDensity:
    """Construct a CurrentDensity from megaamperes per square metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in megaamperes per square metre.

    Returns
    -------
    CurrentDensity
        CurrentDensity represented in megaamperes per square metre.

    """
    return CurrentDensity(
        to_exact(value) * MEGAAMPERE_PER_SQUARE_METRE.scale, MEGAAMPERE_PER_SQUARE_METRE
    )


def AmperePerSquareCentimetre(value: Numeric) -> CurrentDensity:
    """Construct a CurrentDensity from amperes per square centimetre.

    Parameters
    ----------
    value : Numeric
        Magnitude in amperes per square centimetre.

    Returns
    -------
    CurrentDensity
        CurrentDensity represented in amperes per square centimetre.

    """
    return CurrentDensity(
        to_exact(value) * AMPERE_PER_SQUARE_CENTIMETRE.scale,
        AMPERE_PER_SQUARE_CENTIMETRE,
    )


def MilliamperePerSquareCentimetre(value: Numeric) -> CurrentDensity:
    """Construct a CurrentDensity from milliamperes per square centimetre.

    Parameters
    ----------
    value : Numeric
        Magnitude in milliamperes per square centimetre.

    Returns
    -------
    CurrentDensity
        CurrentDensity represented in milliamperes per square centimetre.

    """
    return CurrentDensity(
        to_exact(value) * MILLIAMPERE_PER_SQUARE_CENTIMETRE.scale,
        MILLIAMPERE_PER_SQUARE_CENTIMETRE,
    )


def MicroamperePerSquareCentimetre(value: Numeric) -> CurrentDensity:
    """Construct a CurrentDensity from microamperes per square centimetre.

    Parameters
    ----------
    value : Numeric
        Magnitude in microamperes per square centimetre.

    Returns
    -------
    CurrentDensity
        CurrentDensity represented in microamperes per square centimetre.

    """
    return CurrentDensity(
        to_exact(value) * MICROAMPERE_PER_SQUARE_CENTIMETRE.scale,
        MICROAMPERE_PER_SQUARE_CENTIMETRE,
    )


def AmperePerSquareMillimetre(value: Numeric) -> CurrentDensity:
    """Construct a CurrentDensity from amperes per square millimetre.

    Parameters
    ----------
    value : Numeric
        Magnitude in amperes per square millimetre.

    Returns
    -------
    CurrentDensity
        CurrentDensity represented in amperes per square millimetre.

    """
    return CurrentDensity(
        to_exact(value) * AMPERE_PER_SQUARE_MILLIMETRE.scale,
        AMPERE_PER_SQUARE_MILLIMETRE,
    )


CURRENT_DENSITY_UNITS: Mapping[str, Callable[[Numeric], CurrentDensity]] = unit_table(
    "CURRENT_DENSITY_UNITS",
    {
        AMPERE_PER_SQUARE_METRE: AmperePerSquareMetre,
        MILLIAMPERE_PER_SQUARE_METRE: MilliamperePerSquareMetre,
        KILOAMPERE_PER_SQUARE_METRE: KiloamperePerSquareMetre,
        MEGAAMPERE_PER_SQUARE_METRE: MegaamperePerSquareMetre,
        AMPERE_PER_SQUARE_CENTIMETRE: AmperePerSquareCentimetre,
        MILLIAMPERE_PER_SQUARE_CENTIMETRE: MilliamperePerSquareCentimetre,
        MICROAMPERE_PER_SQUARE_CENTIMETRE: MicroamperePerSquareCentimetre,
        AMPERE_PER_SQUARE_MILLIMETRE: AmperePerSquareMillimetre,
    },
)

__all__ = [
    "AMPERE_PER_SQUARE_CENTIMETRE",
    "AMPERE_PER_SQUARE_METRE",
    "AMPERE_PER_SQUARE_MILLIMETRE",
    "CURRENT_DENSITY_UNITS",
    "KILOAMPERE_PER_SQUARE_METRE",
    "MEGAAMPERE_PER_SQUARE_METRE",
    "MICROAMPERE_PER_SQUARE_CENTIMETRE",
    "MILLIAMPERE_PER_SQUARE_CENTIMETRE",
    "MILLIAMPERE_PER_SQUARE_METRE",
    "AmperePerSquareCentimetre",
    "AmperePerSquareMetre",
    "AmperePerSquareMillimetre",
    "KiloamperePerSquareMetre",
    "MegaamperePerSquareMetre",
    "MicroamperePerSquareCentimetre",
    "MilliamperePerSquareCentimetre",
    "MilliamperePerSquareMetre",
]
