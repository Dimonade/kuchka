"""LinearChargeDensity: the electric charge along a line: charge per length."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import LINEAR_CHARGE_DENSITY
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
    from kuchka.quantities.electromagnetics.magnetic_field_strength import (
        MagneticFieldStrength,
    )
    from kuchka.quantities.electromagnetics.magnetic_flux_density import (
        MagneticFluxDensity,
    )
    from kuchka.quantities.electromagnetics.permittivity import Permittivity
    from kuchka.quantities.electromagnetics.surface_charge_density import (
        SurfaceChargeDensity,
    )
    from kuchka.quantities.electromagnetics.voltage import Voltage
    from kuchka.quantities.electromagnetics.volume_charge_density import (
        VolumeChargeDensity,
    )
    from kuchka.quantities.geometry.area import Area
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.length import Length
    from kuchka.quantities.mechanics.dynamic_viscosity import DynamicViscosity
    from kuchka.quantities.mechanics.force import Force
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class LinearChargeDensity(LinearQuantity):
    """The electric charge along a line: charge per length."""

    dimension: ClassVar[Dimension] = LINEAR_CHARGE_DENSITY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Frequency) -> MagneticFieldStrength: ...
    @overload
    def __mul__(self, other: Length) -> Charge: ...
    @overload
    def __mul__(self, other: MagneticFluxDensity) -> DynamicViscosity: ...
    @overload
    def __mul__(self, other: Proportion) -> LinearChargeDensity: ...
    @overload
    def __mul__(self, other: Velocity) -> Current: ...
    @overload
    def __mul__(self, other: Voltage) -> Force: ...
    @overload
    def __mul__(self, other: Numeric) -> LinearChargeDensity: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Area) -> VolumeChargeDensity: ...
    @overload
    def __truediv__(self, other: Capacitance) -> ElectricFieldStrength: ...
    @overload
    def __truediv__(self, other: ElectricFieldStrength) -> Capacitance: ...
    @overload
    def __truediv__(self, other: Length) -> SurfaceChargeDensity: ...
    @overload
    def __truediv__(self, other: LinearChargeDensity) -> Proportion: ...
    @overload
    def __truediv__(self, other: MagneticFieldStrength) -> Time: ...
    @overload
    def __truediv__(self, other: Permittivity) -> Voltage: ...
    @overload
    def __truediv__(self, other: Proportion) -> LinearChargeDensity: ...
    @overload
    def __truediv__(self, other: SurfaceChargeDensity) -> Length: ...
    @overload
    def __truediv__(self, other: Time) -> MagneticFieldStrength: ...
    @overload
    def __truediv__(self, other: Voltage) -> Permittivity: ...
    @overload
    def __truediv__(self, other: VolumeChargeDensity) -> Area: ...
    @overload
    def __truediv__(self, other: Numeric) -> LinearChargeDensity: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(LINEAR_CHARGE_DENSITY, LinearChargeDensity)

__all__ = ["LinearChargeDensity"]
