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
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base import UnitDef


def _is_boundary_only(name: str, value: object) -> bool:
    """UnitDef constant or a *_UNITS table: kuchka.units-level, never top-level."""
    return isinstance(value, UnitDef) or name.endswith("_UNITS")


def _is_unit_constructor(name: str, value: object) -> bool:
    """Callable that builds a quantity from a plain number, e.g. Volt, Tonne."""
    return callable(value) and not isinstance(value, type) and not name.isupper()


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


# ConvertibleToFrequency is a Protocol, not a LinearQuantity subclass and named
# explicitly, since it's currently the only exception this policy has.
_QUANTITY_TYPE_EXTRAS = {"ConvertibleToFrequency"}


def test_every_quantity_type_is_reachable_from_top_level() -> None:
    for name in quantities_pkg.__all__:
        value = getattr(quantities_pkg, name)
        if value in (LinearQuantity, UnitDef):
            continue  # internal machinery, deliberately not top-level
        is_quantity_type = isinstance(value, type) and issubclass(value, LinearQuantity)
        if is_quantity_type or name in _QUANTITY_TYPE_EXTRAS or name == "Temperature":
            assert hasattr(kuchka, name), (
                f"{name} is a quantity type in kuchka.quantities but missing "
                f"from top-level kuchka."
            )


def test_no_unitdef_or_units_table_leaks_to_top_level() -> None:
    for name in dir(kuchka):
        if name.startswith("_"):
            continue
        value = getattr(kuchka, name)
        assert not isinstance(value, UnitDef), (
            f"{name} is a UnitDef constant; it belongs at kuchka.units only"
        )
        assert not name.endswith("_UNITS"), (
            f"{name} is a boundary table; it belongs at kuchka.units only"
        )


def test_every_constant_is_reachable_from_top_level() -> None:
    for name in constants.__all__:
        assert hasattr(kuchka, name), (
            f"{name} is defined in kuchka.constants but missing from top-level kuchka."
        )


def test_every_error_is_reachable_from_top_level() -> None:
    for name in errors.__all__:
        assert hasattr(kuchka, name), (
            f"{name} is defined in kuchka.errors but missing from top-level kuchka."
        )
