"""Unit constructors for absorbed dose: grays and rads.

    from kuchka import Centigray, Gray, Milligray

    fraction = Gray(2)
    scan = Milligray(12)

`AbsorbedDose` is the energy a radiation field deposits in a mass of material.
Its SI unit is the gray (`Gy`), exactly one joule per kilogram.
The rad (`rad`) is the older CGS unit, defined exactly as a hundredth of a gray, so
`Centigray(1)` and `Rad(1)` are the same dose.
The module provides the gray from nano- through mega- multiples, and the rad and the
millirad.

These are units of energy deposited per mass: they say nothing of what the radiation
does to a person.
`EquivalentDose.from_absorbed_dose` weights a dose for that, and the sievert is its
unit.

The symbol `rad` is also the radian.
The two never meet: the unit tables of `AbsorbedDose` and `Angle` are separate, and
`parse` reads a text as the quantity type it is given.

Examples
--------
A radiotherapy fraction is commonly 2 Gy, which a record from an older system lists
as 200 rad:

>>> Gray(2).to(RAD)
200 rad

A dose of 25 kGy is a commonly used target for the radiation sterilisation of medical
devices:

>>> Kilogray(25).to(GRAY)
25000 Gy

`ABSORBED_DOSE_UNITS` maps symbols such as ``"Gy"``, ``"mGy"``, ``"cGy"``, ``"kGy"``,
and ``"rad"`` to their constructors for boundary code that reads unit labels from
external data.

"""

from __future__ import annotations

from fractions import Fraction
from typing import TYPE_CHECKING

from kuchka.dimensions import SPECIFIC_ENERGY
from kuchka.internal import prefixes
from kuchka.internal.prefixes import with_prefix
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import AbsorbedDose
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

GRAY = UnitDef("gray", "Gy", 1, SPECIFIC_ENERGY)
NANOGRAY = with_prefix(prefixes.NANO, GRAY)
MICROGRAY = with_prefix(prefixes.MICRO, GRAY)
MILLIGRAY = with_prefix(prefixes.MILLI, GRAY)
CENTIGRAY = with_prefix(prefixes.CENTI, GRAY)
KILOGRAY = with_prefix(prefixes.KILO, GRAY)
MEGAGRAY = with_prefix(prefixes.MEGA, GRAY)
RAD = UnitDef("rad", "rad", Fraction(1, 100), SPECIFIC_ENERGY)
MILLIRAD = with_prefix(prefixes.MILLI, RAD)

AbsorbedDose._canonical_unit = GRAY  # noqa: SLF001 -- this module owns AbsorbedDose's canonical unit


def Gray(value: Numeric) -> AbsorbedDose:
    """Construct an AbsorbedDose from a magnitude in grays.

    Parameters
    ----------
    value : Numeric
        Magnitude in grays.

    Returns
    -------
    AbsorbedDose
        AbsorbedDose represented in grays.

    Examples
    --------
    A radiotherapy fraction of 2 Gy, in centigrays:

    >>> Gray(2).to(CENTIGRAY)
    200 cGy

    """
    return AbsorbedDose(to_exact(value) * GRAY.scale, GRAY)


def Nanogray(value: Numeric) -> AbsorbedDose:
    """Construct an AbsorbedDose from a magnitude in nanograys.

    Parameters
    ----------
    value : Numeric
        Magnitude in nanograys.

    Returns
    -------
    AbsorbedDose
        AbsorbedDose represented in nanograys.

    """
    return AbsorbedDose(to_exact(value) * NANOGRAY.scale, NANOGRAY)


def Microgray(value: Numeric) -> AbsorbedDose:
    """Construct an AbsorbedDose from a magnitude in micrograys.

    Parameters
    ----------
    value : Numeric
        Magnitude in micrograys.

    Returns
    -------
    AbsorbedDose
        AbsorbedDose represented in micrograys.

    """
    return AbsorbedDose(to_exact(value) * MICROGRAY.scale, MICROGRAY)


def Milligray(value: Numeric) -> AbsorbedDose:
    """Construct an AbsorbedDose from a magnitude in milligrays.

    Parameters
    ----------
    value : Numeric
        Magnitude in milligrays.

    Returns
    -------
    AbsorbedDose
        AbsorbedDose represented in milligrays.

    """
    return AbsorbedDose(to_exact(value) * MILLIGRAY.scale, MILLIGRAY)


def Centigray(value: Numeric) -> AbsorbedDose:
    """Construct an AbsorbedDose from a magnitude in centigrays.

    Parameters
    ----------
    value : Numeric
        Magnitude in centigrays.

    Returns
    -------
    AbsorbedDose
        AbsorbedDose represented in centigrays.

    Examples
    --------
    A centigray is a rad:

    >>> Centigray(1) == Rad(1)
    True

    """
    return AbsorbedDose(to_exact(value) * CENTIGRAY.scale, CENTIGRAY)


def Kilogray(value: Numeric) -> AbsorbedDose:
    """Construct an AbsorbedDose from a magnitude in kilograys.

    Parameters
    ----------
    value : Numeric
        Magnitude in kilograys.

    Returns
    -------
    AbsorbedDose
        AbsorbedDose represented in kilograys.

    """
    return AbsorbedDose(to_exact(value) * KILOGRAY.scale, KILOGRAY)


def Megagray(value: Numeric) -> AbsorbedDose:
    """Construct an AbsorbedDose from a magnitude in megagrays.

    Parameters
    ----------
    value : Numeric
        Magnitude in megagrays.

    Returns
    -------
    AbsorbedDose
        AbsorbedDose represented in megagrays.

    """
    return AbsorbedDose(to_exact(value) * MEGAGRAY.scale, MEGAGRAY)


def Rad(value: Numeric) -> AbsorbedDose:
    """Construct an AbsorbedDose from a magnitude in rads.

    Parameters
    ----------
    value : Numeric
        Magnitude in rads.

    Returns
    -------
    AbsorbedDose
        AbsorbedDose represented in rads.

    """
    return AbsorbedDose(to_exact(value) * RAD.scale, RAD)


def Millirad(value: Numeric) -> AbsorbedDose:
    """Construct an AbsorbedDose from a magnitude in millirads.

    Parameters
    ----------
    value : Numeric
        Magnitude in millirads.

    Returns
    -------
    AbsorbedDose
        AbsorbedDose represented in millirads.

    """
    return AbsorbedDose(to_exact(value) * MILLIRAD.scale, MILLIRAD)


ABSORBED_DOSE_UNITS: Mapping[str, Callable[[Numeric], AbsorbedDose]] = unit_table(
    "ABSORBED_DOSE_UNITS",
    {
        GRAY: Gray,
        NANOGRAY: Nanogray,
        MICROGRAY: Microgray,
        MILLIGRAY: Milligray,
        CENTIGRAY: Centigray,
        KILOGRAY: Kilogray,
        MEGAGRAY: Megagray,
        RAD: Rad,
        MILLIRAD: Millirad,
    },
)

__all__ = [
    "ABSORBED_DOSE_UNITS",
    "CENTIGRAY",
    "GRAY",
    "KILOGRAY",
    "MEGAGRAY",
    "MICROGRAY",
    "MILLIGRAY",
    "MILLIRAD",
    "NANOGRAY",
    "RAD",
    "Centigray",
    "Gray",
    "Kilogray",
    "Megagray",
    "Microgray",
    "Milligray",
    "Millirad",
    "Nanogray",
    "Rad",
]
