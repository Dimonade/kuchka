"""Enforces the two-tier export policy stated in kuchka/__init__.py's docstring.

Both directions matter:
a constructor or quantity type that exists a level down but never made it to the top
level, and a UnitDef or *_UNITS table that leaked up when it shouldn't have.

kuchka/__init__.py itself stays hand-written;
this only checks it against the auto-complete surface one level down.
"""

from __future__ import annotations

import kuchka
from kuchka import constants
from kuchka import errors
from kuchka import quantities as quantities_pkg
from kuchka import units as units_pkg
from kuchka.quantities.base import AffineQuantity
from kuchka.quantities.base import AffineUnitDef
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base import LogarithmicUnitDef
from kuchka.quantities.base import ModularQuantity
from kuchka.quantities.base import PureLogarithmicQuantity
from kuchka.quantities.base import UnitDef


def _is_unit_constructor(name: str, value: object) -> bool:
    """Callable that builds a quantity from a plain number, e.g. Volt, Tonne."""
    return callable(value) and not isinstance(value, type) and not name.isupper()


def _is_boundary_only(name: str, value: object) -> bool:
    """`*UnitDef` constant or a *_UNITS table: kuchka.units-level, never top-level."""
    return isinstance(
        value, (UnitDef, AffineUnitDef, LogarithmicUnitDef)
    ) or name.endswith("_UNITS")


def test_every_unit_constructor_is_reachable_from_top_level() -> None:
    for name in units_pkg.__all__:
        value = getattr(units_pkg, name)
        if _is_boundary_only(name, value):
            continue
        if _is_unit_constructor(name, value):
            assert hasattr(kuchka, name), (
                f"{name} is a constructor in kuchka.units but missing from "
                f"top-level kuchka -- promote it or document why not present."
            )


_QUANTITY_TYPE_EXTRAS = {"ConvertibleToFrequency"}
"""ConvertibleToFrequency is a Protocol.

It is not a subclass of any of the three quantity bases, and named explicitly since
it's currently the only exception this policy has.
"""
_QUANTITY_BASES = (
    LinearQuantity,
    AffineQuantity,
    ModularQuantity,
    PureLogarithmicQuantity,
)
_INTERNAL_MACHINERY = (
    LinearQuantity,
    AffineQuantity,
    ModularQuantity,
    PureLogarithmicQuantity,
    UnitDef,
    AffineUnitDef,
    LogarithmicUnitDef,
)


def test_every_quantity_type_is_reachable_from_top_level() -> None:
    for name in quantities_pkg.__all__:
        value = getattr(quantities_pkg, name)
        if value in _INTERNAL_MACHINERY:
            continue  # the generic engine itself, deliberately not top-level
        is_quantity_type = isinstance(value, type) and issubclass(
            value, _QUANTITY_BASES
        )
        if is_quantity_type or name in _QUANTITY_TYPE_EXTRAS:
            assert hasattr(kuchka, name), (
                f"{name} is a quantity type in kuchka.quantities but missing "
                f"from top-level kuchka."
            )


def test_no_unitdef_or_units_table_leaks_to_top_level() -> None:
    for name in dir(kuchka):
        if name.startswith("_"):
            continue
        value = getattr(kuchka, name)
        assert not isinstance(value, (UnitDef, AffineUnitDef, LogarithmicUnitDef)), (
            f"{name} is a unit-definition constant; it belongs at kuchka.units only."
        )
        assert not name.endswith("_UNITS"), (
            f"{name} is a boundary table; it belongs at kuchka.units only."
        )


def test_every_constant_is_reachable_from_top_level() -> None:
    for name in constants.__all__:
        assert hasattr(kuchka, name), (
            f"{name} is defined in kuchka.constants but missing from top-level kuchka."
        )


def test_every_fundamental_constant_is_reachable_from_the_dataset_namespace() -> None:
    """A constant added to `fundamental.py` must not go quietly unexported.

    `kuchka.constants.codata_2022` hand-lists its re-exports rather than
    wildcard-aggregating `fundamental.py` (see that module's own docstring for why),
    so nothing stops a new constant from being added to `fundamental.py` without a
    matching import/`__all__` entry here -- this walks `fundamental.__all__`, the
    actual source of truth, rather than `codata_2022.__all__` against itself, which
    would only prove the hand-written list is internally consistent, not complete.
    """
    from kuchka.constants import codata_2022
    from kuchka.constants.codata_2022 import fundamental

    for name in fundamental.__all__:
        assert name in codata_2022.__all__, (
            f"{name} is defined in kuchka.constants.codata_2022.fundamental but "
            f"missing from kuchka.constants.codata_2022.__all__ -- add the import "
            f"and the __all__ entry."
        )
        assert hasattr(codata_2022, name), (
            f"{name} is listed in kuchka.constants.codata_2022.__all__ but is not "
            f"actually imported there."
        )
        assert getattr(codata_2022, name) is getattr(fundamental, name), (
            f"{name} on kuchka.constants.codata_2022 is not the same object as "
            f"kuchka.constants.codata_2022.fundamental.{name} -- check for a stale "
            f"or shadowed re-export."
        )
        assert hasattr(kuchka.codata_2022, name), (
            f"{name} is a CODATA 2022 constant but missing from "
            f"kuchka.codata_2022, the top-level re-export of the submodule."
        )


def test_every_error_is_reachable_from_top_level() -> None:
    for name in errors.__all__:
        assert hasattr(kuchka, name), (
            f"{name} is defined in kuchka.errors but missing from top-level kuchka."
        )
