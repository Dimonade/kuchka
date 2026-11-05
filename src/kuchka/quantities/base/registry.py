"""The dimension registry: what arithmetic hands back for a given exponent vector.

NOTE: Kept separate from `linear.py` even though `_promote` only ever constructs
`LinearQuantity` subclasses, because the dependency runs the other way at import
time: `LinearQuantity.__mul__`/`__truediv__` call `_promote`, so this module cannot
import `linear.py` at runtime without creating a cycle.
The `LinearQuantity` import below is therefore `TYPE_CHECKING`-only -- needed for
accurate annotations, not needed to actually run `register()` or `_promote()`.
"""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING
from typing import Any
from typing import Literal
from typing import cast

from kuchka.dimensions import DIMENSIONLESS
from kuchka.errors import AmbiguousKindError
from kuchka.errors import IncompatibleDimensionError
from kuchka.errors import PlannedDimensionError
from kuchka.errors import UnrepresentableDimensionError
from kuchka.internal.constants import PI
from kuchka.quantities.base.storage import _concrete_types

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.quantities.base.linear import LinearQuantity
    from kuchka.quantities.base.storage import _ScalarStorage
    from kuchka.quantities.base.units import UnitDef

    _Kind = type[_ScalarStorage[Any]]

_KINDS_BY_DIMENSION: dict[Dimension, tuple[_Kind, ...]] = {}
"""Maps a dimension to every quantity kind registered for it, in registration order.

A type is a kind of its dimension, whatever its shape (linear, affine, modular,
logarithmic), and several kinds can share one dimension.
Every concrete quantity type is registered here; this catalogue records which kinds
exist and never decides which type arithmetic returns.
"""

_DIMENSION_REGISTRY: dict[Dimension, type[LinearQuantity]] = {}
"""Maps a dimension signature to its principal kind, the type arithmetic hands back.

So ``Volt(5) * Ampere(2)`` produces a real ``Power`` instance.

Each quantity module populates this via ``_register`` as a side effect of being
imported, so this module needs no list of the types in advance.
The registry is closed when the package finishes importing (see ``_close``): the named
dimensions are part of the library, and arithmetic hands back the library's own types.

Only a linear kind of a dimension with extent is a principal kind, the general
SI/physics name for the dimension (``Voltage`` for M L² T⁻³ I⁻¹, ``Frequency`` for
T⁻¹).
Arithmetic never produces an affine, modular, or logarithmic value, and it returns a
ratio kind or a plain ``Fraction`` for a dimensionless result (see ``_RATIO_KIND``), so
those kinds are in the catalogue and never here.
A second linear kind of a dimension with extent states its relation to the first, as
a specialisation or as contested, and a kind that states none is refused.
A dimension in ``_CONTESTED`` has no principal and so no entry here.
"""

_CONTESTED: dict[Dimension, tuple[type[LinearQuantity], ...]] = {}
"""Maps a dimension to the linear kinds that share it on equal footing.

No kind of a contested dimension is principal, so arithmetic cannot pick a result
type for the dimension by itself.
"""

_SPECIALISATIONS: dict[_Kind, _Kind] = {}
"""Maps a specialisation to the kind it is a role of.

A specialisation is a role of a kind of its dimension and of its shape, such as
``SamplingPeriod`` of ``Time``, and ``SampleRate`` and ``BaudRate`` of ``Frequency``.
It is reached only by explicit construction, and every conversion between it and
another kind is a named operation on the type.
The relation records meaning: it does not convert values, and it does not pick an
arithmetic result unless a rule in ``_RULES`` names the role.
The target is a kind that is not itself a specialisation.
"""

_RULES: dict[tuple[_Kind, str, _Kind], _Kind] = {}
"""Maps (left kind, operation, right kind) to the kind that product or quotient has.

The operation is ``"*"`` or ``"/"``, and the kinds are the exact types of the operands.
An explicit rule decides the result type before the dimension is consulted, so it is
what separates two kinds that share a dimension.
It is also the only way a role takes part in a product or quotient beyond scaling,
dividing by itself, and multiplying by its reciprocal: ``AbsorbedDoseRate * Time`` is
an ``AbsorbedDose`` by a rule.
For instance, ``Force / Area`` is a ``Pressure`` and ``Energy / Volume`` an
``EnergyDensity`` although both results are M L⁻¹ T⁻².
A product is entered in both operand orders.
Every rule is declared through ``_rule`` while the package imports, and the table
closes with the registry.
"""

_BRIDGES: dict[tuple[_Kind, str, _Kind], tuple[_Kind, Fraction]] = {}
"""Maps (left kind, operation, right kind) to the kind a bridge gives, and its factor.

A bridge is a rule whose result differs from the plain product or quotient on the
angle axis alone: ``AngularVelocity * Length`` is a ``Velocity``.
It states ``1 rad = 1`` for the operand kinds it names, so the canonical magnitude is
multiplied by ``(2 pi) ** (a_p - a_r)``, with ``a_p`` the angle exponent of the plain
product and ``a_r`` that of the result, because the turn is the canonical angle.
The plain dimension of a bridge has no arithmetic kind, which the registry checks when
it closes.
A product is entered in both operand orders.
"""

_RECIPROCALS: dict[_Kind, _Kind] = {}
"""Maps a specialisation to the specialisation it is the reciprocal of, in both ways.

A specialisation combines with a plain number, a dimensionless quantity, and itself in
a quotient.
Its reciprocal is the one other kind it multiplies with, and the product is a plain
``Fraction``: ``SampleRate`` times ``SamplingPeriod`` counts samples.
Every other combination is refused, because a role is reached only by explicit
construction and left only by a named conversion.
"""

_RATIO_KIND: dict[Dimension, _Kind] = {}
"""Maps the dimensionless dimension to the kind a ratio of two like quantities has.

A quotient of two quantities of one dimension, and a product of two dimensionless
quantities, is a ratio.
Other dimensionless results, such as a frequency times a duration, count cycles and
remain plain ``Fraction`` values: the dimension has no principal kind.
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


def _kinds_of(dimension: Dimension) -> tuple[_Kind, ...]:
    """Return every kind registered for `dimension`, in registration order."""
    return _KINDS_BY_DIMENSION.get(dimension, ())


def _shared_dimensions() -> dict[Dimension, tuple[_Kind, ...]]:
    """Return each dimension that has more than one kind, with its kinds."""
    return {
        dimension: kinds
        for dimension, kinds in _KINDS_BY_DIMENSION.items()
        if len(kinds) > 1
    }


def _is_registered(quantity_type: _Kind) -> bool:
    """Return whether `quantity_type` is a registered kind of its dimension."""
    return quantity_type in _kinds_of(quantity_type.dimension)


def _shape_of(quantity_type: _Kind) -> type:
    """Return the shape base (linear, affine, modular, logarithmic) of a type."""
    from kuchka.quantities.base import AffineQuantity  # noqa: PLC0415
    from kuchka.quantities.base import LinearQuantity  # noqa: PLC0415 -- same cycle
    from kuchka.quantities.base import ModularQuantity  # noqa: PLC0415 -- same cycle
    from kuchka.quantities.base import PureLogarithmicQuantity  # noqa: PLC0415

    for shape in (
        LinearQuantity,
        AffineQuantity,
        ModularQuantity,
        PureLogarithmicQuantity,
    ):
        if issubclass(quantity_type, shape):
            return shape
    msg = (
        f"{quantity_type.__name__} is not a linear, affine, modular, or logarithmic "
        "type."
    )
    raise TypeError(msg)


def _is_arithmetic_kind(quantity_type: _Kind) -> bool:
    """Return whether arithmetic could produce `quantity_type`.

    A linear kind of a dimension with extent can be an arithmetic result; every other
    kind is only ever reached by explicit construction.
    """
    from kuchka.quantities.base import LinearQuantity  # noqa: PLC0415

    return (
        issubclass(quantity_type, LinearQuantity)
        and quantity_type.dimension != DIMENSIONLESS
    )


def _arithmetic_roots(dimension: Dimension) -> tuple[type[LinearQuantity], ...]:
    """Return the principal kind of `dimension`, or the kinds contesting for it."""
    if dimension in _CONTESTED:
        return _CONTESTED[dimension]
    if dimension in _DIMENSION_REGISTRY:
        return (_DIMENSION_REGISTRY[dimension],)
    return ()


def _relation_of(quantity_type: _Kind) -> tuple[str, _Kind | None] | None:
    """Return how `quantity_type` is registered, or `None` if it is not."""
    if not _is_registered(quantity_type):
        return None
    if quantity_type in _SPECIALISATIONS:
        return ("specialisation", _SPECIALISATIONS[quantity_type])
    if quantity_type in _CONTESTED.get(quantity_type.dimension, ()):
        return ("contested", None)
    return ("root", None)


def _register(
    dimension: Dimension,
    quantity_type: _Kind,
    *,
    specialisation_of: _Kind | None = None,
    contested_with: _Kind | None = None,
) -> None:
    """Register `quantity_type` as a kind of `dimension`.

    Every concrete quantity type registers once, whatever its shape.
    A linear kind of a dimension with extent is also entered in the arithmetic
    registries: the first becomes the principal kind, and a later one states its
    relation to the linear kinds already there.
    `specialisation_of` makes it a role of a kind of its dimension and shape, and
    `contested_with` places it on equal footing with another linear kind, after which
    neither is principal.
    Kinds of other shapes, and dimensionless kinds, share a dimension without stating
    a relation, because arithmetic never chooses between them.

    Called once per quantity type, at import time, by the module that defines that type.

    Raises `TypeError` for a linear kind that has to state a relation and does not, for
    a relation that does not fit, and for a type whose own `dimension` is another one;
    and `RuntimeError` once the registry is closed.
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
        msg = f"{quantity_type.__name__} states one relation, not both."
        raise TypeError(msg)

    current = _relation_of(quantity_type)
    if current is not None:
        if current != _requested_relation(specialisation_of, contested_with):
            msg = (
                f"{quantity_type.__name__} is already registered with a different "
                "relation."
            )
            raise TypeError(msg)
        return
    _validate_new_kind(quantity_type, specialisation_of, contested_with)
    _commit_kind(quantity_type, specialisation_of, contested_with)


def _requested_relation(
    specialisation_of: _Kind | None, contested_with: _Kind | None
) -> tuple[str, _Kind | None]:
    """Return the relation a registration states, in `_relation_of`'s terms."""
    if specialisation_of is not None:
        return ("specialisation", specialisation_of)
    if contested_with is not None:
        return ("contested", None)
    return ("root", None)


def _validate_new_kind(
    quantity_type: _Kind,
    specialisation_of: _Kind | None,
    contested_with: _Kind | None,
) -> None:
    """Refuse a first registration that does not fit, before anything is recorded."""
    if specialisation_of is not None:
        _check_specialisation(quantity_type, specialisation_of)
    elif contested_with is not None:
        _check_contested(quantity_type, contested_with)
    elif _is_arithmetic_kind(quantity_type) and (
        linear := _arithmetic_roots(quantity_type.dimension)
    ):
        names = ", ".join(kind.__name__ for kind in linear)
        msg = (
            f"dimension {quantity_type.dimension!r} is already registered to {names}; "
            f"{quantity_type.__name__} has to state its relation to it: a "
            "specialisation (`specialisation_of=`) or contested (`contested_with=`), "
            "so that arithmetic has one principal kind to hand back or none (see the "
            "note above `_DIMENSION_REGISTRY`)."
        )
        raise TypeError(msg)


def _commit_kind(
    quantity_type: _Kind,
    specialisation_of: _Kind | None,
    contested_with: _Kind | None,
) -> None:
    """Record a validated first registration in every registry it belongs to."""
    dimension = quantity_type.dimension
    _KINDS_BY_DIMENSION[dimension] = (*_kinds_of(dimension), quantity_type)
    if specialisation_of is not None:
        _SPECIALISATIONS[quantity_type] = specialisation_of
        return
    linear = cast("type[LinearQuantity]", quantity_type)
    if contested_with is not None:
        contested = _CONTESTED.get(dimension) or (_DIMENSION_REGISTRY.pop(dimension),)
        _CONTESTED[dimension] = (*contested, linear)
    elif _is_arithmetic_kind(quantity_type):
        _DIMENSION_REGISTRY[dimension] = linear


def _check_specialisation(quantity_type: _Kind, target: _Kind) -> None:
    """Refuse a specialisation that is not a role of a kind of the same shape."""
    if (
        target is quantity_type
        or target.dimension != quantity_type.dimension
        or not _is_registered(target)
    ):
        names = ", ".join(kind.__name__ for kind in _kinds_of(quantity_type.dimension))
        msg = (
            f"{quantity_type.__name__} cannot specialise {target.__name__}: a "
            f"specialisation names another kind registered for "
            f"{quantity_type.dimension!r} (registered: {names or 'nothing yet'})."
        )
        raise TypeError(msg)
    if target in _SPECIALISATIONS:
        msg = (
            f"{quantity_type.__name__} cannot specialise {target.__name__}, which is "
            "itself a specialisation: name the kind it specialises."
        )
        raise TypeError(msg)
    if _shape_of(quantity_type) is not _shape_of(target):
        msg = (
            f"{quantity_type.__name__} cannot specialise {target.__name__}: a "
            "specialisation has the shape of its kind."
        )
        raise TypeError(msg)


def _check_contested(quantity_type: _Kind, target: _Kind) -> None:
    """Refuse a contest that is not between linear kinds arithmetic could produce."""
    if not _is_arithmetic_kind(quantity_type) or target not in _arithmetic_roots(
        quantity_type.dimension
    ):
        msg = (
            f"{quantity_type.__name__} cannot be contested with {target.__name__}: "
            "only linear kinds that arithmetic could produce are contested, and the "
            "target is the principal kind or one of the contested kinds."
        )
        raise TypeError(msg)


def _result_unit(kind: type[LinearQuantity]) -> UnitDef:
    """Return the unit the results of arithmetic of `kind` display in."""
    own = "_result_unit" in vars(kind)
    return kind._result_unit if own else kind._canonical_unit  # noqa: SLF001 -- the kind's own units


def _rule(
    left: _Kind,
    operation: Literal["*", "/"],
    right: _Kind,
    result: _Kind,
) -> None:
    """Declare that `left <operation> right` is a `result`.

    A product holds in both operand orders.
    The operands are registered linear kinds with a dimension, and a role may be one.
    The result is the principal kind of the dimension the operation produces, one of its
    contested kinds, or a role of a kind of that dimension.
    A role is reached by explicit construction and left by a named conversion, so only
    a rule that names it makes arithmetic produce or take one.
    `AbsorbedDoseRate * Time` is an `AbsorbedDose` because a rule says so, and
    `AbsorbedDoseRate * Mass` is refused.

    Raises `TypeError` for a rule that does not fit or contradicts another, and
    `RuntimeError` once the registry is closed.
    A refused rule leaves the table unchanged.
    """
    if _closed:
        msg = (
            f"cannot add a rule for {left.__name__} {operation} {right.__name__}: the "
            "dimension registry is closed once `kuchka` has finished importing."
        )
        raise RuntimeError(msg)
    if operation not in ("*", "/"):
        msg = f"an operation is '*' or '/', not {operation!r}."
        raise TypeError(msg)
    for operand in (left, right):
        if not (_is_registered(operand) and _is_arithmetic_kind(operand)):
            msg = (
                f"{operand.__name__} cannot be an operand of a rule: an operand is a "
                "registered linear kind with a dimension."
            )
            raise TypeError(msg)
    dimension = (
        left.dimension * right.dimension
        if operation == "*"
        else left.dimension / right.dimension
    )
    if result.dimension != dimension or not (
        result in _arithmetic_roots(dimension) or result in _SPECIALISATIONS
    ):
        names = ", ".join(kind.__name__ for kind in _arithmetic_roots(dimension))
        msg = (
            f"{left.__name__} {operation} {right.__name__} has dimension "
            f"{dimension!r}, so {result.__name__} cannot be its result: the result is "
            f"the principal kind or a contested kind of that dimension "
            f"({names or 'none registered'}), or a role of one."
        )
        raise TypeError(msg)
    for key in _declared_keys(left, operation, right, result):
        _RULES[key] = result


def _declared_keys(
    left: _Kind, operation: Literal["*", "/"], right: _Kind, result: _Kind
) -> list[tuple[_Kind, str, _Kind]]:
    """Return the keys a rule or a bridge is entered under, both orders for a product.

    Raises `TypeError` when a rule or a bridge already gives another result for one.
    """
    keys: list[tuple[_Kind, str, _Kind]] = [(left, operation, right)]
    if operation == "*" and left is not right:
        keys.append((right, operation, left))
    for key in keys:
        known = _BRIDGES[key][0] if key in _BRIDGES else _RULES.get(key)
        if known is not None and known is not result:
            msg = (
                f"{left.__name__} {operation} {right.__name__} is already "
                f"{known.__name__}, not {result.__name__}."
            )
            raise TypeError(msg)
    return keys


def _bridge(
    left: _Kind,
    operation: Literal["*", "/"],
    right: _Kind,
    result: _Kind,
) -> None:
    """Declare that `left <operation> right` is a `result`, across the angle axis.

    The result differs from the plain product or quotient on the angle axis alone, and
    the factor follows from the two angle exponents (see `_BRIDGES`).
    A product holds in both operand orders.
    The operands and the result are principal or contested kinds, and the plain
    product or quotient has a dimension, since `Frequency * Time` counts cycles.
    That the plain dimension has no arithmetic kind is checked when the registry
    closes, since a later module may register one.

    Raises `TypeError` for a bridge that does not fit or contradicts a rule or another
    bridge, and `RuntimeError` once the registry is closed.
    A refused bridge leaves the table unchanged.
    """
    if _closed:
        msg = (
            f"cannot add a bridge for {left.__name__} {operation} {right.__name__}: "
            "the dimension registry is closed once `kuchka` has finished importing."
        )
        raise RuntimeError(msg)
    if operation not in ("*", "/"):
        msg = f"an operation is '*' or '/', not {operation!r}."
        raise TypeError(msg)
    for kind in (left, right, result):
        if not (
            _is_arithmetic_kind(kind) and kind in _arithmetic_roots(kind.dimension)
        ):
            msg = (
                f"{kind.__name__} cannot take part in a bridge: its operands and its "
                "result are principal or contested kinds."
            )
            raise TypeError(msg)
    plain = _plain_dimension(left, operation, right)
    if plain == DIMENSIONLESS or not _differs_in_angle_alone(plain, result.dimension):
        msg = (
            f"{left.__name__} {operation} {right.__name__} has dimension {plain!r}, "
            f"so a bridge to {result.__name__} ({result.dimension!r}) does not fit: "
            "a bridge changes the angle exponent of a dimension, and nothing else."
        )
        raise TypeError(msg)
    factor = _TURN_IN_RADIANS ** (plain.angle - result.dimension.angle)
    for key in _declared_keys(left, operation, right, result):
        _BRIDGES[key] = (result, factor)


_TURN_IN_RADIANS = 2 * PI
"""The radians in a turn, the canonical angle: the base of every bridge factor."""


def _plain_dimension(left: _Kind, operation: str, right: _Kind) -> Dimension:
    """Return the dimension of `left <operation> right` by exponent arithmetic."""
    if operation == "*":
        return left.dimension * right.dimension
    return left.dimension / right.dimension


def _differs_in_angle_alone(first: Dimension, second: Dimension) -> bool:
    """Return whether two dimensions differ, and only in their angle exponent."""
    return first != second and replace(first, angle=0) == replace(second, angle=0)


def _check_bridges() -> None:
    """Refuse a bridge whose plain dimension has an arithmetic kind.

    A bridge adds a result where arithmetic had none, so a kind registered for its
    plain dimension conflicts with it.
    Raises `TypeError` naming the bridge and the kind.
    """
    for (left, operation, right), (result, _) in _BRIDGES.items():
        plain = _plain_dimension(left, operation, right)
        kinds = _arithmetic_roots(plain)
        if kinds:
            names = ", ".join(kind.__name__ for kind in kinds)
            msg = (
                f"the bridge {left.__name__} {operation} {right.__name__} -> "
                f"{result.__name__} conflicts with {names}, registered for its plain "
                f"dimension {plain!r}: a bridge fills a dimension with no kind."
            )
            raise TypeError(msg)


def _register_reciprocal(first: _Kind, second: _Kind) -> None:
    """Declare two specialisations as the reciprocals of each other.

    Raises `TypeError` for two kinds that are not specialisations whose product is
    dimensionless, and `RuntimeError` once the registry is closed.
    """
    if _closed:
        msg = (
            f"cannot make {first.__name__} and {second.__name__} reciprocals: the "
            "dimension registry is closed once `kuchka` has finished importing."
        )
        raise RuntimeError(msg)
    if (
        first not in _SPECIALISATIONS
        or second not in _SPECIALISATIONS
        or first.dimension * second.dimension != DIMENSIONLESS
    ):
        msg = (
            f"{first.__name__} and {second.__name__} cannot be reciprocals: both are "
            "specialisations, and their dimensions multiply to a dimensionless one."
        )
        raise TypeError(msg)
    _RECIPROCALS[first] = second
    _RECIPROCALS[second] = first


def _conversion_hint(role: _Kind) -> str:
    """Return how to leave a specialisation: its conversion, or that it has none."""
    kind = _SPECIALISATIONS[role]
    snake = "".join(f"_{c.lower()}" if c.isupper() else c for c in kind.__name__)
    name = f"to{snake}"
    if hasattr(role, name):
        return (
            f"`{role.__name__}` is a role of `{kind.__name__}`: call `.{name}()` to "
            f"take it as a `{kind.__name__}`."
        )
    return (
        f"`{role.__name__}` has no conversion to `{kind.__name__}`, so it combines "
        "only with a plain number, a dimensionless quantity, and itself in a quotient."
    )


def _reciprocal_role(
    left: LinearQuantity, right: LinearQuantity
) -> type[LinearQuantity] | None:
    """Return the kind of a dimensionless `left` over a specialisation `right`.

    It is the reciprocal specialisation, as for a plain number over `right`, and a
    specialisation with no reciprocal refuses.
    Returns `None` when `right` is not a specialisation.
    """
    right_kind = type(right)
    if right_kind not in _SPECIALISATIONS:
        return None
    reciprocal = _RECIPROCALS.get(right_kind)
    if reciprocal is None:
        hint = f"`{right_kind.__name__}` has no reciprocal kind to divide into."
        raise IncompatibleDimensionError("divide", left, right, hint=hint)
    return cast("type[LinearQuantity]", reciprocal)


def _refuse_a_role(
    operation: Literal["*", "/"], left: LinearQuantity, right: LinearQuantity
) -> None:
    """Raise `IncompatibleDimensionError` for a specialisation used out of its role."""
    left_kind, right_kind = type(left), type(right)
    roles = [kind for kind in (left_kind, right_kind) if kind in _SPECIALISATIONS]
    if not roles or DIMENSIONLESS in (left.dimension, right.dimension):
        return
    if operation == "/" and left_kind is right_kind:
        return
    if operation == "*" and _RECIPROCALS.get(left_kind) is right_kind:
        return
    if (left_kind, operation, right_kind) in _RULES:
        return
    hint = " ".join(_conversion_hint(role) for role in dict.fromkeys(roles))
    verb = "multiply" if operation == "*" else "divide"
    raise IncompatibleDimensionError(verb, left, right, hint=hint)


def _register_ratio(quantity_type: _Kind) -> None:
    """Declare `quantity_type` as the kind of a ratio of two like quantities.

    The type is a registered linear kind of the dimensionless dimension.

    Raises `TypeError` for a type that does not fit and `RuntimeError` once the
    registry is closed.
    """
    if _closed:
        msg = (
            f"cannot make {quantity_type.__name__} the ratio kind: the dimension "
            "registry is closed once `kuchka` has finished importing."
        )
        raise RuntimeError(msg)
    from kuchka.quantities.base import LinearQuantity  # noqa: PLC0415 -- same cycle

    if (
        not issubclass(quantity_type, LinearQuantity)
        or quantity_type.dimension != DIMENSIONLESS
        or not _is_registered(quantity_type)
    ):
        msg = (
            f"{quantity_type.__name__} cannot be the ratio kind: it is a registered "
            "linear kind of the dimensionless dimension."
        )
        raise TypeError(msg)
    _RATIO_KIND[DIMENSIONLESS] = quantity_type


def _ratio(magnitude: Fraction) -> LinearQuantity:
    """Return `magnitude` as the ratio kind, displayed in its coherent unit."""
    ratio_type = cast("type[LinearQuantity]", _RATIO_KIND[DIMENSIONLESS])
    return ratio_type(magnitude, _result_unit(ratio_type))


def _is_ratio(
    operation: Literal["*", "/"], left: LinearQuantity, right: LinearQuantity
) -> bool:
    """Return whether `left <operation> right` is a ratio of like quantities."""
    if operation == "/":
        return left.dimension == right.dimension
    return left.dimension == right.dimension == DIMENSIONLESS


def _result_kind(
    operation: Literal["*", "/"], left: _Kind, right: _Kind
) -> _Kind | None:
    """Return the kind that `left <operation> right` has, if a rule decides it.

    A dimensionless operand leaves the kind of the other operand as it is, so a
    `SampleRate` scaled by a `Proportion` is still a `SampleRate`.
    Otherwise an explicit rule decides, and `None` leaves it to the dimension.
    """
    if right.dimension == DIMENSIONLESS:
        return left
    if left.dimension == DIMENSIONLESS and operation == "*":
        return right
    return _RULES.get((left, operation, right))


def _combine(
    operation: Literal["*", "/"],
    left: LinearQuantity,
    right: LinearQuantity,
    magnitude: Fraction,
) -> LinearQuantity | Fraction:
    """Build the correctly-typed result of multiplying or dividing two quantities.

    A specialisation is refused unless it is scaled by a dimensionless operand,
    divided by itself, multiplied by its reciprocal, or named by a rule; a dimensionless
    operand over a specialisation is its reciprocal specialisation.
    Then, in order: a ratio of like quantities is the ratio kind; any other
    dimensionless result is a plain ``Fraction``; a dimensionless operand keeps the
    other operand's kind; an explicit rule names the kind; otherwise the dimension
    decides (see `_promote`).
    """
    _refuse_a_role(operation, left, right)
    if operation == "/" and left.dimension == DIMENSIONLESS:
        reciprocal = _reciprocal_role(left, right)
        if reciprocal is not None:
            return reciprocal(magnitude, _result_unit(reciprocal))
    dimension = (
        left.dimension * right.dimension
        if operation == "*"
        else left.dimension / right.dimension
    )
    if dimension == DIMENSIONLESS:
        ratio_kind = _RATIO_KIND.get(DIMENSIONLESS)
        if ratio_kind is None or not _is_ratio(operation, left, right):
            return magnitude
        return _ratio(magnitude)
    bridged = _BRIDGES.get((type(left), operation, type(right)))
    if bridged is not None:
        bridge_kind, factor = bridged
        result_type = cast("type[LinearQuantity]", bridge_kind)
        return result_type(magnitude * factor, _result_unit(result_type))
    kind = _result_kind(operation, type(left), type(right))
    if kind is None:
        return _promote(dimension, magnitude)
    result_kind = cast("type[LinearQuantity]", kind)
    return result_kind(magnitude, _result_unit(result_kind))


def _concrete_kinds() -> list[_Kind]:
    """Return every concrete quantity type that has been defined."""
    return [cast("_Kind", kind) for kind in _concrete_types()]


def _close() -> None:
    """Close the registry: later registrations raise `RuntimeError`.

    Called once, when the package has imported every quantity module.
    Every concrete quantity type, of any shape and dimension, has to be a registered
    kind by then.
    Raises `TypeError` naming the types that are not.
    """
    global _closed  # noqa: PLW0603 -- one-way switch, set once at the end of the import
    if _closed:
        return
    unregistered = sorted(
        kind.__name__ for kind in _concrete_kinds() if not _is_registered(kind)
    )
    if unregistered:
        msg = (
            f"{', '.join(unregistered)} are not registered for their dimension: each "
            "quantity module registers its types while it is imported."
        )
        raise TypeError(msg)
    _check_bridges()
    _closed = True


def _promote(dimension: Dimension, magnitude: Fraction) -> LinearQuantity | Fraction:
    """Build the result of a multiplication or division from its dimension alone.

    A dimensionless result is returned as a plain ``Fraction``: the ratio of two like
    quantities is built by `_combine`, which knows the operands.
    The principal kind of the dimension is the result; a contested dimension raises
    `AmbiguousKindError`, because no kind of it is the general one.
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
        raise UnrepresentableDimensionError(
            dimension, hint=_angle_neighbours(dimension)
        ) from None
    return quantity_type(magnitude, _result_unit(quantity_type))


def _angle_neighbours(dimension: Dimension) -> str | None:
    """Describe the kinds `dimension` differs from on the angle axis alone.

    Names each kind with the angle exponent between them, nearest first, and the
    bridges that give it.
    Returns `None` when no kind is that close.
    """
    neighbours = sorted(
        (
            kind
            for other in (*_DIMENSION_REGISTRY, *_CONTESTED)
            if _differs_in_angle_alone(dimension, other)
            for kind in _arithmetic_roots(other)
        ),
        key=lambda kind: abs(dimension.angle - kind.dimension.angle),
    )
    lines = []
    for kind in neighbours:
        offset = replace(DIMENSIONLESS, angle=dimension.angle - kind.dimension.angle)
        line = f"It differs from `{kind.__name__}` by {offset!r} alone"
        routes = _bridges_to(kind)
        if routes:
            line += f", and {' and '.join(routes)} gives one"
        lines.append(f"{line}.")
    return "\n".join(lines) or None


def _bridges_to(kind: _Kind) -> list[str]:
    """Return each bridge that gives `kind`, a product written in one operand order."""
    routes: list[str] = []
    for (left, operation, right), (result, _) in _BRIDGES.items():
        reverse = f"`{right.__name__} {operation} {left.__name__}`"
        if result is kind and not (operation == "*" and reverse in routes):
            routes.append(f"`{left.__name__} {operation} {right.__name__}`")
    return routes


__all__: list[str] = []
