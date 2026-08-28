"""Unit constructors for Proportion: Ratio and Percent.

    from kuchka import Percent, Ratio

    tolerance = Percent(5)
    duty_cycle = Ratio(Decimal("0.8"))

`Ratio` is the coherent, unscaled unit: a bare fraction, typically between 0 and 1.
`Percent` is a hundredth of that: `Percent(5) == Ratio(Decimal("0.05"))`.
ISO 80000 denotes the coherent unit for a dimensionless quantity as `"1"`;
`repr()` follows that convention, so `Ratio(Decimal("0.05"))` prints as `0.05 1`.
"""

from __future__ import annotations

from decimal import Decimal
from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import DIMENSIONLESS
from kuchka.numeric import Numeric
from kuchka.numeric import to_decimal
from kuchka.quantities import Proportion
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

RATIO = UnitDef("ratio", "1", Decimal(1), DIMENSIONLESS)
PERCENT = UnitDef("percent", "%", Decimal("0.01"), DIMENSIONLESS)

Proportion._canonical_unit = RATIO  # noqa: SLF001 -- this module owns Proportion's canonical unit


def Ratio(value: Numeric) -> Proportion:
    """Construct a Proportion from a bare fraction, e.g. 0.05 for five percent."""
    return Proportion(to_decimal(value) * RATIO.scale, RATIO)


def Percent(value: Numeric) -> Proportion:
    """Construct a Proportion from a magnitude expressed in percent."""
    return Proportion(to_decimal(value) * PERCENT.scale, PERCENT)


PROPORTION_UNITS: Mapping[str, Callable[[Numeric], Proportion]] = MappingProxyType(
    {
        "1": Ratio,
        "%": Percent,
    }
)
