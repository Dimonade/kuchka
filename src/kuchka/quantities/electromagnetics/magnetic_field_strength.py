"""Magnetic field strength and magnetization: the two readings of an ampere per metre.

`Magnetization` is a role of `MagneticFieldStrength`: the same dimension, read as the
magnetic response of a material and not as the field applied to it.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import MAGNETIC_FIELD_STRENGTH
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register
from kuchka.quantities.base.registry import _rule
from kuchka.quantities.electromagnetics.magnetic_flux_density import MagneticFluxDensity
from kuchka.quantities.mechanics.energy_density import EnergyDensity

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.current import Current
    from kuchka.quantities.electromagnetics.magnetic_flux import MagneticFlux
    from kuchka.quantities.electromagnetics.permeability import Permeability
    from kuchka.quantities.length import Length
    from kuchka.quantities.mechanics.force import Force
    from kuchka.quantities.proportion import Proportion


class MagneticFieldStrength(LinearQuantity):
    """The magnetising field, H: the part of a magnetic field due to free currents.

    Current per length, and the field that relates to flux density as `B = μH` in a
    linear medium.
    `to_magnetization()` reads it as a `Magnetization`.
    `MagneticFluxDensity * MagneticFieldStrength` is an `EnergyDensity`, the product
    `B·H`: the energy stored in a linear medium is half of it, `w = B·H / 2`.
    """

    dimension: ClassVar[Dimension] = MAGNETIC_FIELD_STRENGTH
    __slots__ = ()

    def to_magnetization(self) -> Magnetization:
        """View this field strength as a `Magnetization`.

        The unit it displays in carries over, and
        `Magnetization.to_magnetic_field_strength()` takes the value back.
        """
        return Magnetization(self._magnitude, self._display_unit)

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Length) -> Current: ...
    @overload
    def __mul__(self, other: MagneticFlux) -> Force: ...
    @overload
    def __mul__(self, other: MagneticFluxDensity) -> EnergyDensity: ...
    @overload
    def __mul__(self, other: Permeability) -> MagneticFluxDensity: ...
    @overload
    def __mul__(self, other: Proportion) -> MagneticFieldStrength: ...
    @overload
    def __mul__(self, other: Numeric) -> MagneticFieldStrength: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: MagneticFieldStrength) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> MagneticFieldStrength: ...
    @overload
    def __truediv__(self, other: Numeric) -> MagneticFieldStrength: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


class Magnetization(LinearQuantity):
    """The magnetic dipole moment per unit volume of a material, M.

    Dimensionally identical to `MagneticFieldStrength`: the material's response to an
    applied field, where `B = μ0(H + M)`.
    `to_magnetic_field_strength()` takes it as a `MagneticFieldStrength` to add it to an
    applied field or to scale it by a permeability.
    """

    dimension: ClassVar[Dimension] = MAGNETIC_FIELD_STRENGTH
    __slots__ = ()

    def to_magnetic_field_strength(self) -> MagneticFieldStrength:
        """View this magnetization as a `MagneticFieldStrength`.

        The unit it displays in carries over, and
        `MagneticFieldStrength.to_magnetization()` takes the value back.
        """
        return MagneticFieldStrength(self._magnitude, self._display_unit)

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Proportion) -> Magnetization: ...
    @overload
    def __mul__(self, other: Numeric) -> Magnetization: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Magnetization) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> Magnetization: ...
    @overload
    def __truediv__(self, other: Numeric) -> Magnetization: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(MAGNETIC_FIELD_STRENGTH, MagneticFieldStrength)
_register(
    MAGNETIC_FIELD_STRENGTH, Magnetization, specialisation_of=MagneticFieldStrength
)

_rule(MagneticFluxDensity, "*", MagneticFieldStrength, EnergyDensity)

__all__ = ["MagneticFieldStrength", "Magnetization"]
