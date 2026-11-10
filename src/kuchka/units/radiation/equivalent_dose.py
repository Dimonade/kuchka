"""Equivalent dose constructors: the sievert, its prefixes, and the rem.

    from kuchka import Microsievert, Millisievert, Sievert

    reading = Microsievert(0.12)
    annual = Millisievert(2.4)

`EquivalentDose` is an absorbed dose weighted for its effect on tissue.
Its SI unit is the sievert (`Sv`), exactly one joule per kilogram, the same as the gray.
The rem (`rem`) is the older CGS unit, defined exactly as a hundredth of a sievert, so
`Millisievert(10)` and `Rem(1)` are the same dose.
The module provides the sievert from nano- through kilo- multiples, and the rem and the
millirem.

A sievert measures risk and not energy, so the unit tables of `EquivalentDose` and
`AbsorbedDose` do not mix, and a dose in grays becomes one in sieverts only through
`EquivalentDose.from_absorbed_dose` and a radiation weighting factor.
The type covers the protection quantities measured in sieverts: equivalent dose,
effective dose, and the ambient and personal dose equivalents an instrument reads.

Examples
--------
A dosimeter reading is often in microsieverts per hour, which is a rate and not an
equivalent dose.
A total of 0.12 µSv, in nanosieverts:

>>> Microsievert(0.12).to(NANOSIEVERT)
120 nSv

A limit of 5 rem, in the unit the SI uses:

>>> Rem(5).to(MILLISIEVERT)
50 mSv

`EQUIVALENT_DOSE_UNITS` maps symbols such as ``"Sv"``, ``"mSv"``, ``"uSv"``, ``"rem"``,
and ``"mrem"`` to their constructors for boundary code that reads unit labels from
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
from kuchka.quantities import EquivalentDose
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

SIEVERT = UnitDef("sievert", "Sv", 1, SPECIFIC_ENERGY)
NANOSIEVERT = with_prefix(prefixes.NANO, SIEVERT)
MICROSIEVERT = with_prefix(prefixes.MICRO, SIEVERT)
MILLISIEVERT = with_prefix(prefixes.MILLI, SIEVERT)
KILOSIEVERT = with_prefix(prefixes.KILO, SIEVERT)
REM = UnitDef("rem", "rem", Fraction(1, 100), SPECIFIC_ENERGY)
MILLIREM = with_prefix(prefixes.MILLI, REM)

EquivalentDose._canonical_unit = SIEVERT  # noqa: SLF001 -- this module owns EquivalentDose's canonical unit


def Sievert(value: Numeric) -> EquivalentDose:
    """Construct an EquivalentDose from a magnitude in sieverts.

    Parameters
    ----------
    value : Numeric
        Magnitude in sieverts.

    Returns
    -------
    EquivalentDose
        EquivalentDose represented in sieverts.

    """
    return EquivalentDose(to_exact(value) * SIEVERT.scale, SIEVERT)


def Nanosievert(value: Numeric) -> EquivalentDose:
    """Construct an EquivalentDose from a magnitude in nanosieverts.

    Parameters
    ----------
    value : Numeric
        Magnitude in nanosieverts.

    Returns
    -------
    EquivalentDose
        EquivalentDose represented in nanosieverts.

    """
    return EquivalentDose(to_exact(value) * NANOSIEVERT.scale, NANOSIEVERT)


def Microsievert(value: Numeric) -> EquivalentDose:
    """Construct an EquivalentDose from a magnitude in microsieverts.

    Parameters
    ----------
    value : Numeric
        Magnitude in microsieverts.

    Returns
    -------
    EquivalentDose
        EquivalentDose represented in microsieverts.

    """
    return EquivalentDose(to_exact(value) * MICROSIEVERT.scale, MICROSIEVERT)


def Millisievert(value: Numeric) -> EquivalentDose:
    """Construct an EquivalentDose from a magnitude in millisieverts.

    Parameters
    ----------
    value : Numeric
        Magnitude in millisieverts.

    Returns
    -------
    EquivalentDose
        EquivalentDose represented in millisieverts.

    """
    return EquivalentDose(to_exact(value) * MILLISIEVERT.scale, MILLISIEVERT)


def Kilosievert(value: Numeric) -> EquivalentDose:
    """Construct an EquivalentDose from a magnitude in kilosieverts.

    Parameters
    ----------
    value : Numeric
        Magnitude in kilosieverts.

    Returns
    -------
    EquivalentDose
        EquivalentDose represented in kilosieverts.

    """
    return EquivalentDose(to_exact(value) * KILOSIEVERT.scale, KILOSIEVERT)


def Rem(value: Numeric) -> EquivalentDose:
    """Construct an EquivalentDose from a magnitude in rems.

    Parameters
    ----------
    value : Numeric
        Magnitude in rems.

    Returns
    -------
    EquivalentDose
        EquivalentDose represented in rems.

    Examples
    --------
    A rem is ten millisieverts:

    >>> Rem(1) == Millisievert(10)
    True

    """
    return EquivalentDose(to_exact(value) * REM.scale, REM)


def Millirem(value: Numeric) -> EquivalentDose:
    """Construct an EquivalentDose from a magnitude in millirems.

    Parameters
    ----------
    value : Numeric
        Magnitude in millirems.

    Returns
    -------
    EquivalentDose
        EquivalentDose represented in millirems.

    """
    return EquivalentDose(to_exact(value) * MILLIREM.scale, MILLIREM)


EQUIVALENT_DOSE_UNITS: Mapping[str, Callable[[Numeric], EquivalentDose]] = unit_table(
    "EQUIVALENT_DOSE_UNITS",
    {
        SIEVERT: Sievert,
        NANOSIEVERT: Nanosievert,
        MICROSIEVERT: Microsievert,
        MILLISIEVERT: Millisievert,
        KILOSIEVERT: Kilosievert,
        REM: Rem,
        MILLIREM: Millirem,
    },
)

__all__ = [
    "EQUIVALENT_DOSE_UNITS",
    "KILOSIEVERT",
    "MICROSIEVERT",
    "MILLIREM",
    "MILLISIEVERT",
    "NANOSIEVERT",
    "REM",
    "SIEVERT",
    "Kilosievert",
    "Microsievert",
    "Millirem",
    "Millisievert",
    "Nanosievert",
    "Rem",
    "Sievert",
]
