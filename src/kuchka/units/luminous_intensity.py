"""LuminousIntensity unit constructors: Candela.

    from kuchka import Candela

    source = Candela(120)

`LUMINOUS_INTENSITY_UNITS` maps each symbol to its constructor, for boundary code that
reads a unit as a string from outside the application.

No prefixed constructors exist yet: figures in the current engineering vocabulary this
library targets stay within a couple of orders of magnitude of one candela, the same
reasoning that leaves `Foot` and `Yard` out of `Length` for now.
"""

from __future__ import annotations

from decimal import Decimal
from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import LUMINOUS_INTENSITY
from kuchka.numeric import Numeric
from kuchka.numeric import to_decimal
from kuchka.quantities import LuminousIntensity
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

CANDELA = UnitDef("candela", "cd", Decimal(1), LUMINOUS_INTENSITY)

LuminousIntensity._canonical_unit = CANDELA  # noqa: SLF001 -- this module owns LuminousIntensity's canonical unit


def Candela(value: Numeric) -> LuminousIntensity:
    """Construct a LuminousIntensity from a magnitude expressed in candela."""
    return LuminousIntensity(to_decimal(value) * CANDELA.scale, CANDELA)


LUMINOUS_INTENSITY_UNITS: Mapping[str, Callable[[Numeric], LuminousIntensity]] = (
    MappingProxyType(
        {
            "cd": Candela,
        }
    )
)
