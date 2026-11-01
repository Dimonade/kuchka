"""Catalytic activity constructors: Katal, Microkatal, EnzymeUnit, and more.

Catalytic activity is the rate at which a catalyst converts a substrate: the katal
(`kat`) is one mole converted per second, and is the canonical unit.
Enzymes are measured in the prefixed forms (`mkat`, `µkat`, `nkat`) and in the enzyme
unit (`U`), the older unit of one micromole converted per minute, so `1 U` is exactly
`1/60 µkat`.

A catalytic activity has the dimension of a `MolarFlowRate` and is not interchangeable
with one: `CatalyticActivity.to_molar_flow_rate()` is the conversion.
The international unit `IU` is not a spelling, because it also measures vitamins and
hormones.

`CATALYTIC_ACTIVITY_UNITS` maps each symbol to its constructor, for boundary code that
reads a unit as a string from outside the application.
"""

from __future__ import annotations

from fractions import Fraction
from typing import TYPE_CHECKING

from kuchka.dimensions import MOLAR_FLOW_RATE
from kuchka.internal import prefixes
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import CatalyticActivity
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

KATAL_NAME = "katal"
KATAL_SYMBOL = "kat"

NANOKATAL = prefixed_unit(prefixes.NANO, KATAL_NAME, KATAL_SYMBOL, MOLAR_FLOW_RATE)
MICROKATAL = prefixed_unit(prefixes.MICRO, KATAL_NAME, KATAL_SYMBOL, MOLAR_FLOW_RATE)
MILLIKATAL = prefixed_unit(prefixes.MILLI, KATAL_NAME, KATAL_SYMBOL, MOLAR_FLOW_RATE)
KATAL = prefixed_unit(prefixes.UNIT, KATAL_NAME, KATAL_SYMBOL, MOLAR_FLOW_RATE)
ENZYME_UNIT = UnitDef(
    "enzyme_unit",
    "U",
    Fraction(1, 60_000_000),
    MOLAR_FLOW_RATE,
    words=("enzyme unit",),
)

CatalyticActivity._canonical_unit = KATAL  # noqa: SLF001 -- this module owns CatalyticActivity's canonical unit


def Nanokatal(value: Numeric) -> CatalyticActivity:
    """Construct a catalytic activity from a magnitude in nanokatals.

    Parameters
    ----------
    value : Numeric
        Catalytic activity magnitude in nkat.

    Returns
    -------
    CatalyticActivity
        Catalytic activity represented in nanokatals.

    """
    return CatalyticActivity(to_exact(value) * NANOKATAL.scale, NANOKATAL)


def Microkatal(value: Numeric) -> CatalyticActivity:
    """Construct a catalytic activity from a magnitude in microkatals.

    Parameters
    ----------
    value : Numeric
        Catalytic activity magnitude in µkat.

    Returns
    -------
    CatalyticActivity
        Catalytic activity represented in microkatals.

    """
    return CatalyticActivity(to_exact(value) * MICROKATAL.scale, MICROKATAL)


def Millikatal(value: Numeric) -> CatalyticActivity:
    """Construct a catalytic activity from a magnitude in millikatals.

    Parameters
    ----------
    value : Numeric
        Catalytic activity magnitude in mkat.

    Returns
    -------
    CatalyticActivity
        Catalytic activity represented in millikatals.

    """
    return CatalyticActivity(to_exact(value) * MILLIKATAL.scale, MILLIKATAL)


def Katal(value: Numeric) -> CatalyticActivity:
    """Construct a catalytic activity from a magnitude in katals.

    Parameters
    ----------
    value : Numeric
        Catalytic activity magnitude in kat.

    Returns
    -------
    CatalyticActivity
        Catalytic activity represented in katals.

    Examples
    --------
    A preparation of 120 nkat converts 7.2 µmol of substrate each minute:

    >>> Nanokatal(120).to_molar_flow_rate()
    0.00000012 mol/s

    """
    return CatalyticActivity(to_exact(value) * KATAL.scale, KATAL)


def EnzymeUnit(value: Numeric) -> CatalyticActivity:
    """Construct a catalytic activity from a magnitude in enzyme units.

    Parameters
    ----------
    value : Numeric
        Catalytic activity magnitude in U.

    Returns
    -------
    CatalyticActivity
        Catalytic activity represented in enzyme units.

    Examples
    --------
    An enzyme unit is a micromole per minute, a sixtieth of a microkatal:

    >>> EnzymeUnit(60) == Microkatal(1)
    True

    """
    return CatalyticActivity(to_exact(value) * ENZYME_UNIT.scale, ENZYME_UNIT)


CATALYTIC_ACTIVITY_UNITS: Mapping[str, Callable[[Numeric], CatalyticActivity]] = (
    unit_table(
        "CATALYTIC_ACTIVITY_UNITS",
        {
            NANOKATAL: Nanokatal,
            MICROKATAL: Microkatal,
            MILLIKATAL: Millikatal,
            KATAL: Katal,
            ENZYME_UNIT: EnzymeUnit,
        },
    )
)

__all__ = [
    "CATALYTIC_ACTIVITY_UNITS",
    "ENZYME_UNIT",
    "KATAL",
    "MICROKATAL",
    "MILLIKATAL",
    "NANOKATAL",
    "EnzymeUnit",
    "Katal",
    "Microkatal",
    "Millikatal",
    "Nanokatal",
]
