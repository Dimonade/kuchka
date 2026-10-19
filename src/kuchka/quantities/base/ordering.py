"""Equality, hashing, and a total order for exact-type scalar quantities."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Self

from kuchka.errors import IncompatibleDimensionError
from kuchka.internal.typing import override

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension


class _OrderedScalarMixin:
    """Equality, hashing, and a total order over a `_ScalarStorage` magnitude.

    Composed into `LinearQuantity` and `AffineQuantity`: both are exact-type,
    totally-ordered scalars, so "equal" and "less than" mean the same thing for
    either -- compare the stored magnitude, only against another instance of the
    exact same type.

    Deliberately not part of `_ScalarStorage` itself: a modular/circular quantity
    (a compass heading, a phase angle) shares the same storage shape but has no
    well-defined, universal "greater than", so it composes `_ScalarStorage` directly
    and leaves ordering out, rather than inheriting it here and having to
    un-implement it.
    """

    _magnitude: Fraction
    dimension: ClassVar[Dimension]
    __slots__ = ()

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, _OrderedScalarMixin) or type(self) is not type(other):
            return NotImplemented
        return self._magnitude == other._magnitude

    @override
    def __hash__(self) -> int:
        return hash((type(self), self._magnitude))

    def __lt__(self, other: Self) -> bool:
        if not isinstance(other, _OrderedScalarMixin) or type(self) is not type(other):
            raise IncompatibleDimensionError("compare", self, other)
        return self._magnitude < other._magnitude

    def __le__(self, other: Self) -> bool:
        if not isinstance(other, _OrderedScalarMixin) or type(self) is not type(other):
            raise IncompatibleDimensionError("compare", self, other)
        return self._magnitude <= other._magnitude

    def __gt__(self, other: Self) -> bool:
        if not isinstance(other, _OrderedScalarMixin) or type(self) is not type(other):
            raise IncompatibleDimensionError("compare", self, other)
        return self._magnitude > other._magnitude

    def __ge__(self, other: Self) -> bool:
        if not isinstance(other, _OrderedScalarMixin) or type(self) is not type(other):
            raise IncompatibleDimensionError("compare", self, other)
        return self._magnitude >= other._magnitude


__all__ = ["_OrderedScalarMixin"]
