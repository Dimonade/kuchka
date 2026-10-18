"""Energy density: energy per unit volume.

Shares its dimension with `Pressure` (both are M L^-1 T^-2), and is a different
concept: a pressure is a force on an area, and an energy density is how much energy a
volume holds.
Neither is the general kind of the dimension, so `EnergyDensity` and `Pressure` are
contested, and the operand kinds decide the result:

- `Energy / Volume -> EnergyDensity`, declared here, and its inverses,
  `EnergyDensity * Volume -> Energy` and `Energy / EnergyDensity -> Volume`, whose
  other overload halves live on `Volume` and `Energy` themselves;
- `Force / Area -> Pressure`, declared with `Pressure`.

Any other operation that produces this dimension raises `AmbiguousKindError`, and a
`Pressure` or an `EnergyDensity` is then constructed explicitly.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import ENERGY_DENSITY
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register
from kuchka.quantities.base.registry import _rule
from kuchka.quantities.energy import Energy
from kuchka.quantities.pressure import Pressure
from kuchka.quantities.volume import Volume

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.area import Area
    from kuchka.quantities.kinematics import Force
    from kuchka.quantities.proportion import Proportion


class EnergyDensity(LinearQuantity):
    """Energy per unit volume: how much energy a volume of a material or store holds."""

    dimension: ClassVar[Dimension] = ENERGY_DENSITY
    __slots__ = ()

    @overload
    def __mul__(self, other: Volume) -> Energy: ...
    @overload
    def __mul__(self, other: Area) -> Force: ...
    @overload
    def __mul__(self, other: Proportion) -> EnergyDensity: ...
    @overload
    def __mul__(self, other: Numeric) -> EnergyDensity: ...
    @overload
    def __mul__(self, other: LinearQuantity) -> LinearQuantity | Fraction: ...

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: EnergyDensity) -> Proportion: ...
    @overload
    def __truediv__(self, other: Pressure) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> EnergyDensity: ...
    @overload
    def __truediv__(self, other: Numeric) -> EnergyDensity: ...
    @overload
    def __truediv__(self, other: LinearQuantity) -> LinearQuantity | Fraction: ...

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(ENERGY_DENSITY, EnergyDensity, contested_with=Pressure)
_rule(Energy, "/", Volume, EnergyDensity)

__all__ = ["EnergyDensity"]
