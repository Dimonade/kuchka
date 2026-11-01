"""Molar charge: the electric charge carried by one mole of a substance."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import MOLAR_CHARGE
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.amount import AmountOfSubstance
    from kuchka.quantities.chemistry.entities_per_amount import EntitiesPerAmount
    from kuchka.quantities.chemistry.molar_energy import MolarEnergy
    from kuchka.quantities.chemistry.molar_flow_rate import MolarFlowRate
    from kuchka.quantities.current import Current
    from kuchka.quantities.electromagnetics.charge import Charge
    from kuchka.quantities.electromagnetics.voltage import Voltage
    from kuchka.quantities.proportion import Proportion


class MolarCharge(LinearQuantity):
    """The electric charge carried by one mole of a substance: coulombs per mole."""

    dimension: ClassVar[Dimension] = MOLAR_CHARGE
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: AmountOfSubstance) -> Charge: ...
    @overload
    def __mul__(self, other: MolarFlowRate) -> Current: ...
    @overload
    def __mul__(self, other: Proportion) -> MolarCharge: ...
    @overload
    def __mul__(self, other: Voltage) -> MolarEnergy: ...
    @overload
    def __mul__(self, other: Numeric) -> MolarCharge: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Charge) -> EntitiesPerAmount: ...
    @overload
    def __truediv__(self, other: EntitiesPerAmount) -> Charge: ...
    @overload
    def __truediv__(self, other: MolarCharge) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> MolarCharge: ...
    @overload
    def __truediv__(self, other: Numeric) -> MolarCharge: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(MOLAR_CHARGE, MolarCharge)

__all__ = ["MolarCharge"]
