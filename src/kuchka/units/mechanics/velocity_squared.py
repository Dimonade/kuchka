"""Velocity-squared unit constructors: square metres and kilometres per second squared.

    from kuchka import SquareKilometrePerSecondSquared

    gravitational_parameter_term = SquareKilometrePerSecondSquared(62.5)

A velocity squared is a velocity times a velocity, and shares its dimension with
`SpecificEnergy`, so a value is converted between the two explicitly.

`VELOCITY_SQUARED_UNITS` maps each symbol to its constructor, for boundary code that
reads a unit as a string from outside the application.
"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from kuchka.dimensions import VELOCITY_SQUARED
from kuchka.internal import symbols
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import UnitDef
from kuchka.quantities import VelocitySquared

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

_DOT = symbols.MIDDLE_DOT

SQUARE_METRE_PER_SECOND_SQUARED = UnitDef(
    "square_metre_per_second_squared",
    f"m{symbols.SUPERSCRIPT_TWO}/s{symbols.SUPERSCRIPT_TWO}",
    Decimal(1),
    VELOCITY_SQUARED,
    aliases=(
        "m^2/s^2",
        "m**2/s**2",
    ),
    words=("square metres per second squared", "square meters per second squared"),
)
SQUARE_KILOMETRE_PER_SECOND_SQUARED = UnitDef(
    "square_kilometre_per_second_squared",
    f"km{symbols.SUPERSCRIPT_TWO}/s{symbols.SUPERSCRIPT_TWO}",
    Decimal(1_000_000),
    VELOCITY_SQUARED,
    aliases=(
        "km^2/s^2",
        "km**2/s**2",
    ),
    words=(
        "square kilometres per second squared",
        "square kilometers per second squared",
    ),
)

VelocitySquared._canonical_unit = SQUARE_METRE_PER_SECOND_SQUARED  # noqa: SLF001 -- this module owns VelocitySquared's canonical unit


def SquareMetrePerSecondSquared(value: Numeric) -> VelocitySquared:
    """Construct a VelocitySquared from square metres per second squared."""
    return VelocitySquared(
        to_exact(value) * SQUARE_METRE_PER_SECOND_SQUARED.scale,
        SQUARE_METRE_PER_SECOND_SQUARED,
    )


def SquareKilometrePerSecondSquared(value: Numeric) -> VelocitySquared:
    """Construct a VelocitySquared from square kilometres per second squared."""
    return VelocitySquared(
        to_exact(value) * SQUARE_KILOMETRE_PER_SECOND_SQUARED.scale,
        SQUARE_KILOMETRE_PER_SECOND_SQUARED,
    )


VELOCITY_SQUARED_UNITS: Mapping[str, Callable[[Numeric], VelocitySquared]] = unit_table(
    "VELOCITY_SQUARED_UNITS",
    {
        SQUARE_METRE_PER_SECOND_SQUARED: SquareMetrePerSecondSquared,
        SQUARE_KILOMETRE_PER_SECOND_SQUARED: SquareKilometrePerSecondSquared,
    },
)

__all__ = [
    "SQUARE_KILOMETRE_PER_SECOND_SQUARED",
    "SQUARE_METRE_PER_SECOND_SQUARED",
    "VELOCITY_SQUARED_UNITS",
    "SquareKilometrePerSecondSquared",
    "SquareMetrePerSecondSquared",
]
