"""Mass: how much matter something contains."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import MASS
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.geometry.volume import Volume
    from kuchka.quantities.kinematics.acceleration import Acceleration
    from kuchka.quantities.mechanics.density import Density
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.force import Force
    from kuchka.quantities.mechanics.specific_energy import SpecificEnergy
    from kuchka.quantities.proportion import Proportion


class Mass(LinearQuantity):
    """How much matter something contains."""

    dimension: ClassVar[Dimension] = MASS
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Acceleration) -> Force: ...
    @overload
    def __mul__(self, other: Proportion) -> Mass: ...
    @overload
    def __mul__(self, other: SpecificEnergy) -> Energy: ...
    @overload
    def __mul__(self, other: Numeric) -> Mass: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Density) -> Volume: ...
    @overload
    def __truediv__(self, other: Mass) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> Mass: ...
    @overload
    def __truediv__(self, other: Volume) -> Density: ...
    @overload
    def __truediv__(self, other: Numeric) -> Mass: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(MASS, Mass)

__all__ = ["Mass"]
