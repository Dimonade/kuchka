"""Time and Frequency, plus the domain vocabulary that shares their dimensions.

`Time` (T^1) and `Frequency` (T^-1) are the SI-general pair:
they are the types the dimension registry hands back for any arithmetic that produces
a plain span or a plain rate, the same role `Voltage` plays for M L^2 T^-3 I^-1.

`Time` is deliberately a span, not a point in time:
a sample period, a timeout, or a duration between two readings all fit it.
A point-in-time reading (a timestamp) would need the same affine treatment
`Temperature` gets -- a distinct type, most likely `Instant`, with its own
"you cannot add two timestamps" rule -- and is left unmodelled until something in the
vocabulary actually needs it.

`SamplingPeriod` and `SampleRate` are a second, unregistered pair sharing the same two
dimensions:
a sample period genuinely is the reciprocal of a sample rate, so they convert into each
other directly, without going through `Frequency`.
`BaudRate` also shares `Frequency`'s dimension but is not its reciprocal partner, and
therefore, is not given one:
baud is a rate of symbols, not of bits or of seconds, so a default numeric equivalence
with `Frequency` would be right only by coincidence, for any signal encoding more or
less than one bit per symbol.

See `_DIMENSION_REGISTRY`'s docstring for why only `Time` and `Frequency` are
registered here, and `LinearQuantity.__rtruediv__` for how `1 / SamplingPeriod(...)`
is kept from silently answering with the wrong sibling type.
"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from typing import ClassVar
from typing import overload
from typing import Protocol
from typing import runtime_checkable
from typing import TYPE_CHECKING

from kuchka.dimensions import FREQUENCY
from kuchka.dimensions import TIME
from kuchka.numeric import to_decimal
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base import register

if TYPE_CHECKING:
    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.charge import Charge
    from kuchka.quantities.electrical import Current
    from kuchka.quantities.electrical import Power
    from kuchka.quantities.energy import Energy
    from kuchka.quantities.kinematics import Velocity
    from kuchka.quantities.length import Length

_NUMERIC_TYPES = (int, float, Decimal, Fraction)


class Time(LinearQuantity):
    """A span of time: a duration, a timeout, an interval between readings."""

    dimension: ClassVar[Dimension] = TIME

    @overload
    def __mul__(self, other: Frequency) -> Decimal: ...
    @overload
    def __mul__(self, other: Current) -> Charge: ...
    @overload
    def __mul__(self, other: Power) -> Energy: ...
    @overload
    def __mul__(self, other: Velocity) -> Length: ...
    @overload
    def __mul__(self, other: Numeric) -> Time: ...
    @overload
    def __mul__(self, other: object) -> LinearQuantity | Decimal: ...

    def __mul__(self, other: object) -> LinearQuantity | Decimal:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: Numeric) -> Time: ...
    @overload
    def __truediv__(self, other: object) -> LinearQuantity | Decimal: ...

    def __truediv__(self, other: object) -> LinearQuantity | Decimal:
        return super().__truediv__(other)

    @overload
    def __rtruediv__(self, other: Numeric) -> Frequency: ...
    @overload
    def __rtruediv__(self, other: object) -> LinearQuantity | Decimal: ...

    def __rtruediv__(self, other: object) -> LinearQuantity | Decimal:
        # NOTE: `Time` is the registered T^1 type, so the base implementation's
        # canonical-type guard passes and this reaches `Frequency` through
        # ordinary dimension algebra -- no override of the runtime logic needed, only
        # of the static signature.
        return super().__rtruediv__(other)


class Frequency(LinearQuantity):
    """A rate of repetition: cycles per second, in the ordinary physics sense."""

    dimension: ClassVar[Dimension] = FREQUENCY

    @overload
    def __mul__(self, other: Time) -> Decimal: ...
    @overload
    def __mul__(self, other: Numeric) -> Frequency: ...
    @overload
    def __mul__(self, other: object) -> LinearQuantity | Decimal: ...

    def __mul__(self, other: object) -> LinearQuantity | Decimal:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: Numeric) -> Frequency: ...
    @overload
    def __truediv__(self, other: object) -> LinearQuantity | Decimal: ...

    def __truediv__(self, other: object) -> LinearQuantity | Decimal:
        return super().__truediv__(other)

    @overload
    def __rtruediv__(self, other: Numeric) -> Time: ...
    @overload
    def __rtruediv__(self, other: object) -> LinearQuantity | Decimal: ...

    def __rtruediv__(self, other: object) -> LinearQuantity | Decimal:
        return super().__rtruediv__(other)

    def as_frequency(self) -> Frequency:
        """Return this value unchanged, as a `Frequency`.

        This identity conversion exists so that code written against
        `ConvertibleToFrequency` can call `.as_frequency()` on a `Frequency` the same
        way it would on a `SampleRate`, without a special case for the type that
        already is one.
        """
        return self


@runtime_checkable
class ConvertibleToFrequency(Protocol):
    """Anything with an `as_frequency()` method: a Frequency or a SampleRate.

    Intended for consumer-side type hints, e.g. a Nyquist check that should accept a
    `Frequency` or a `SampleRate` interchangeably:

        def nyquist_ok(signal: ConvertibleToFrequency, sample_rate: Frequency) -> bool:
            return signal.as_frequency() * 2 <= sample_rate

    `BaudRate` deliberately does not satisfy this protocol:
    see the module docstring for why it has no `as_frequency()` at all.
    """

    def as_frequency(self) -> Frequency:
        """Return this value's equivalent as a Frequency."""
        ...


class SamplingPeriod(LinearQuantity):
    """The interval between two samples, e.g. an ADC's per-reading spacing.

    Dimensionally identical to `Time`, and convertible to and from `SampleRate`
    directly (see the module docstring), but never produced by generic arithmetic:
    the only way to get one is to construct it explicitly, the same way `Temperature`
    is never a side effect of ordinary arithmetic on other quantities.
    """

    dimension: ClassVar[Dimension] = TIME

    @overload
    def __mul__(self, other: SampleRate) -> Decimal: ...
    @overload
    def __mul__(self, other: Numeric) -> SamplingPeriod: ...
    @overload
    def __mul__(self, other: object) -> LinearQuantity | Decimal: ...

    def __mul__(self, other: object) -> LinearQuantity | Decimal:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: Numeric) -> SamplingPeriod: ...
    @overload
    def __truediv__(self, other: object) -> LinearQuantity | Decimal: ...

    def __truediv__(self, other: object) -> LinearQuantity | Decimal:
        return super().__truediv__(other)

    @overload
    def __rtruediv__(self, other: Numeric) -> SampleRate: ...
    @overload
    def __rtruediv__(self, other: object) -> LinearQuantity | Decimal: ...

    def __rtruediv__(self, other: object) -> LinearQuantity | Decimal:
        # NOTE: Overridden and not inherited:
        # `SamplingPeriod` is not the registered type for T^1 (`Time` is), so the base
        # implementation's canonical-type guard would refuse this and not risk handing
        # back the wrong sibling.
        #
        # `SamplingPeriod` and `SampleRate` are genuine reciprocals of each other
        # specifically, so that conversion is spelled out here directly instead.
        if isinstance(other, _NUMERIC_TYPES):
            magnitude = to_decimal(other) / self._magnitude
            return SampleRate(magnitude, SampleRate._canonical_unit)
        return NotImplemented


class SampleRate(LinearQuantity):
    """How often an acquisition system takes a reading, e.g. an ADC's sample rate.

    Dimensionally identical to `Frequency`, and convertible to and from
    `SamplingPeriod` directly, but never produced by generic arithmetic:
    see the `SamplingPeriod` docstring for why.
    """

    dimension: ClassVar[Dimension] = FREQUENCY

    @overload
    def __mul__(self, other: SamplingPeriod) -> Decimal: ...
    @overload
    def __mul__(self, other: Numeric) -> SampleRate: ...
    @overload
    def __mul__(self, other: object) -> LinearQuantity | Decimal: ...

    def __mul__(self, other: object) -> LinearQuantity | Decimal:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: Numeric) -> SampleRate: ...
    @overload
    def __truediv__(self, other: object) -> LinearQuantity | Decimal: ...

    def __truediv__(self, other: object) -> LinearQuantity | Decimal:
        return super().__truediv__(other)

    @overload
    def __rtruediv__(self, other: Numeric) -> SamplingPeriod: ...
    @overload
    def __rtruediv__(self, other: object) -> LinearQuantity | Decimal: ...

    def __rtruediv__(self, other: object) -> LinearQuantity | Decimal:
        if isinstance(other, _NUMERIC_TYPES):
            magnitude = to_decimal(other) / self._magnitude
            return SamplingPeriod(magnitude, SamplingPeriod._canonical_unit)
        return NotImplemented

    def as_frequency(self) -> Frequency:
        """View this sample rate as an ordinary Frequency, e.g. for a Nyquist check.

        This is a one-way, explicit door: nothing on `Frequency` converts back into a
        `SampleRate`, since a bare frequency carries no information about which
        acquisition system it came from.
        """
        return Frequency(self._magnitude, Frequency._canonical_unit)  # noqa: SLF001 -- Frequency's own canonical unit


class BaudRate(LinearQuantity):
    """A symbol rate, e.g. a UART's configured baud rate.

    Dimensionally identical to `Frequency`, but not interchangeable with it or with
    `SampleRate`:
    baud counts symbols per second, not bits or cycles, so it is not a `Frequency` in
    disguise the way `SampleRate` is a `Frequency`-shaped concept restricted to
    acquisition.

    It is deliberately given no reciprocal and no `as_frequency()` -- neither is a
    well-defined, encoding-independent conversion, and a wrong default here would be
    wrong silently.
    """

    dimension: ClassVar[Dimension] = FREQUENCY

    @overload
    def __mul__(self, other: Numeric) -> BaudRate: ...
    @overload
    def __mul__(self, other: object) -> LinearQuantity | Decimal: ...

    def __mul__(self, other: object) -> LinearQuantity | Decimal:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: Numeric) -> BaudRate: ...
    @overload
    def __truediv__(self, other: object) -> LinearQuantity | Decimal: ...

    def __truediv__(self, other: object) -> LinearQuantity | Decimal:
        return super().__truediv__(other)


register(TIME, Time)
register(FREQUENCY, Frequency)

__all__ = [
    "BaudRate",
    "ConvertibleToFrequency",
    "Frequency",
    "SampleRate",
    "SamplingPeriod",
    "Time",
]
