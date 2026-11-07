"""Dimensional analysis primitives.

This module is internal machinery.
Ordinary users of the library never construct a :class:`Dimension` directly,
as they use the named engineering types (``Voltage``, ``Current``, ...),
and unit constructors (``Volt``, ``Milliampere``, ...) exposed from the top-level.

Dimensions are represented as exponent vectors over the seven SI base quantities:
mass, length, time, electric current, thermodynamic temperature, amount of substance,
and luminous intensity -- plus three supplementary axes, ``angle``, ``solid_angle`` and
``information``, tracked separately from the seven base quantities.

SI itself treats plane angle as a quantity of dimension one (the radian is a
dimensionless derived unit), and `kuchka` is not taking a position against that.
The ``angle`` field makes :data:`ANGLE` and :data:`DIMENSIONLESS` distinct ``Dimension``
values, and it takes part in arithmetic like any other axis.
Torque is energy per angle (M L² T⁻² angle⁻¹) and angular velocity is angle per time
(angle T⁻¹), so both differ from energy and from the hertz, which SI's own
base-quantity accounting cannot tell apart.
`Proportion` (genuinely dimensionless, ``Percent``/``Ratio``) and angles are different
dimensions for the same reason.

The ``solid_angle`` field does the same for the steradian, which SI also treats as a
dimensionless derived unit (a square metre per square metre).
It is an axis of its own and not the square of the angle axis, because a solid angle
is not the product of two plane angles.
Luminous flux is luminous intensity times solid angle (J solid_angle), so the lumen
differs from the candela, and illuminance is flux per area.

The ``information`` field does the same for data: a count of bits is neither a
`Proportion` nor a number of cycles.
A data rate is information per time (information T⁻¹), so it differs from the hertz,
the sample rate, and the baud, which all have the dimension T⁻¹.

Multiplying two physical quantities adds their exponent vectors.
Dividing subtracts them.
This gives the arithmetic engine a single general mechanism for deriving compound
dimensions (Power from Voltage * Current, Resistance from Voltage / Current, and so on),
instead of a hand-written table of every possible pairwise combination.
"""

from __future__ import annotations

from dataclasses import dataclass

from kuchka.internal import symbols
from kuchka.internal.symbols import get_superscript
from kuchka.internal.typing import override


@dataclass(frozen=True, slots=True)
class Dimension:
    """An exponent vector over the SI base dimensions used by this library.

    Two ``Dimension`` instances compare equal (and hash equal) exactly when every
    exponent matches -- this is what lets the arithmetic engine use a plain `dict` to
    look up "which named type does M¹ L² T⁻³ correspond to?".
    """

    time: int = 0
    length: int = 0
    mass: int = 0
    current: int = 0
    temperature: int = 0
    amount: int = 0
    luminous_intensity: int = 0
    angle: int = 0
    solid_angle: int = 0
    information: int = 0

    def __mul__(self, other: Dimension) -> Dimension:
        return Dimension(
            time=self.time + other.time,
            length=self.length + other.length,
            mass=self.mass + other.mass,
            current=self.current + other.current,
            temperature=self.temperature + other.temperature,
            amount=self.amount + other.amount,
            luminous_intensity=self.luminous_intensity + other.luminous_intensity,
            angle=self.angle + other.angle,
            solid_angle=self.solid_angle + other.solid_angle,
            information=self.information + other.information,
        )

    def __truediv__(self, other: Dimension) -> Dimension:
        return Dimension(
            time=self.time - other.time,
            length=self.length - other.length,
            mass=self.mass - other.mass,
            current=self.current - other.current,
            temperature=self.temperature - other.temperature,
            amount=self.amount - other.amount,
            luminous_intensity=self.luminous_intensity - other.luminous_intensity,
            angle=self.angle - other.angle,
            solid_angle=self.solid_angle - other.solid_angle,
            information=self.information - other.information,
        )

    @override
    def __repr__(self) -> str:
        labels = (
            ("time", "T"),
            ("length", "L"),
            ("mass", "M"),
            ("current", "I"),
            ("temperature", symbols.THETA),
            ("amount", "N"),
            ("luminous_intensity", "J"),
            ("angle", symbols.ANGLE),
            ("solid_angle", symbols.SOLID_ANGLE),
            ("information", symbols.INFORMATION),
        )

        parts = []
        for field, label in labels:
            exponent = getattr(self, field)
            if exponent == 0:
                continue
            parts.append(f"{label}{get_superscript(exponent)}")

        return " ".join(parts) if parts else "dimensionless"


DIMENSIONLESS = Dimension()
POWER = Dimension(time=-3, length=2, mass=1)
RESISTANCE = Dimension(time=-3, length=2, mass=1, current=-2)
VOLTAGE = Dimension(time=-3, length=2, mass=1, current=-1)
PRESSURE = Dimension(time=-2, length=-1, mass=1)
ACCELERATION = Dimension(time=-2, length=1)
FORCE = Dimension(time=-2, length=1, mass=1)
ENERGY = Dimension(time=-2, length=2, mass=1)
FREQUENCY = Dimension(time=-1)
VELOCITY = Dimension(time=-1, length=1)
TIME = Dimension(time=1)
CHARGE = Dimension(time=1, current=1)
CONDUCTANCE = Dimension(time=3, length=-2, mass=-1, current=2)
DENSITY = Dimension(length=-3, mass=1)
LENGTH = Dimension(length=1)
AREA = Dimension(length=2)
VOLUME = Dimension(length=3)
MASS = Dimension(mass=1)
CURRENT = Dimension(current=1)
TEMPERATURE_DELTA = Dimension(temperature=1)
AMOUNT_OF_SUBSTANCE = Dimension(amount=1)
LUMINOUS_INTENSITY = Dimension(luminous_intensity=1)

# Not strictly SI dimensions, but required to separate concepts.

ANGLE = Dimension(angle=1)
"""The dimension of a plane angle: `Angle`'s dimension.

See the module docstring for why this is tracked as its own axis rather than reusing
:data:`DIMENSIONLESS`, even though SI itself treats plane angle as dimensionless.
"""
SOLID_ANGLE = Dimension(solid_angle=1)
"""The dimension of a solid angle: `SolidAngle`'s dimension."""
DATA = Dimension(information=1)

# Derived, by explicit rules.

ENERGY_DENSITY = ENERGY / VOLUME
SPECIFIC_ENERGY = ENERGY / MASS
VELOCITY_SQUARED = VELOCITY * VELOCITY
MOMENTUM = MASS * VELOCITY
IMPULSE = FORCE * TIME
HEATING_RATE = TEMPERATURE_DELTA / TIME
HEAT_CAPACITY = ENERGY / TEMPERATURE_DELTA
SPECIFIC_HEAT_CAPACITY = SPECIFIC_ENERGY / TEMPERATURE_DELTA
MOLAR_HEAT_CAPACITY = HEAT_CAPACITY / AMOUNT_OF_SUBSTANCE
ANGULAR_VELOCITY = ANGLE / TIME
ANGULAR_ACCELERATION = ANGULAR_VELOCITY / TIME
ANGULAR_JERK = ANGULAR_ACCELERATION / TIME
"""∠ T⁻³: the rate of change of an angular acceleration, so `alpha / t` is one."""
ANGULAR_VELOCITY_SQUARED = ANGULAR_VELOCITY * ANGULAR_VELOCITY
"""∠² T⁻²: the square of an angular velocity, so `omega * omega * I` is an energy."""
TIME_SQUARED = TIME * TIME
"""T²: the square of a duration, so `t * t * g` is a length."""
TIME_CUBED = TIME_SQUARED * TIME
"""T³: the cube of a duration, so `j * t * t * t` is a length."""
TIME_FOURTH_POWER = TIME_CUBED * TIME
"""T⁴: the fourth power of a duration, so `s * t * t * t * t` is a length."""
JERK = ACCELERATION / TIME
"""T⁻³ L: the rate of change of an acceleration, so `j * t` is an acceleration."""
SNAP = JERK / TIME
"""T⁻⁴ L: the rate of change of a jerk, so `s * t` is a jerk."""
TORQUE = ENERGY / ANGLE
FIRST_MOMENT_OF_MASS = MASS * LENGTH
MOMENT_OF_INERTIA = TORQUE / ANGULAR_ACCELERATION
"""M L² ∠⁻²: the torque per angular acceleration, so `I * alpha` is a torque."""
ANGULAR_MOMENTUM = MOMENT_OF_INERTIA * ANGULAR_VELOCITY
DATA_RATE = DATA / TIME
MAGNETIC_FLUX = VOLTAGE * TIME
MAGNETIC_FLUX_DENSITY = MAGNETIC_FLUX / AREA
CAPACITANCE = CHARGE / VOLTAGE
INDUCTANCE = MAGNETIC_FLUX / CURRENT
PERMITTIVITY = CAPACITANCE / LENGTH
PERMEABILITY = INDUCTANCE / LENGTH
MAGNETIC_FIELD_STRENGTH = CURRENT / LENGTH
LUMINOUS_FLUX = LUMINOUS_INTENSITY * SOLID_ANGLE
ILLUMINANCE = LUMINOUS_FLUX / AREA
LUMINOUS_ENERGY = LUMINOUS_FLUX * TIME
LUMINOUS_EXPOSURE = ILLUMINANCE * TIME
LUMINANCE = LUMINOUS_INTENSITY / AREA
LUMINOUS_EFFICACY = LUMINOUS_FLUX / POWER
VOLUMETRIC_FLOW_RATE = VOLUME / TIME
MASS_FLOW_RATE = MASS / TIME
MOLAR_MASS = MASS / AMOUNT_OF_SUBSTANCE
MOLAR_CONCENTRATION = AMOUNT_OF_SUBSTANCE / VOLUME
MOLAR_ENERGY = ENERGY / AMOUNT_OF_SUBSTANCE
ENTITIES_PER_AMOUNT = DIMENSIONLESS / AMOUNT_OF_SUBSTANCE
MOLALITY = AMOUNT_OF_SUBSTANCE / MASS
MOLAR_VOLUME = VOLUME / AMOUNT_OF_SUBSTANCE
MOLAR_FLOW_RATE = AMOUNT_OF_SUBSTANCE / TIME
MOLAR_CHARGE = CHARGE / AMOUNT_OF_SUBSTANCE
SPECIFIC_CHARGE = CHARGE / MASS
ACTIVITY_CONCENTRATION = FREQUENCY / VOLUME
SPECIFIC_ACTIVITY = FREQUENCY / MASS
SURFACE_ACTIVITY = FREQUENCY / AREA
SPECIFIC_CURRENT = CURRENT / MASS
SPECIFIC_POWER = POWER / MASS

__all__ = [
    "ACCELERATION",
    "ACTIVITY_CONCENTRATION",
    "AMOUNT_OF_SUBSTANCE",
    "ANGLE",
    "ANGULAR_ACCELERATION",
    "ANGULAR_JERK",
    "ANGULAR_MOMENTUM",
    "ANGULAR_VELOCITY",
    "ANGULAR_VELOCITY_SQUARED",
    "AREA",
    "CAPACITANCE",
    "CHARGE",
    "CONDUCTANCE",
    "CURRENT",
    "DATA",
    "DATA_RATE",
    "DENSITY",
    "DIMENSIONLESS",
    "ENERGY",
    "ENERGY_DENSITY",
    "ENTITIES_PER_AMOUNT",
    "FIRST_MOMENT_OF_MASS",
    "FORCE",
    "FREQUENCY",
    "HEATING_RATE",
    "HEAT_CAPACITY",
    "ILLUMINANCE",
    "IMPULSE",
    "INDUCTANCE",
    "JERK",
    "LENGTH",
    "LUMINANCE",
    "LUMINOUS_EFFICACY",
    "LUMINOUS_ENERGY",
    "LUMINOUS_EXPOSURE",
    "LUMINOUS_FLUX",
    "LUMINOUS_INTENSITY",
    "MAGNETIC_FIELD_STRENGTH",
    "MAGNETIC_FLUX",
    "MAGNETIC_FLUX_DENSITY",
    "MASS",
    "MASS_FLOW_RATE",
    "MOLALITY",
    "MOLAR_CHARGE",
    "MOLAR_CONCENTRATION",
    "MOLAR_ENERGY",
    "MOLAR_FLOW_RATE",
    "MOLAR_HEAT_CAPACITY",
    "MOLAR_MASS",
    "MOLAR_VOLUME",
    "MOMENTUM",
    "PERMEABILITY",
    "PERMITTIVITY",
    "POWER",
    "PRESSURE",
    "RESISTANCE",
    "SNAP",
    "SOLID_ANGLE",
    "SPECIFIC_ACTIVITY",
    "SPECIFIC_CHARGE",
    "SPECIFIC_CURRENT",
    "SPECIFIC_ENERGY",
    "SPECIFIC_HEAT_CAPACITY",
    "SPECIFIC_POWER",
    "SURFACE_ACTIVITY",
    "TEMPERATURE_DELTA",
    "TIME",
    "TIME_CUBED",
    "TIME_FOURTH_POWER",
    "TIME_SQUARED",
    "TORQUE",
    "VELOCITY",
    "VELOCITY_SQUARED",
    "VOLTAGE",
    "VOLUME",
    "VOLUMETRIC_FLOW_RATE",
    "Dimension",
]
