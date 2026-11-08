"""Conductance: how readily a circuit element passes current."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import CONDUCTANCE
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.current import Current
    from kuchka.quantities.electromagnetics.capacitance import Capacitance
    from kuchka.quantities.electromagnetics.charge import Charge
    from kuchka.quantities.electromagnetics.electric_field_strength import (
        ElectricFieldStrength,
    )
    from kuchka.quantities.electromagnetics.inductance import Inductance
    from kuchka.quantities.electromagnetics.magnetic_field_strength import (
        MagneticFieldStrength,
    )
    from kuchka.quantities.electromagnetics.magnetic_flux import MagneticFlux
    from kuchka.quantities.electromagnetics.magnetic_flux_density import (
        MagneticFluxDensity,
    )
    from kuchka.quantities.electromagnetics.permittivity import Permittivity
    from kuchka.quantities.electromagnetics.resistance import Resistance
    from kuchka.quantities.electromagnetics.surface_charge_density import (
        SurfaceChargeDensity,
    )
    from kuchka.quantities.electromagnetics.voltage import Voltage
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class Conductance(LinearQuantity):
    """How readily a circuit element passes current: the reciprocal of Resistance."""

    dimension: ClassVar[Dimension] = CONDUCTANCE
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: ElectricFieldStrength) -> MagneticFieldStrength: ...
    @overload
    def __mul__(self, other: Inductance) -> Time: ...
    @overload
    def __mul__(self, other: MagneticFlux) -> Charge: ...
    @overload
    def __mul__(self, other: MagneticFluxDensity) -> SurfaceChargeDensity: ...
    @overload
    def __mul__(self, other: Proportion) -> Conductance: ...
    @overload
    def __mul__(self, other: Resistance) -> Fraction: ...
    @overload
    def __mul__(self, other: Time) -> Capacitance: ...
    @overload
    def __mul__(self, other: Voltage) -> Current: ...
    @overload
    def __mul__(self, other: Numeric) -> Conductance: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Capacitance) -> Frequency: ...
    @overload
    def __truediv__(self, other: Conductance) -> Proportion: ...
    @overload
    def __truediv__(self, other: Frequency) -> Capacitance: ...
    @overload
    def __truediv__(self, other: Permittivity) -> Velocity: ...
    @overload
    def __truediv__(self, other: Proportion) -> Conductance: ...
    @overload
    def __truediv__(self, other: Velocity) -> Permittivity: ...
    @overload
    def __truediv__(self, other: Numeric) -> Conductance: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)

    # BEGIN GENERATED __rtruediv__
    @overload
    def __rtruediv__(self, other: Numeric) -> Resistance: ...
    @overload
    def __rtruediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __rtruediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction:
        return super().__rtruediv__(other)


_register(CONDUCTANCE, Conductance)

__all__ = ["Conductance"]
