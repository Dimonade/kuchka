"""Resistance, Reactance, and Impedance: opposition to current flow.

`Reactance` and `Impedance` are roles of `Resistance`: the same dimension, read as the
opposition of a reactive element and of a whole circuit to alternating current.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import RESISTANCE
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
    from kuchka.quantities.electromagnetics.conductance import Conductance
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
    from kuchka.quantities.electromagnetics.permeability import Permeability
    from kuchka.quantities.electromagnetics.surface_charge_density import (
        SurfaceChargeDensity,
    )
    from kuchka.quantities.electromagnetics.voltage import Voltage
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class Resistance(LinearQuantity):
    """The opposition a circuit element presents to current flow."""

    dimension: ClassVar[Dimension] = RESISTANCE
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Capacitance) -> Time: ...
    @overload
    def __mul__(self, other: Charge) -> MagneticFlux: ...
    @overload
    def __mul__(self, other: Conductance) -> Fraction: ...
    @overload
    def __mul__(self, other: Current) -> Voltage: ...
    @overload
    def __mul__(self, other: MagneticFieldStrength) -> ElectricFieldStrength: ...
    @overload
    def __mul__(self, other: Proportion) -> Resistance: ...
    @overload
    def __mul__(self, other: SurfaceChargeDensity) -> MagneticFluxDensity: ...
    @overload
    def __mul__(self, other: Time) -> Inductance: ...
    @overload
    def __mul__(self, other: Numeric) -> Resistance: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __rtruediv__
    @overload
    def __rtruediv__(self, other: Numeric) -> Conductance: ...
    @overload
    def __rtruediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __rtruediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction:
        # NOTE: `Resistance` is the registered canonical type for `RESISTANCE`, so the
        # base implementation's canonical-type guard passes and this reaches
        # `Conductance` through ordinary dimension algebra -- no override of the
        # runtime logic needed, only of the static signature (see `Time.__rtruediv__`
        # for the same pattern with Frequency).
        return super().__rtruediv__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Frequency) -> Inductance: ...
    @overload
    def __truediv__(self, other: Inductance) -> Frequency: ...
    @overload
    def __truediv__(self, other: Permeability) -> Velocity: ...
    @overload
    def __truediv__(self, other: Proportion) -> Resistance: ...
    @overload
    def __truediv__(self, other: Resistance) -> Proportion: ...
    @overload
    def __truediv__(self, other: Velocity) -> Permeability: ...
    @overload
    def __truediv__(self, other: Numeric) -> Resistance: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)

    def to_reactance(self) -> Reactance:
        """View this resistance as a `Reactance`.

        The unit it displays in carries over, and `Reactance.to_resistance()` takes the
        value back.
        """
        return Reactance(self._magnitude, self._display_unit)

    def to_impedance(self) -> Impedance:
        """View this resistance as an `Impedance`.

        The unit it displays in carries over, and `Impedance.to_resistance()` takes the
        value back.
        """
        return Impedance(self._magnitude, self._display_unit)


class Reactance(LinearQuantity):
    """The opposition of an inductor or a capacitor to alternating current.

    Dimensionally identical to `Resistance`, and signed: positive for an inductive
    element and negative for a capacitive one.
    `to_resistance()` takes it as a `Resistance` for any other arithmetic.
    """

    dimension: ClassVar[Dimension] = RESISTANCE
    __slots__ = ()

    def to_resistance(self) -> Resistance:
        """View this reactance as an ordinary `Resistance`.

        The unit it displays in carries over, and `Resistance.to_reactance()` takes the
        value back.
        """
        return Resistance(self._magnitude, self._display_unit)

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Proportion) -> Reactance: ...
    @overload
    def __mul__(self, other: Numeric) -> Reactance: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Proportion) -> Reactance: ...
    @overload
    def __truediv__(self, other: Reactance) -> Proportion: ...
    @overload
    def __truediv__(self, other: Numeric) -> Reactance: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


class Impedance(LinearQuantity):
    """The total opposition of a circuit to alternating current, as a magnitude.

    Dimensionally identical to `Resistance`.
    `to_resistance()` takes it as a `Resistance` for any other arithmetic.
    """

    dimension: ClassVar[Dimension] = RESISTANCE
    __slots__ = ()

    def to_resistance(self) -> Resistance:
        """View this impedance as an ordinary `Resistance`.

        The unit it displays in carries over, and `Resistance.to_impedance()` takes the
        value back.
        """
        return Resistance(self._magnitude, self._display_unit)

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Proportion) -> Impedance: ...
    @overload
    def __mul__(self, other: Numeric) -> Impedance: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Impedance) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> Impedance: ...
    @overload
    def __truediv__(self, other: Numeric) -> Impedance: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(RESISTANCE, Resistance)
_register(RESISTANCE, Reactance, specialisation_of=Resistance)
_register(RESISTANCE, Impedance, specialisation_of=Resistance)

__all__ = ["Impedance", "Reactance", "Resistance"]
