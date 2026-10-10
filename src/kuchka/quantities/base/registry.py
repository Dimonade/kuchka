"""The dimension registry: what arithmetic hands back for a given exponent vector.

NOTE: Kept separate from `linear.py` even though `_promote` only ever constructs
`LinearQuantity` subclasses, because the dependency runs the other way at import
time: `LinearQuantity.__mul__`/`__truediv__` call `_promote`, so this module cannot
import `linear.py` at runtime without creating a cycle.
The `LinearQuantity` import below is therefore `TYPE_CHECKING`-only -- needed for
accurate annotations, not needed to actually run `register()` or `_promote()`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import DIMENSIONLESS
from kuchka.errors import AmbiguousKindError
from kuchka.errors import PlannedDimensionError
from kuchka.errors import UnrepresentableDimensionError

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.quantities.base.linear import LinearQuantity

_DIMENSION_REGISTRY: dict[Dimension, type[LinearQuantity]] = {}
"""Maps a dimension signature to its principal kind, the type arithmetic hands back.

So ``Volt(5) * Ampere(2)`` produces a real ``Power`` instance.

Each quantity module populates this via ``_register`` as a side effect of being
imported, so this module needs no list of the types in advance.
The registry is closed when the package finishes importing (see ``_close``): the named
dimensions are part of the library, and arithmetic hands back the library's own types.

A type is a kind, and several kinds can share one dimension.
The principal kind of a dimension is the general SI/physics name for it
(``Voltage`` for M L^2 T^-3 I^-1, ``Frequency`` for T^-1, and so on), and it is the
only kind of that dimension that arithmetic produces.
Every other kind of the dimension declares how it relates to the principal when it
registers (see ``_SPECIALISATIONS`` and ``_CONTESTED``), and a type that shares a
dimension without declaring a relation is refused.
A dimension in ``_CONTESTED`` has no principal and so no entry here.
"""

_SPECIALISATIONS: dict[type[LinearQuantity], type[LinearQuantity]] = {}
"""Maps a specialisation to the kind of its dimension that it specialises.

A specialisation is a role of an existing kind: ``SamplingPeriod`` of ``Time``,
``SampleRate`` and ``BaudRate`` of ``Frequency``.
It is reached only by explicit construction, and every conversion between it and
another kind is a named operation on the type.
"""

_CONTESTED: dict[Dimension, tuple[type[LinearQuantity], ...]] = {}
"""Maps a dimension to the kinds that share it on equal footing.

No kind of a contested dimension is principal, so arithmetic cannot pick a result
type for the dimension by itself.
"""

_PLANNED_DIMENSIONS: dict[Dimension, str] = {}
"""Maps a dimension signature to the name of a quantity this library intends to
implement but does not yet.

Lets `_promote` raise `PlannedDimensionError` for a dimension this library already has
a name for, naming the result instead of only printing its exponent vector.

Curated by hand, the same way the `@overload` tables are: adding an entry here improves
the error message, and is a marker for what to implement next.

Emptied out as each named dimension gets a real registered type.
"""


_closed = False


def _kinds_of(dimension: Dimension) -> tuple[type[LinearQuantity], ...]:
    """Return every kind registered for `dimension`, in registration order."""
    principals: tuple[type[LinearQuantity], ...]
    if dimension in _CONTESTED:
        principals = _CONTESTED[dimension]
    elif dimension in _DIMENSION_REGISTRY:
        principals = (_DIMENSION_REGISTRY[dimension],)
    else:
        return ()
    specialisations = tuple(
        kind for kind in _SPECIALISATIONS if kind.dimension == dimension
    )
    return principals + specialisations


def _shared_dimensions() -> dict[Dimension, tuple[type[LinearQuantity], ...]]:
    """Return each dimension that has more than one kind, with its kinds."""
    dimensions = {*_DIMENSION_REGISTRY, *_CONTESTED}
    return {
        dimension: kinds
        for dimension in dimensions
        if len(kinds := _kinds_of(dimension)) > 1
    }


def _is_registered(quantity_type: type[LinearQuantity]) -> bool:
    """Return whether `quantity_type` is a registered kind of its dimension."""
    return quantity_type in _kinds_of(quantity_type.dimension)


def _register(
    dimension: Dimension,
    quantity_type: type[LinearQuantity],
    *,
    specialisation_of: type[LinearQuantity] | None = None,
    contested_with: type[LinearQuantity] | None = None,
) -> None:
    """Register `quantity_type` as a kind of `dimension`.

    The first type of a dimension becomes its principal kind.
    A later type states its relation to a kind already registered for the dimension:
    `specialisation_of` makes it a role of that kind, and `contested_with` places it
    on equal footing with that kind, after which neither is principal.

    Called once per quantity type, at import time, by the module that defines that type.

    Raises `TypeError` for a second type that states no relation, for a relation to a
    type that is not a registered kind of the dimension, and for a type whose own
    `dimension` is another one; and `RuntimeError` once the registry is closed.
    These are defects in kuchka's own quantity modules, not something a caller of the
    public API can trigger, so none of them is part of the `MeasurementError`
    hierarchy that application code handles.
    A refused registration leaves the registry unchanged.
    """
    if _closed:
        msg = (
            f"cannot register {quantity_type.__name__}: the dimension registry is "
            "closed once `kuchka` has finished importing."
        )
        raise RuntimeError(msg)
    if quantity_type.dimension != dimension:
        msg = (
            f"{quantity_type.__name__} has dimension "
            f"{quantity_type.dimension!r} and cannot be registered for {dimension!r}."
        )
        raise TypeError(msg)
    if specialisation_of is not None and contested_with is not None:
        msg = (
            f"{quantity_type.__name__} is either a specialisation or contested, "
            "not both."
        )
        raise TypeError(msg)

    known = _kinds_of(dimension)
    if specialisation_of is not None:
        _register_specialisation(quantity_type, specialisation_of, known)
    elif contested_with is not None:
        _register_contested(quantity_type, contested_with, known)
    elif quantity_type not in known:
        if known:
            names = ", ".join(kind.__name__ for kind in known)
            msg = (
                f"dimension {dimension!r} is already registered to {names}; "
                f"{quantity_type.__name__} has to declare how it relates to it, as a "
                "specialisation (`specialisation_of=`) or as contested "
                "(`contested_with=`), so that arithmetic has one principal kind to "
                "hand back or none (see the note above `_DIMENSION_REGISTRY`)."
            )
            raise TypeError(msg)
        _DIMENSION_REGISTRY[dimension] = quantity_type


def _register_specialisation(
    quantity_type: type[LinearQuantity],
    target: type[LinearQuantity],
    known: tuple[type[LinearQuantity], ...],
) -> None:
    """Record `quantity_type` as a specialisation of `target`."""
    _check_relation_target(quantity_type, target, known)
    if _SPECIALISATIONS.get(quantity_type) is target:
        return
    _refuse_if_kind_already_registered(quantity_type, known)
    _SPECIALISATIONS[quantity_type] = target


def _register_contested(
    quantity_type: type[LinearQuantity],
    target: type[LinearQuantity],
    known: tuple[type[LinearQuantity], ...],
) -> None:
    """Place `quantity_type` on equal footing with `target`."""
    dimension = quantity_type.dimension
    _check_relation_target(quantity_type, target, known)
    if quantity_type in _CONTESTED.get(dimension, ()):
        return
    _refuse_if_kind_already_registered(quantity_type, known)
    if dimension in _CONTESTED:
        _CONTESTED[dimension] = (*_CONTESTED[dimension], quantity_type)
    else:
        _CONTESTED[dimension] = (_DIMENSION_REGISTRY.pop(dimension), quantity_type)


def _check_relation_target(
    quantity_type: type[LinearQuantity],
    target: type[LinearQuantity],
    known: tuple[type[LinearQuantity], ...],
) -> None:
    """Refuse a relation to something other than a principal or contested kind."""
    principals = [kind for kind in known if kind not in _SPECIALISATIONS]
    if target is quantity_type or target not in principals:
        names = ", ".join(kind.__name__ for kind in principals) or "nothing yet"
        msg = (
            f"{quantity_type.__name__} cannot relate to {target.__name__}: a "
            f"relation names another kind registered for {quantity_type.dimension!r} "
            "that is not "
            f"itself a specialisation (registered: {names})."
        )
        raise TypeError(msg)


def _refuse_if_kind_already_registered(
    quantity_type: type[LinearQuantity],
    known: tuple[type[LinearQuantity], ...],
) -> None:
    """Refuse to give a registered type a second, different relation."""
    if quantity_type in known:
        msg = (
            f"{quantity_type.__name__} is already registered with a different relation."
        )
        raise TypeError(msg)


def _concrete_linear_types() -> list[type[LinearQuantity]]:
    """Return every concrete linear quantity type that has been defined."""
    from kuchka.quantities.base.linear import LinearQuantity  # noqa: PLC0415 -- the module imports this one at its own import time

    found: list[type[LinearQuantity]] = []
    pending = list(LinearQuantity.__subclasses__())
    while pending:
        candidate = pending.pop()
        pending.extend(candidate.__subclasses__())
        if "dimension" in vars(candidate):
            found.append(candidate)
    return found


def _close() -> None:
    """Close the registry: later registrations raise `RuntimeError`.

    Called once, when the package has imported every quantity module.
    Every concrete linear quantity type with a dimension has to be a registered kind
    of it by then, so a type that shares a dimension cannot exist without having
    declared its relation.
    Raises `TypeError` naming the types that are not.
    """
    global _closed  # noqa: PLW0603 -- one-way switch, set once at the end of the import
    if _closed:
        return
    undeclared = sorted(
        kind.__name__
        for kind in _concrete_linear_types()
        if kind.dimension != DIMENSIONLESS and not _is_registered(kind)
    )
    if undeclared:
        msg = (
            f"{', '.join(undeclared)} share a dimension without being registered "
            "for it: each states a relation to the kinds already there."
        )
        raise TypeError(msg)
    _closed = True


def _promote(dimension: Dimension, magnitude: Fraction) -> LinearQuantity | Fraction:
    """Build the correctly-typed result of a multiplication or division.

    A dimensionless result (e.g. Resistance / Resistance) is returned as a plain
    ``Fraction`` ratio, matching ordinary physics convention.
    """
    if dimension == DIMENSIONLESS:
        return magnitude
    contested = _CONTESTED.get(dimension)
    if contested is not None:
        raise AmbiguousKindError(dimension, contested)
    try:
        quantity_type = _DIMENSION_REGISTRY[dimension]
    except KeyError:
        planned_name = _PLANNED_DIMENSIONS.get(dimension)
        if planned_name is not None:
            raise PlannedDimensionError(dimension, planned_name) from None
        raise UnrepresentableDimensionError(dimension) from None
    return quantity_type(magnitude, quantity_type._canonical_unit)  # noqa: SLF001 -- accessing the registered type's own canonical unit, not a foreign instance's internals


__all__: list[str] = []
