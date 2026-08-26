"""Unit constructors for Length: metric prefixes, plus Inch.

    from kuchka import Meter, Millimeter, Inch

    beam_diameter = Micrometer(50)
    panel_gap = Millimeter(2) + Inch(Decimal("0.1"))

Every imperial unit of length has been an exact decimal multiple of the
metre since the 1959 international yard and pound agreement, so `Inch`
sits alongside the metric prefixes without giving up `Decimal` exactness:
`Inch(1) == Millimeter(Decimal("25.4"))` holds exactly, the same way
`Volt(1) == Millivolt(1000)` does.
`Foot` (0.3048 m exactly), `Yard` (0.9144 m exactly), and `Mile` (1609.344 m exactly)
are not implemented yet -- only `Inch` is, since it is the one that actually shows up
in mechanical and enclosure specs even in an otherwise metric shop -- but the same
exactness applies to all four, and adding one is a two-line `UnitDef` plus a
constructor function, the same shape as everything below.
"""

from __future__ import annotations

from decimal import Decimal
from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import LENGTH
from kuchka.numeric import Numeric
from kuchka.numeric import to_decimal
from kuchka.quantities import Length
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

NANOMETER = UnitDef("nanometer", "nm", Decimal("0.000000001"), LENGTH)
MICROMETER = UnitDef("micrometer", "\u00b5m", Decimal("0.000001"), LENGTH)
MILLIMETER = UnitDef("millimeter", "mm", Decimal("0.001"), LENGTH)
METER = UnitDef("meter", "m", Decimal(1), LENGTH)
KILOMETER = UnitDef("kilometer", "km", Decimal(1000), LENGTH)
INCH = UnitDef("inch", "in", Decimal("0.0254"), LENGTH)

Length._canonical_unit = METER  # noqa: SLF001 -- this module owns Length's canonical unit


def Nanometer(value: Numeric) -> Length:
    """Construct a Length from a magnitude expressed in nanometers."""
    return Length(to_decimal(value) * NANOMETER.scale, NANOMETER)


def Micrometer(value: Numeric) -> Length:
    """Construct a Length from a magnitude expressed in micrometers."""
    return Length(to_decimal(value) * MICROMETER.scale, MICROMETER)


def Millimeter(value: Numeric) -> Length:
    """Construct a Length from a magnitude expressed in millimeters."""
    return Length(to_decimal(value) * MILLIMETER.scale, MILLIMETER)


def Meter(value: Numeric) -> Length:
    """Construct a Length from a magnitude expressed in meters."""
    return Length(to_decimal(value) * METER.scale, METER)


def Kilometer(value: Numeric) -> Length:
    """Construct a Length from a magnitude expressed in kilometers."""
    return Length(to_decimal(value) * KILOMETER.scale, KILOMETER)


def Inch(value: Numeric) -> Length:
    """Construct a Length from a magnitude expressed in inches.

    Exact, not approximate: an inch has been defined as precisely
    0.0254 meters since 1959, so this conversion carries no more rounding
    error than any of the metric prefixes above.
    """
    return Length(to_decimal(value) * INCH.scale, INCH)


LENGTH_UNITS: Mapping[str, Callable[[Numeric], Length]] = MappingProxyType({
    "nm": Nanometer,
    "um": Micrometer,
    "mm": Millimeter,
    "m": Meter,
    "km": Kilometer,
    "in": Inch,
})
