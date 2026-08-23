"""Dimensional analysis primitives.

This module is internal machinery.
Ordinary users of the library never construct a :class:`Dimension` directly,
as they use the named engineering types (``Voltage``, ``Current``, ...),
and unit constructors (``Volt``, ``Milliampere``, ...) exposed from the top-level.

Dimensions are represented as exponent vectors over five of the seven SI base
quantities: mass, length, time, electric current, and thermodynamic temperature.
Amount of substance and luminous intensity are not yet represented, since nothing in
the current engineering vocabulary needs them;
adding either later means adding a field to :class:`Dimension` and the corresponding
case to its arithmetic below.

Multiplying two physical quantities adds their exponent vectors.
Dividing subtracts them.
This gives the arithmetic engine a single general mechanism for deriving compound
dimensions (Power from Voltage * Current, Resistance from Voltage / Current, and so on),
instead of a hand-written table of every possible pairwise combination.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Dimension:
    """An exponent vector over the SI base dimensions used by this library.

    Two ``Dimension`` instances compare equal (and hash equal) exactly when every
    exponent matches -- this is what lets the arithmetic engine use a plain `dict` to
    look up "which named type does M^1 L^2 T^-3 correspond to?".
    """

    mass: int = 0
    length: int = 0
    time: int = 0
    current: int = 0
    temperature: int = 0

    def __mul__(self, other: Dimension) -> Dimension:
        return Dimension(
            mass=self.mass + other.mass,
            length=self.length + other.length,
            time=self.time + other.time,
            current=self.current + other.current,
            temperature=self.temperature + other.temperature,
        )

    def __truediv__(self, other: Dimension) -> Dimension:
        return Dimension(
            mass=self.mass - other.mass,
            length=self.length - other.length,
            time=self.time - other.time,
            current=self.current - other.current,
            temperature=self.temperature - other.temperature,
        )

    def __repr__(self) -> str:
        labels = (
            ("mass", "M"),
            ("length", "L"),
            ("time", "T"),
            ("current", "I"),
            ("temperature", "\u0398"),
        )
        parts = []
        for field, label in labels:
            exponent = getattr(self, field)
            if exponent == 0:
                continue
            parts.append(label if exponent == 1 else f"{label}^{exponent}")
        return " ".join(parts) if parts else "dimensionless"


DIMENSIONLESS = Dimension()
CURRENT = Dimension(current=1)
VOLTAGE = Dimension(mass=1, length=2, time=-3, current=-1)
POWER = Dimension(mass=1, length=2, time=-3)
RESISTANCE = Dimension(mass=1, length=2, time=-3, current=-2)
TEMPERATURE_DELTA = Dimension(temperature=1)
