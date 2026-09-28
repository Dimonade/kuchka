"""Dimensional analysis primitives.

This module is internal machinery.
Ordinary users of the library never construct a :class:`Dimension` directly,
as they use the named engineering types (``Voltage``, ``Current``, ...),
and unit constructors (``Volt``, ``Milliampere``, ...) exposed from the top-level.

Dimensions are represented as exponent vectors over the seven SI base quantities:
mass, length, time, electric current, thermodynamic temperature, amount of substance,
and luminous intensity -- plus one supplementary axis, ``angle``, tracked separately
from the seven base quantities.

SI itself treats plane angle as a quantity of dimension one (the radian is a
dimensionless derived unit), and `kuchka` is not taking a position against that.
The ``angle`` field exists purely so that :data:`ANGLE` and :data:`DIMENSIONLESS` are
distinguishable ``Dimension`` values here.
Without it, `Proportion` (genuinely dimensionless, ``Percent``/``Ratio``) and `Angle`
would compare as the exact same dimension, which would be wrong to build error messages
and conversion checks against even though SI's own base-quantity accounting agrees they
are both "one".

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
    look up "which named type does M^1 L^2 T^-3 correspond to?".
    """

    time: int = 0
    length: int = 0
    mass: int = 0
    current: int = 0
    temperature: int = 0
    amount: int = 0
    luminous_intensity: int = 0
    angle: int = 0

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
ANGLE = Dimension(angle=1)
"""The dimension of a plane angle: `Angle`'s dimension.

See the module docstring for why this is tracked as its own axis rather than reusing
:data:`DIMENSIONLESS`, even though SI itself treats plane angle as dimensionless.
"""

__all__ = [
    "ACCELERATION",
    "AMOUNT_OF_SUBSTANCE",
    "ANGLE",
    "AREA",
    "CHARGE",
    "CONDUCTANCE",
    "CURRENT",
    "DENSITY",
    "DIMENSIONLESS",
    "ENERGY",
    "FORCE",
    "FREQUENCY",
    "LENGTH",
    "LUMINOUS_INTENSITY",
    "MASS",
    "POWER",
    "PRESSURE",
    "RESISTANCE",
    "TEMPERATURE_DELTA",
    "TIME",
    "VELOCITY",
    "VOLTAGE",
    "VOLUME",
    "Dimension",
]
