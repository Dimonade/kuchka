"""LuminousIntensity unit constructors: Candela.

This module defines the canonical candela unit and its public constructor.

Examples
--------
>>> from kuchka import Candela
>>> source = Candela(120)
>>> type(source).__name__
'LuminousIntensity'

Notes
-----
`LUMINOUS_INTENSITY_UNITS` maps each unit symbol to its constructor.
This is intended for boundary code that receives a unit as a string from outside the
application.

"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from kuchka.dimensions import LUMINOUS_INTENSITY
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import LuminousIntensity
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

CANDELA = UnitDef("candela", "cd", Decimal(1), LUMINOUS_INTENSITY)
"""Definition of the candela unit."""

LuminousIntensity._canonical_unit = CANDELA  # noqa: SLF001 -- this module owns LuminousIntensity's canonical unit


def Candela(value: Numeric) -> LuminousIntensity:
    """Construct a luminous intensity from a magnitude in candela.

    Parameters
    ----------
    value : Numeric
        Magnitude expressed in candela.

    Returns
    -------
    LuminousIntensity
        Luminous intensity represented by `value` candela.

    Examples
    --------
    >>> source = Candela(120)
    >>> type(source).__name__
    'LuminousIntensity'

    See Also
    --------
    CANDELA : Definition of the candela unit.
    LUMINOUS_INTENSITY_UNITS : Available luminous intensity units.
    LuminousIntensity : Quantity type represented by this constructor.

    """
    return LuminousIntensity(to_exact(value) * CANDELA.scale, CANDELA)


LUMINOUS_INTENSITY_UNITS: Mapping[str, Callable[[Numeric], LuminousIntensity]] = (
    unit_table(
        "LUMINOUS_INTENSITY_UNITS",
        {
            CANDELA: Candela,
        },
    )
)
"""Mappings from unit symbols to their constructors."""

__all__ = [
    "CANDELA",
    "LUMINOUS_INTENSITY_UNITS",
    "Candela",
]
