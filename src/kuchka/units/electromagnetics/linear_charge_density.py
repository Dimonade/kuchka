"""Unit constructors for linear charge density: coulombs per metre and its prefixes.

    from kuchka import CoulombPerMetre, NanocoulombPerMetre

    line = CoulombPerMetre(0.5)
    cable = NanocoulombPerMetre(120)

`LinearChargeDensity` is electric charge along a line, `Charge / Length`.
Its canonical unit is the coulomb per metre (`C/m`).

Examples
--------
A line carrying 0.5 C/m holds 2 C over 4 m:

>>> from kuchka import Metre
>>> CoulombPerMetre(0.5) * Metre(4)
2 C

`LINEAR_CHARGE_DENSITY_UNITS` maps symbols such as ``"C/m"`` and ``"nC/m"`` to their
constructors, for boundary code that reads a unit as a string from outside the
application.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import LINEAR_CHARGE_DENSITY
from kuchka.internal import prefixes
from kuchka.internal.prefixes import with_prefix
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import LinearChargeDensity
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

COULOMB_PER_METRE = UnitDef(
    "coulomb_per_metre",
    "C/m",
    1,
    LINEAR_CHARGE_DENSITY,
    words=("coulombs per metre", "coulombs per meter"),
)
MILLICOULOMB_PER_METRE = with_prefix(prefixes.MILLI, COULOMB_PER_METRE)
MICROCOULOMB_PER_METRE = with_prefix(prefixes.MICRO, COULOMB_PER_METRE)
NANOCOULOMB_PER_METRE = with_prefix(prefixes.NANO, COULOMB_PER_METRE)
PICOCOULOMB_PER_METRE = with_prefix(prefixes.PICO, COULOMB_PER_METRE)

LinearChargeDensity._canonical_unit = COULOMB_PER_METRE  # noqa: SLF001 -- this module owns LinearChargeDensity's canonical unit


def CoulombPerMetre(value: Numeric) -> LinearChargeDensity:
    """Construct a LinearChargeDensity from coulombs per metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in coulombs per metre.

    Returns
    -------
    LinearChargeDensity
        LinearChargeDensity represented in coulombs per metre.

    """
    return LinearChargeDensity(
        to_exact(value) * COULOMB_PER_METRE.scale, COULOMB_PER_METRE
    )


def MillicoulombPerMetre(value: Numeric) -> LinearChargeDensity:
    """Construct a LinearChargeDensity from millicoulombs per metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in millicoulombs per metre.

    Returns
    -------
    LinearChargeDensity
        LinearChargeDensity represented in millicoulombs per metre.

    """
    return LinearChargeDensity(
        to_exact(value) * MILLICOULOMB_PER_METRE.scale, MILLICOULOMB_PER_METRE
    )


def MicrocoulombPerMetre(value: Numeric) -> LinearChargeDensity:
    """Construct a LinearChargeDensity from microcoulombs per metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in microcoulombs per metre.

    Returns
    -------
    LinearChargeDensity
        LinearChargeDensity represented in microcoulombs per metre.

    """
    return LinearChargeDensity(
        to_exact(value) * MICROCOULOMB_PER_METRE.scale, MICROCOULOMB_PER_METRE
    )


def NanocoulombPerMetre(value: Numeric) -> LinearChargeDensity:
    """Construct a LinearChargeDensity from nanocoulombs per metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in nanocoulombs per metre.

    Returns
    -------
    LinearChargeDensity
        LinearChargeDensity represented in nanocoulombs per metre.

    """
    return LinearChargeDensity(
        to_exact(value) * NANOCOULOMB_PER_METRE.scale, NANOCOULOMB_PER_METRE
    )


def PicocoulombPerMetre(value: Numeric) -> LinearChargeDensity:
    """Construct a LinearChargeDensity from picocoulombs per metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in picocoulombs per metre.

    Returns
    -------
    LinearChargeDensity
        LinearChargeDensity represented in picocoulombs per metre.

    """
    return LinearChargeDensity(
        to_exact(value) * PICOCOULOMB_PER_METRE.scale, PICOCOULOMB_PER_METRE
    )


LINEAR_CHARGE_DENSITY_UNITS: Mapping[str, Callable[[Numeric], LinearChargeDensity]] = (
    unit_table(
        "LINEAR_CHARGE_DENSITY_UNITS",
        {
            COULOMB_PER_METRE: CoulombPerMetre,
            MILLICOULOMB_PER_METRE: MillicoulombPerMetre,
            MICROCOULOMB_PER_METRE: MicrocoulombPerMetre,
            NANOCOULOMB_PER_METRE: NanocoulombPerMetre,
            PICOCOULOMB_PER_METRE: PicocoulombPerMetre,
        },
    )
)

__all__ = [
    "COULOMB_PER_METRE",
    "LINEAR_CHARGE_DENSITY_UNITS",
    "MICROCOULOMB_PER_METRE",
    "MILLICOULOMB_PER_METRE",
    "NANOCOULOMB_PER_METRE",
    "PICOCOULOMB_PER_METRE",
    "CoulombPerMetre",
    "MicrocoulombPerMetre",
    "MillicoulombPerMetre",
    "NanocoulombPerMetre",
    "PicocoulombPerMetre",
]
