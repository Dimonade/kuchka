"""LogarithmicRatio: a ratio of two like quantities, expressed in decibels.

A gain, an attenuation, a signal-to-noise ratio, an isolation: any ratio that
engineers quote on a logarithmic scale.
The decibel is the canonical unit.
See `kuchka.units.logarithmic` for the unit constructors and worked examples.

A level converts to the linear ratio it describes in two flavours, because the same
number of decibels stands for a different ratio depending on the kind of quantity:

* power quantities (power, energy, intensity): ``ratio = 10 ** (level / 10)``;
* field quantities (voltage, current, pressure): ``ratio = 10 ** (level / 20)``.

Levels combine, scale, and compare exactly.
Converting to or from a linear ratio is the one place a logarithm is evaluated:
it runs in `Decimal` at the active context precision and the result is stored as the
exact `Fraction` of that `Decimal`.
A level that is a whole multiple of the flavour's divisor (10 dB or 20 dB) converts
exactly, since the result is an exact power of ten.
"""

from __future__ import annotations

from decimal import Decimal
from decimal import Overflow
from fractions import Fraction
from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Self

from kuchka.dimensions import DIMENSIONLESS
from kuchka.errors import InvalidMeasurementError
from kuchka.numeric import to_decimal
from kuchka.numeric import to_exact
from kuchka.quantities.base import PureLogarithmicQuantity
from kuchka.quantities.base.registry import _register
from kuchka.quantities.proportion import Proportion

if TYPE_CHECKING:
    from kuchka.dimensions import Dimension

_POWER_DIVISOR = Fraction(10)
_FIELD_DIVISOR = Fraction(20)


def _linear_ratio(level: Fraction, divisor: Fraction) -> Proportion:
    """Evaluate ``10 ** (level / divisor)`` as a `Proportion`."""
    exponent = to_decimal(level / divisor)
    msg = (
        f"cannot express a level of {float(level)} dB as a linear ratio: "
        "the ratio is outside the range `Decimal` can represent."
    )
    try:
        ratio = Decimal(10) ** exponent
    except Overflow as exc:
        raise InvalidMeasurementError(msg) from exc
    if ratio == 0:
        raise InvalidMeasurementError(msg)
    return Proportion(to_exact(ratio), Proportion._canonical_unit)  # noqa: SLF001 -- Proportion's own canonical unit


def _level_of(ratio: Proportion, divisor: Fraction) -> Fraction:
    """Evaluate ``divisor * log10(ratio)`` in decibels."""
    value = ratio.magnitude
    if value <= 0:
        msg = (
            f"cannot express a ratio of {float(value)} logarithmically: "
            "only a positive ratio has a logarithm."
        )
        raise InvalidMeasurementError(msg)
    return to_exact(to_decimal(value).log10()) * divisor


class LogarithmicRatio(PureLogarithmicQuantity):
    """A ratio of two like quantities, expressed in decibels.

    Supports the arithmetic of `PureLogarithmicQuantity`, plus conversion to and from
    the linear ratio a level describes, as a `Proportion`.
    """

    dimension: ClassVar[Dimension] = DIMENSIONLESS
    __slots__ = ()

    def as_power_ratio(self) -> Proportion:
        """Return the linear ratio of two power quantities this level describes.

        ``Decibel(30).as_power_ratio() == Ratio(1000)``.
        """
        return _linear_ratio(self._magnitude, _POWER_DIVISOR)

    def as_field_ratio(self) -> Proportion:
        """Return the linear ratio of two field quantities this level describes.

        ``Decibel(40).as_field_ratio() == Ratio(100)``.
        """
        return _linear_ratio(self._magnitude, _FIELD_DIVISOR)

    @classmethod
    def from_power_ratio(cls, ratio: Proportion) -> Self:
        """Return the level, in decibels, of a ratio of two power quantities.

        ``LogarithmicRatio.from_power_ratio(Ratio(1000)) == Decibel(30)``.
        The ratio must be positive.
        """
        return cls(_level_of(ratio, _POWER_DIVISOR), cls._canonical_unit)

    @classmethod
    def from_field_ratio(cls, ratio: Proportion) -> Self:
        """Return the level, in decibels, of a ratio of two field quantities.

        ``LogarithmicRatio.from_field_ratio(Ratio(100)) == Decibel(40)``.
        The ratio must be positive.
        """
        return cls(_level_of(ratio, _FIELD_DIVISOR), cls._canonical_unit)


_register(DIMENSIONLESS, LogarithmicRatio)

__all__ = ["LogarithmicRatio"]
