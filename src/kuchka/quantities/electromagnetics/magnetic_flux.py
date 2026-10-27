"""Magnetic flux: the magnetic field integrated over a surface."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import MAGNETIC_FLUX
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.current import Current
    from kuchka.quantities.electromagnetics.charge import Charge
    from kuchka.quantities.electromagnetics.conductance import Conductance
    from kuchka.quantities.electromagnetics.inductance import Inductance
    from kuchka.quantities.electromagnetics.magnetic_flux_density import (
        MagneticFluxDensity,
    )
    from kuchka.quantities.electromagnetics.resistance import Resistance
    from kuchka.quantities.electromagnetics.voltage import Voltage
    from kuchka.quantities.geometry.area import Area
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class MagneticFlux(LinearQuantity):
    """The magnetic field integrated over a surface: the flux linking a circuit."""

    dimension: ClassVar[Dimension] = MAGNETIC_FLUX
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Conductance) -> Charge: ...
    @overload
    def __mul__(self, other: Current) -> Energy: ...
    @overload
    def __mul__(self, other: Frequency) -> Voltage: ...
    @overload
    def __mul__(self, other: Proportion) -> MagneticFlux: ...
    @overload
    def __mul__(self, other: Numeric) -> MagneticFlux: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Area) -> MagneticFluxDensity: ...
    @overload
    def __truediv__(self, other: Charge) -> Resistance: ...
    @overload
    def __truediv__(self, other: Current) -> Inductance: ...
    @overload
    def __truediv__(self, other: Inductance) -> Current: ...
    @overload
    def __truediv__(self, other: MagneticFlux) -> Proportion: ...
    @overload
    def __truediv__(self, other: MagneticFluxDensity) -> Area: ...
    @overload
    def __truediv__(self, other: Proportion) -> MagneticFlux: ...
    @overload
    def __truediv__(self, other: Resistance) -> Charge: ...
    @overload
    def __truediv__(self, other: Time) -> Voltage: ...
    @overload
    def __truediv__(self, other: Voltage) -> Time: ...
    @overload
    def __truediv__(self, other: Numeric) -> MagneticFlux: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(MAGNETIC_FLUX, MagneticFlux)

__all__ = ["MagneticFlux"]
