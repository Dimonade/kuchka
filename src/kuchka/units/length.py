"""Unit constructors for Length: metric prefixes, plus Inch.

    from kuchka import Metre, Millimetre, Inch

    beam_diameter = Micrometre(50)
    panel_gap = Millimetre(2) + Inch(Decimal("0.1"))

`Metre` is the canonical spelling, matching BIPM's own spelling of the SI base unit.
`Meter` and its prefixed forms (`Millimeter`, `Kilometer`, `Micrometer`, `Nanometer`),
along with the matching `UnitDef` constants (`METER`, `MILLIMETER`, ...), are plain
aliases for American English use -- the exact same objects, not wrappers around them,
the same relationship `Tonne` has to `Megagram`.

Unlike `Tonne`/`Megagram`, there is no symbol to reconcile: both spellings display as
`m`.

Every imperial unit of length has been an exact decimal multiple of the metre since the
1959 international yard and pound agreement, so `Inch` sits alongside the metric
prefixes without giving up `Decimal` exactness:
`Inch(1) == Millimetre(Decimal("25.4"))` holds exactly, the same way
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

NANOMETRE = UnitDef("nanometre", "nm", Decimal("0.000000001"), LENGTH)
MICROMETRE = UnitDef("micrometre", "\u00b5m", Decimal("0.000001"), LENGTH)
MILLIMETRE = UnitDef("millimetre", "mm", Decimal("0.001"), LENGTH)
METRE = UnitDef("metre", "m", Decimal(1), LENGTH)
KILOMETRE = UnitDef("kilometre", "km", Decimal(1000), LENGTH)
INCH = UnitDef("inch", "in", Decimal("0.0254"), LENGTH)

NANOMETER = NANOMETRE
MICROMETER = MICROMETRE
MILLIMETER = MILLIMETRE
METER = METRE
KILOMETER = KILOMETRE

Length._canonical_unit = METRE  # noqa: SLF001 -- this module owns Length's canonical unit


def Nanometre(value: Numeric) -> Length:
    """Construct a Length from a magnitude expressed in nanometres."""
    return Length(to_decimal(value) * NANOMETRE.scale, NANOMETRE)


def Micrometre(value: Numeric) -> Length:
    """Construct a Length from a magnitude expressed in micrometres."""
    return Length(to_decimal(value) * MICROMETRE.scale, MICROMETRE)


def Millimetre(value: Numeric) -> Length:
    """Construct a Length from a magnitude expressed in millimetres."""
    return Length(to_decimal(value) * MILLIMETRE.scale, MILLIMETRE)


def Metre(value: Numeric) -> Length:
    """Construct a Length from a magnitude expressed in metres."""
    return Length(to_decimal(value) * METRE.scale, METRE)


def Kilometre(value: Numeric) -> Length:
    """Construct a Length from a magnitude expressed in kilometres."""
    return Length(to_decimal(value) * KILOMETRE.scale, KILOMETRE)


def Inch(value: Numeric) -> Length:
    """Construct a Length from a magnitude expressed in inches.

    Exact, not approximate: an inch has been defined as precisely
    0.0254 meters since 1959, so this conversion carries no more rounding
    error than any of the metric prefixes above.
    """
    return Length(to_decimal(value) * INCH.scale, INCH)


Nanometer = Nanometre
Micrometer = Micrometre
Millimeter = Millimetre
Meter = Metre
Kilometer = Kilometre

LENGTH_UNITS: Mapping[str, Callable[[Numeric], Length]] = MappingProxyType(
    {
        "nm": Nanometre,
        "um": Micrometre,
        "mm": Millimetre,
        "m": Metre,
        "km": Kilometre,
        "in": Inch,
    }
)
