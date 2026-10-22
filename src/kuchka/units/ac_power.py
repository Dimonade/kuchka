"""Unit constructors for ApparentPower and ReactivePower: the volt-ampere and the var.

    from kuchka import KilovoltAmpere, Kilovar

    supply = KilovoltAmpere(5)
    compensation = Kilovar(2)

The volt-ampere (`VA`) measures `ApparentPower` and the var (`var`) measures
`ReactivePower`.
Both have the dimension of the watt, and each has its own units and its own type, so
a volt-ampere is never added to a watt or a var by accident.
The units run from the milli- to the giga- multiple.

Examples
--------
A transformer rated 5 kVA with 3.2 kVA connected has 1.8 kVA left:

>>> headroom = KilovoltAmpere(5) - VoltAmpere(3200)
>>> headroom.to(KILOVOLT_AMPERE)
1.8 kVA

A bank of capacitors rated 2 kvar against an inductive load of 3.5 kvar leaves 1.5 kvar
of inductive reactive power, shown as a negative number:

>>> Kilovar(2) - Kilovar(3.5)
-1.5 kvar

`VAr` and `VAR` read as the var, so `kVAr` and `MVAR` are accepted too.

`APPARENT_POWER_UNITS` and `REACTIVE_POWER_UNITS` map each symbol to its constructor,
for boundary code that reads a unit as a string from outside the application.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import POWER
from kuchka.internal import prefixes
from kuchka.internal.prefixes import with_prefix
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import ApparentPower
from kuchka.quantities import ReactivePower
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

VOLT_AMPERE = UnitDef(
    "volt_ampere",
    "VA",
    1,
    POWER,
    words=("volt ampere", "volt-ampere", "voltampere"),
)
MILLIVOLT_AMPERE = with_prefix(prefixes.MILLI, VOLT_AMPERE)
KILOVOLT_AMPERE = with_prefix(prefixes.KILO, VOLT_AMPERE)
MEGAVOLT_AMPERE = with_prefix(prefixes.MEGA, VOLT_AMPERE)
GIGAVOLT_AMPERE = with_prefix(prefixes.GIGA, VOLT_AMPERE)

ApparentPower._canonical_unit = VOLT_AMPERE  # noqa: SLF001 -- this module owns ApparentPower's canonical unit


def VoltAmpere(value: Numeric) -> ApparentPower:
    """Construct an ApparentPower from a magnitude expressed in volt-amperes.

    Parameters
    ----------
    value : Numeric
        Apparent power in volt-amperes.

    Returns
    -------
    ApparentPower
        Apparent power represented in volt-amperes.

    Examples
    --------
    >>> VoltAmpere(1).to(VOLT_AMPERE)
    1 VA

    """
    return ApparentPower(to_exact(value) * VOLT_AMPERE.scale, VOLT_AMPERE)


def MillivoltAmpere(value: Numeric) -> ApparentPower:
    """Construct an ApparentPower from a magnitude expressed in millivolt-amperes.

    Parameters
    ----------
    value : Numeric
        Apparent power in millivolt-amperes.

    Returns
    -------
    ApparentPower
        Apparent power represented in millivolt-amperes.

    Examples
    --------
    >>> MillivoltAmpere(1).to(VOLT_AMPERE)
    0.001 VA

    """
    return ApparentPower(to_exact(value) * MILLIVOLT_AMPERE.scale, MILLIVOLT_AMPERE)


def KilovoltAmpere(value: Numeric) -> ApparentPower:
    """Construct an ApparentPower from a magnitude expressed in kilovolt-amperes.

    Parameters
    ----------
    value : Numeric
        Apparent power in kilovolt-amperes.

    Returns
    -------
    ApparentPower
        Apparent power represented in kilovolt-amperes.

    Examples
    --------
    >>> KilovoltAmpere(1).to(VOLT_AMPERE)
    1000 VA

    """
    return ApparentPower(to_exact(value) * KILOVOLT_AMPERE.scale, KILOVOLT_AMPERE)


def MegavoltAmpere(value: Numeric) -> ApparentPower:
    """Construct an ApparentPower from a magnitude expressed in megavolt-amperes.

    Parameters
    ----------
    value : Numeric
        Apparent power in megavolt-amperes.

    Returns
    -------
    ApparentPower
        Apparent power represented in megavolt-amperes.

    Examples
    --------
    >>> MegavoltAmpere(1).to(VOLT_AMPERE)
    1000000 VA

    """
    return ApparentPower(to_exact(value) * MEGAVOLT_AMPERE.scale, MEGAVOLT_AMPERE)


def GigavoltAmpere(value: Numeric) -> ApparentPower:
    """Construct an ApparentPower from a magnitude expressed in gigavolt-amperes.

    Parameters
    ----------
    value : Numeric
        Apparent power in gigavolt-amperes.

    Returns
    -------
    ApparentPower
        Apparent power represented in gigavolt-amperes.

    Examples
    --------
    >>> GigavoltAmpere(1).to(VOLT_AMPERE)
    1000000000 VA

    """
    return ApparentPower(to_exact(value) * GIGAVOLT_AMPERE.scale, GIGAVOLT_AMPERE)


APPARENT_POWER_UNITS: Mapping[str, Callable[[Numeric], ApparentPower]] = unit_table(
    "APPARENT_POWER_UNITS",
    {
        VOLT_AMPERE: VoltAmpere,
        MILLIVOLT_AMPERE: MillivoltAmpere,
        KILOVOLT_AMPERE: KilovoltAmpere,
        MEGAVOLT_AMPERE: MegavoltAmpere,
        GIGAVOLT_AMPERE: GigavoltAmpere,
    },
)

VAR = UnitDef(
    "var",
    "var",
    1,
    POWER,
    aliases=("VAr", "VAR"),
    words=("volt ampere reactive", "volt-ampere reactive"),
)
MILLIVAR = with_prefix(prefixes.MILLI, VAR)
KILOVAR = with_prefix(prefixes.KILO, VAR)
MEGAVAR = with_prefix(prefixes.MEGA, VAR)
GIGAVAR = with_prefix(prefixes.GIGA, VAR)

ReactivePower._canonical_unit = VAR  # noqa: SLF001 -- this module owns ReactivePower's canonical unit


def Var(value: Numeric) -> ReactivePower:
    """Construct a ReactivePower from a magnitude expressed in vars.

    Parameters
    ----------
    value : Numeric
        Reactive power in vars.

    Returns
    -------
    ReactivePower
        Reactive power represented in vars.

    Examples
    --------
    >>> Var(1).to(VAR)
    1 var

    """
    return ReactivePower(to_exact(value) * VAR.scale, VAR)


def Millivar(value: Numeric) -> ReactivePower:
    """Construct a ReactivePower from a magnitude expressed in millivars.

    Parameters
    ----------
    value : Numeric
        Reactive power in millivars.

    Returns
    -------
    ReactivePower
        Reactive power represented in millivars.

    Examples
    --------
    >>> Millivar(1).to(VAR)
    0.001 var

    """
    return ReactivePower(to_exact(value) * MILLIVAR.scale, MILLIVAR)


def Kilovar(value: Numeric) -> ReactivePower:
    """Construct a ReactivePower from a magnitude expressed in kilovars.

    Parameters
    ----------
    value : Numeric
        Reactive power in kilovars.

    Returns
    -------
    ReactivePower
        Reactive power represented in kilovars.

    Examples
    --------
    >>> Kilovar(1).to(VAR)
    1000 var

    """
    return ReactivePower(to_exact(value) * KILOVAR.scale, KILOVAR)


def Megavar(value: Numeric) -> ReactivePower:
    """Construct a ReactivePower from a magnitude expressed in megavars.

    Parameters
    ----------
    value : Numeric
        Reactive power in megavars.

    Returns
    -------
    ReactivePower
        Reactive power represented in megavars.

    Examples
    --------
    >>> Megavar(1).to(VAR)
    1000000 var

    """
    return ReactivePower(to_exact(value) * MEGAVAR.scale, MEGAVAR)


def Gigavar(value: Numeric) -> ReactivePower:
    """Construct a ReactivePower from a magnitude expressed in gigavars.

    Parameters
    ----------
    value : Numeric
        Reactive power in gigavars.

    Returns
    -------
    ReactivePower
        Reactive power represented in gigavars.

    Examples
    --------
    >>> Gigavar(1).to(VAR)
    1000000000 var

    """
    return ReactivePower(to_exact(value) * GIGAVAR.scale, GIGAVAR)


REACTIVE_POWER_UNITS: Mapping[str, Callable[[Numeric], ReactivePower]] = unit_table(
    "REACTIVE_POWER_UNITS",
    {
        VAR: Var,
        MILLIVAR: Millivar,
        KILOVAR: Kilovar,
        MEGAVAR: Megavar,
        GIGAVAR: Gigavar,
    },
)

__all__ = [
    "APPARENT_POWER_UNITS",
    "GIGAVAR",
    "GIGAVOLT_AMPERE",
    "KILOVAR",
    "KILOVOLT_AMPERE",
    "MEGAVAR",
    "MEGAVOLT_AMPERE",
    "MILLIVAR",
    "MILLIVOLT_AMPERE",
    "REACTIVE_POWER_UNITS",
    "VAR",
    "VOLT_AMPERE",
    "Gigavar",
    "GigavoltAmpere",
    "Kilovar",
    "KilovoltAmpere",
    "Megavar",
    "MegavoltAmpere",
    "Millivar",
    "MillivoltAmpere",
    "Var",
    "VoltAmpere",
]
