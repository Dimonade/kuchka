"""Time and Frequency, plus the domain vocabulary that shares their dimensions.

`Time` (T¹) and `Frequency` (T⁻¹) are the SI-general pair:
they are the types the dimension registry hands back for any arithmetic that produces
a plain span or a plain rate, the same role `Voltage` plays for M L² T⁻³ I⁻¹.

`Time` is a span: a sample period, a timeout, or a duration between two readings.
`.to_sampling_period()` and `.to_instant()` read that same span as a different kind of
quantity, at whatever prefix it was already constructed with:

    period = Microsecond(2).to_sampling_period()
    reading = Second(1_700_000_000).to_instant()

`Instant` is the point-in-time counterpart to `Time`, the same affine relationship
`Temperature` has to `TemperatureDelta`:

    later = reading + Second(42)   # -> Instant
    later - reading                # -> Time(42)

`SamplingPeriod` and `SampleRate` are specialisations of `Time` and `Frequency`, a
second pair sharing the same two dimensions:
a sample period genuinely is the reciprocal of a sample rate, so they convert into each
other directly, without going through `Frequency`.
`BaudRate` is a specialisation of `Frequency` too, with no reciprocal partner, and
therefore is not given one:
baud is a rate of symbols, not of bits or of seconds, so a default numeric equivalence
with `Frequency` would be right only by coincidence, for any signal encoding more or
less than one bit per symbol.

See `_DIMENSION_REGISTRY`'s docstring for why only `Time` and `Frequency` are the
principal kinds of their dimensions, and `LinearQuantity.__rtruediv__` for how
`1 / SamplingPeriod(...)` is kept from silently answering with the wrong sibling type.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Protocol
from typing import overload
from typing import runtime_checkable

from kuchka.dimensions import FREQUENCY
from kuchka.dimensions import TIME
from kuchka.internal.typing import override
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities.base import AffineQuantity
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register
from kuchka.quantities.base.registry import _register_reciprocal

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.quantities.amount import AmountOfSubstance
    from kuchka.quantities.angular import AngularDisplacement
    from kuchka.quantities.chemistry.entities_per_amount import EntitiesPerAmount
    from kuchka.quantities.chemistry.molar_flow_rate import MolarFlowRate
    from kuchka.quantities.current import Current
    from kuchka.quantities.electromagnetics.capacitance import Capacitance
    from kuchka.quantities.electromagnetics.charge import Charge
    from kuchka.quantities.electromagnetics.conductance import Conductance
    from kuchka.quantities.electromagnetics.inductance import Inductance
    from kuchka.quantities.electromagnetics.magnetic_flux import MagneticFlux
    from kuchka.quantities.electromagnetics.resistance import Resistance
    from kuchka.quantities.electromagnetics.voltage import Voltage
    from kuchka.quantities.geometry.volume import Volume
    from kuchka.quantities.information.data import Data
    from kuchka.quantities.information.data_rate import DataRate
    from kuchka.quantities.kinematics.acceleration import Acceleration
    from kuchka.quantities.kinematics.angular_velocity import AngularVelocity
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.length import Length
    from kuchka.quantities.mass import Mass
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.force import Force
    from kuchka.quantities.mechanics.impulse import Impulse
    from kuchka.quantities.mechanics.mass_flow_rate import MassFlowRate
    from kuchka.quantities.mechanics.momentum import Momentum
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.mechanics.volumetric_flow_rate import VolumetricFlowRate
    from kuchka.quantities.photometry.illuminance import Illuminance
    from kuchka.quantities.photometry.luminous_energy import LuminousEnergy
    from kuchka.quantities.photometry.luminous_exposure import LuminousExposure
    from kuchka.quantities.photometry.luminous_flux import LuminousFlux
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.thermal import TemperatureDelta
    from kuchka.quantities.thermodynamics.heating_rate import HeatingRate


class Time(LinearQuantity):
    """A span of time: a duration, a timeout, an interval between readings."""

    dimension: ClassVar[Dimension] = TIME
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Acceleration) -> Velocity: ...
    @overload
    def __mul__(self, other: AngularVelocity) -> AngularDisplacement: ...
    @overload
    def __mul__(self, other: Conductance) -> Capacitance: ...
    @overload
    def __mul__(self, other: Current) -> Charge: ...
    @overload
    def __mul__(self, other: DataRate) -> Data: ...
    @overload
    def __mul__(self, other: Force) -> Impulse: ...
    @overload
    def __mul__(self, other: Frequency) -> Fraction: ...
    @overload
    def __mul__(self, other: HeatingRate) -> TemperatureDelta: ...
    @overload
    def __mul__(self, other: Illuminance) -> LuminousExposure: ...
    @overload
    def __mul__(self, other: LuminousFlux) -> LuminousEnergy: ...
    @overload
    def __mul__(self, other: MassFlowRate) -> Mass: ...
    @overload
    def __mul__(self, other: MolarFlowRate) -> AmountOfSubstance: ...
    @overload
    def __mul__(self, other: Power) -> Energy: ...
    @overload
    def __mul__(self, other: Proportion) -> Time: ...
    @overload
    def __mul__(self, other: Resistance) -> Inductance: ...
    @overload
    def __mul__(self, other: Velocity) -> Length: ...
    @overload
    def __mul__(self, other: Voltage) -> MagneticFlux: ...
    @overload
    def __mul__(self, other: VolumetricFlowRate) -> Volume: ...
    @overload
    def __mul__(self, other: Numeric) -> Time: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Capacitance) -> Resistance: ...
    @overload
    def __truediv__(self, other: Conductance) -> Inductance: ...
    @overload
    def __truediv__(self, other: Inductance) -> Conductance: ...
    @overload
    def __truediv__(self, other: Proportion) -> Time: ...
    @overload
    def __truediv__(self, other: Resistance) -> Capacitance: ...
    @overload
    def __truediv__(self, other: Time) -> Proportion: ...
    @overload
    def __truediv__(self, other: Numeric) -> Time: ...
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
    def __rtruediv__(self, other: Numeric) -> Frequency: ...
    @overload
    def __rtruediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __rtruediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction:
        # NOTE: `Time` is the registered T¹ type, so the base implementation's
        # canonical-type guard passes and this reaches `Frequency` through
        # ordinary dimension algebra -- no override of the runtime logic needed, only
        # of the static signature.
        return super().__rtruediv__(other)

    def to_sampling_period(self) -> SamplingPeriod:
        """View a span as a `SamplingPeriod`, e.g. for use as `SampleRate` reciprocal.

            period = Millisecond(2).to_sampling_period()
            rate = 1 / period   # -> `SampleRate`

        `SamplingPeriod` shares `Time`'s own coordinate units.
        Display unit carries through.
        """
        return SamplingPeriod(self._magnitude, self._display_unit)

    def to_instant(self) -> Instant:
        """View this span as an `Instant` that many seconds from wherever zero is.

            reading = Second(1_700_000_000).to_instant()
            later = reading + Millisecond(500)   # -> Instant

        `Second`, `Millisecond`, `Microsecond`, `Minute`, and `Hour` all work here --
        `Hour(1).to_instant()` is the instant one hour past whatever the caller treats
        as zero, the same way `Kelvin(0)` is a `Temperature` reading, not a unit of
        its own.
        """
        return Instant(self._magnitude, Instant._canonical_unit)  # noqa: SLF001 -- Instant's own canonical unit


class Instant(AffineQuantity[Time]):
    """A point in time: a clock reading, a log timestamp, a sensor's capture moment.

        reading = Second(1_700_000_000).to_instant()
        later = reading + Second(42)
        elapsed = later - reading   # -> Time(42)

    Reached from any `Time` value via `.to_instant()`, at whatever prefix that value
    was already constructed with.
    Where the zero point of the scale falls is entirely up to the caller:
    an `Instant` carries no calendar of its own, the same way a `Temperature` carries
    no opinion about which planet it was measured on.
    """

    dimension: ClassVar[Dimension] = TIME
    _delta_type: ClassVar[type[LinearQuantity]] = Time
    _conversion_target_hint: ClassVar[str] = "a matching affine instant unit"
    __slots__ = ()


class Frequency(LinearQuantity):
    """A rate of repetition: cycles per second, in the ordinary physics sense."""

    dimension: ClassVar[Dimension] = FREQUENCY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: AmountOfSubstance) -> MolarFlowRate: ...
    @overload
    def __mul__(self, other: AngularDisplacement) -> AngularVelocity: ...
    @overload
    def __mul__(self, other: Capacitance) -> Conductance: ...
    @overload
    def __mul__(self, other: Charge) -> Current: ...
    @overload
    def __mul__(self, other: Data) -> DataRate: ...
    @overload
    def __mul__(self, other: Energy) -> Power: ...
    @overload
    def __mul__(self, other: Impulse) -> Force: ...
    @overload
    def __mul__(self, other: Inductance) -> Resistance: ...
    @overload
    def __mul__(self, other: Length) -> Velocity: ...
    @overload
    def __mul__(self, other: LuminousEnergy) -> LuminousFlux: ...
    @overload
    def __mul__(self, other: LuminousExposure) -> Illuminance: ...
    @overload
    def __mul__(self, other: MagneticFlux) -> Voltage: ...
    @overload
    def __mul__(self, other: Mass) -> MassFlowRate: ...
    @overload
    def __mul__(self, other: Momentum) -> Force: ...
    @overload
    def __mul__(self, other: Proportion) -> Frequency: ...
    @overload
    def __mul__(self, other: TemperatureDelta) -> HeatingRate: ...
    @overload
    def __mul__(self, other: Time) -> Fraction: ...
    @overload
    def __mul__(self, other: Velocity) -> Acceleration: ...
    @overload
    def __mul__(self, other: Volume) -> VolumetricFlowRate: ...
    @overload
    def __mul__(self, other: Numeric) -> Frequency: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: EntitiesPerAmount) -> MolarFlowRate: ...
    @overload
    def __truediv__(self, other: Frequency) -> Proportion: ...
    @overload
    def __truediv__(self, other: MolarFlowRate) -> EntitiesPerAmount: ...
    @overload
    def __truediv__(self, other: Proportion) -> Frequency: ...
    @overload
    def __truediv__(self, other: Numeric) -> Frequency: ...
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
    def __rtruediv__(self, other: Numeric) -> Time: ...
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

    def to_frequency(self) -> Frequency:
        """Return this value unchanged, as a `Frequency`.

        This identity conversion exists so that code written against
        `ConvertibleToFrequency` can call `.to_frequency()` on a `Frequency` the same
        way it would on a `SampleRate`, without a special case for the type that
        already is one.
        """
        return self

    def to_angular_velocity(self) -> AngularVelocity:
        """View these cycles per second as the angle swept per second by a rotation.

            Mains frequency as angular velocity: Hertz(50).to_angular_velocity()

        One hertz is one turn per second, which is two pi radians per second.
        """
        from kuchka.quantities.kinematics.angular_velocity import AngularVelocity  # noqa: PLC0415

        return AngularVelocity(self._magnitude, AngularVelocity._result_unit)  # noqa: SLF001 -- AngularVelocity's own units


@runtime_checkable
class ConvertibleToFrequency(Protocol):
    """Anything with a `to_frequency()` method.

    A `Frequency`, a `SampleRate`, and an `AngularVelocity` all have one.

    Intended for consumer-side type hints, e.g. a Nyquist check that should accept a
    `Frequency` or a `SampleRate` interchangeably:

        def nyquist_ok(signal: ConvertibleToFrequency, sample_rate: Frequency) -> bool:
            return signal.to_frequency() * 2 <= sample_rate

    `BaudRate` deliberately does not satisfy this protocol:
    see the module docstring for why it has no `to_frequency()` at all.
    """

    def to_frequency(self) -> Frequency:
        """Return this value's equivalent as a Frequency."""
        ...


class SamplingPeriod(LinearQuantity):
    """The interval between two samples, e.g. an ADC's per-reading spacing.

        period = Millisecond(2).to_sampling_period()
        rate = 1 / period   # -> SampleRate(500)

    Dimensionally identical to `Time`, and convertible to and from `SampleRate`
    directly (see the module docstring), but never produced by generic arithmetic:
    the only way to get one is `Time.to_sampling_period()`, the same way
    `Temperature` is never a side effect of ordinary arithmetic on other quantities.

    It scales by a plain number or a `Proportion`, divides by another `SamplingPeriod`
    into a `Proportion`, and multiplies with its reciprocal `SampleRate`.
    `to_time()` takes it as a `Time` for any other arithmetic.
    """

    dimension: ClassVar[Dimension] = TIME
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Proportion) -> SamplingPeriod: ...
    @overload
    def __mul__(self, other: SampleRate) -> Fraction: ...
    @overload
    def __mul__(self, other: Numeric) -> SamplingPeriod: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Proportion) -> SamplingPeriod: ...
    @overload
    def __truediv__(self, other: SamplingPeriod) -> Proportion: ...
    @overload
    def __truediv__(self, other: Numeric) -> SamplingPeriod: ...
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
    def __rtruediv__(self, other: Numeric) -> SampleRate: ...
    @overload
    def __rtruediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __rtruediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction:
        # NOTE: Overridden and not inherited:
        # `SamplingPeriod` is not the registered type for T¹ (`Time` is), so the base
        # implementation's canonical-type guard would refuse this and not risk handing
        # back the wrong sibling.
        #
        # `SamplingPeriod` and `SampleRate` are genuine reciprocals of each other
        # specifically, so that conversion is spelled out here directly instead.
        if isinstance(other, Numeric):
            magnitude = to_exact(other) / self._magnitude
            return SampleRate(magnitude, SampleRate._canonical_unit)
        return NotImplemented

    def to_time(self) -> Time:
        """View this interval as an ordinary `Time`, e.g. to multiply it by a speed.

            Millisecond(2).to_sampling_period().to_time() == Millisecond(2)

        The unit it displays in carries over, and `Time.to_sampling_period()` takes
        the value back.
        """
        return Time(self._magnitude, self._display_unit)


class SampleRate(LinearQuantity):
    """How often an acquisition system takes a reading, e.g. an ADC's sample rate.

    Dimensionally identical to `Frequency`, and convertible to and from
    `SamplingPeriod` directly, but never produced by generic arithmetic:
    see the `SamplingPeriod` docstring for why.

    It scales by a plain number or a `Proportion`, divides by another `SampleRate`
    into a `Proportion`, and multiplies with its reciprocal `SamplingPeriod`.
    `to_frequency()` takes it as a `Frequency` for any other arithmetic.
    """

    dimension: ClassVar[Dimension] = FREQUENCY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Proportion) -> SampleRate: ...
    @overload
    def __mul__(self, other: SamplingPeriod) -> Fraction: ...
    @overload
    def __mul__(self, other: Numeric) -> SampleRate: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Proportion) -> SampleRate: ...
    @overload
    def __truediv__(self, other: SampleRate) -> Proportion: ...
    @overload
    def __truediv__(self, other: Numeric) -> SampleRate: ...
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
    def __rtruediv__(self, other: Numeric) -> SamplingPeriod: ...
    @overload
    def __rtruediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __rtruediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction:
        if isinstance(other, Numeric):
            magnitude = to_exact(other) / self._magnitude
            return SamplingPeriod(magnitude, SamplingPeriod._canonical_unit)
        return NotImplemented

    def to_frequency(self) -> Frequency:
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

    It is deliberately given no reciprocal and no `to_frequency()` -- neither is a
    well-defined, encoding-independent conversion, and a wrong default here would be
    wrong silently.

    It scales by a plain number or a `Proportion`, and divides by another `BaudRate`
    into a `Proportion`.
    """

    dimension: ClassVar[Dimension] = FREQUENCY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Proportion) -> BaudRate: ...
    @overload
    def __mul__(self, other: Numeric) -> BaudRate: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: BaudRate) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> BaudRate: ...
    @overload
    def __truediv__(self, other: Numeric) -> BaudRate: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(TIME, Time)
_register(FREQUENCY, Frequency)
_register(TIME, SamplingPeriod, specialisation_of=Time)
_register(FREQUENCY, SampleRate, specialisation_of=Frequency)
_register(FREQUENCY, BaudRate, specialisation_of=Frequency)
_register_reciprocal(SamplingPeriod, SampleRate)
_register(TIME, Instant)

__all__ = [
    "BaudRate",
    "ConvertibleToFrequency",
    "Frequency",
    "Instant",
    "SampleRate",
    "SamplingPeriod",
    "Time",
]
