"""TemperatureDelta and Temperature: linear and affine parts of thermal measurement.

A gap of N degrees can be added, subtracted, and scaled the same way a voltage or a
current can: "the gap doubled" is physically meaningful in a way "the temperature
doubled" is not.
That is what makes :class:`TemperatureDelta` an ordinary
:class:`~kuchka.quantities.base.LinearQuantity`, sitting alongside Voltage and Current,
while :class:`Temperature` is a :class:`~kuchka.quantities.base.AffineQuantity`
instead -- see that class's docstring for the operations a point on a scale supports
and the ones it deliberately omits, and why.

This module treats Celsius and Kelvin identically:
both construct the same ``Temperature`` type, and neither supports scalar
multiplication, even though "2 x 300 K" has a defensible thermodynamic reading that
"2 x 20 degC" does not.
Giving Kelvin its own multiplicable type would be a reasonable extension for a use case
built around thermodynamic scaling, but it is out of scope for the device-engineering
vocabulary this library currently targets.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar

from kuchka.dimensions import TEMPERATURE_DELTA
from kuchka.quantities.base import AffineQuantity
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base import register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension


class TemperatureDelta(LinearQuantity):
    """A difference between two temperatures, e.g. a tolerance band."""

    dimension: ClassVar[Dimension] = TEMPERATURE_DELTA


register(TEMPERATURE_DELTA, TemperatureDelta)


class Temperature(AffineQuantity[TemperatureDelta]):
    """An absolute thermodynamic temperature reading.

    Supports the operations that are physically meaningful for a point on an affine
    scale: comparison, subtracting another ``Temperature`` to get a
    ``TemperatureDelta``, and shifting by a ``TemperatureDelta``.

    See :class:`~kuchka.quantities.base.AffineQuantity` for the operations this
    deliberately omits, and why. `__add__`/`__sub__` are not restated here at all --
    parametrizing `AffineQuantity` with `TemperatureDelta` above is what gives this
    class its precise arithmetic signature (`TemperatureDelta -> Temperature`,
    `Temperature -> TemperatureDelta`) by inheritance alone.
    """

    dimension: ClassVar[Dimension] = TEMPERATURE_DELTA
    _delta_type: ClassVar[type[LinearQuantity]] = TemperatureDelta
    _conversion_target_hint: ClassVar[str] = (
        "a temperature unit such as Kelvin or Celsius"
    )
    __slots__ = ()

    @property
    def kelvin(self) -> Fraction:
        """Magnitude expressed in Kelvin, this type's canonical unit."""
        return self._magnitude


__all__ = ["Temperature", "TemperatureDelta"]
