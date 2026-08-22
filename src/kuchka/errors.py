"""The measurement system's exception hierarchy.

Every error a user is likely to hit -- a dimension mismatch, a naked float
where a measurement was expected, an unrecognised conversion target -- is a
subclass of :class:`MeasurementError`, so application code can catch the
whole family with one except clause if it wants to.
"""

from __future__ import annotations

from typing import Any


class MeasurementError(Exception):
    """Base class for all measurement-system errors."""


class InvalidMeasurementError(MeasurementError):
    """A value could not be turned into (or combined with) a measurement.

    Raised at construction time (e.g. passing a string, or a measurement of
    the wrong dimension, into a unit constructor) and at arithmetic
    boundaries where a naked number was used where a measurement was
    expected.
    """


class IncompatibleDimensionError(MeasurementError):
    """Raised when an operation is attempted between incompatible dimensions."""

    def __init__(self, operation: str, left: Any, right: Any) -> None:
        left_name = type(left).__name__
        right_name = type(right).__name__
        left_dim = getattr(left, "dimension", None)
        right_dim = getattr(right, "dimension", None)
        message = (
            f"Cannot {operation} {left_name} and {right_name}.\n"
            f"{left_name} has dimension [{left_dim!r}].\n"
            f"{right_name} has dimension [{right_dim!r}]."
        )
        super().__init__(message)
        self.operation = operation
        self.left = left
        self.right = right


class InvalidConversionError(MeasurementError):
    """Raised when ``.to(...)`` is given something that isn't a valid unit."""


class UnrepresentableDimensionError(MeasurementError):
    """Raised when arithmetic produces a dimension with no registered type.

    This is a scope boundary, not a bug: v0.1 only knows about the
    quantities listed in the design proposal. Operations that would
    mathematically produce something outside that vocabulary (e.g.
    Resistance * Resistance) are rejected clearly rather than silently
    returning an untyped number.
    """

    def __init__(self, dimension: Any) -> None:
        super().__init__(
            f"the result of this operation has dimension [{dimension!r}], "
            "which has no registered engineering type in this version of "
            "the library."
        )
        self.dimension = dimension
