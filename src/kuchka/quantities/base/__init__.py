"""The generic quantity engine shared by every physically-typed quantity.

This is a package that is split by responsibility so it can keep growing
(more algebraic shapes: modular/circular, logarithmic, ...) by organically
extracting new features into modules:

- `units.py` -- the unit-definition types (`UnitDef`, `AffineUnitDef`) and the
  structural `_DisplayUnit` protocol tying them together.
- `storage.py` -- `_ScalarStorage`, the immutable state, pickling, and text
  rendering every scalar-valued quantity needs regardless of its arithmetic shape.
  Implements no operator at all.
- `ordering.py` -- `_OrderedScalarMixin`, equality/hashing/total-order for shapes
  where "greater than" is unambiguous.
  Deliberately not part of `_ScalarStorage`, so a shape with no total order, like
  modular/circular quantity, can build on the same storage without inheriting
  comparisons it would have to un-implement.
- `registry.py` -- the dimension-to-type registry (`register`, `_promote`) that
  lets e.g. ``Volt(5) * Ampere(2)`` come back as a real `Power` instance.
- `linear.py` -- `LinearQuantity`: units differ by a pure scale factor.
- `affine.py` -- `AffineQuantity`: units differ by both a scale and an offset, so
  the quantity is a point on a scale and not a vector (`Temperature`).
- `modular.py` -- `ModularQuantity`: the quantity wraps around after a fixed
  period, so it is a position on a circle and not a point on a line (`Angle`).
- `logarithmic.py` -- `PureLogarithmicQuantity`: the quantity is the logarithm of a
  ratio, so combining two of them multiplies the ratios they describe
  (`LogarithmicRatio`).

Every name below is re-exported here so existing imports
(``from kuchka.quantities.base import LinearQuantity``) keep working exactly as
before the split -- this package's import surface is unchanged even though its
internals are now spread across several files.

NOTE: ``register`` is re-exported via the ``import x as x`` form and not by adding
it to ``__all__``: it needs to stay importable by name for every quantity module
(``from kuchka.quantities.base import register``), which ``mypy --strict``'s
``--no-implicit-reexport`` check requires to be spelled out explicitly, but it must
NOT appear in ``__all__``, since ``kuchka/quantities/__init__.py`` wildcard-imports
this package's ``__all__`` and would otherwise leak ``register`` -- internal
machinery -- up into ``kuchka.quantities``'s own public surface.
"""

from __future__ import annotations

from kuchka.quantities.base.affine import AffineQuantity
from kuchka.quantities.base.linear import LinearQuantity
from kuchka.quantities.base.logarithmic import PureLogarithmicQuantity
from kuchka.quantities.base.modular import ModularQuantity
from kuchka.quantities.base.registry import register as register
from kuchka.quantities.base.units import AffineUnitDef
from kuchka.quantities.base.units import LogarithmicUnitDef
from kuchka.quantities.base.units import UnitDef

__all__ = [
    "AffineQuantity",
    "AffineUnitDef",
    "LinearQuantity",
    "LogarithmicUnitDef",
    "ModularQuantity",
    "PureLogarithmicQuantity",
    "UnitDef",
]
