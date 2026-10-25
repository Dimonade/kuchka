"""Every package exports a clean composition of the `__all__` of its parts."""

from __future__ import annotations

import importlib
import pkgutil
import types

import pytest

import kuchka

PACKAGES = [
    kuchka,
    kuchka.units,
    kuchka.units.electromagnetics,
    kuchka.units.geometry,
    kuchka.units.information,
    kuchka.units.kinematics,
    kuchka.units.mechanics,
    kuchka.units.radiation,
    kuchka.units.temporal,
    kuchka.quantities,
    kuchka.quantities.electromagnetics,
    kuchka.quantities.geometry,
    kuchka.quantities.information,
    kuchka.quantities.kinematics,
    kuchka.quantities.mechanics,
    kuchka.quantities.radiation,
    kuchka.quantities.base,
    kuchka.constants,
    kuchka.errors,
]
PACKAGE_IDS = [package.__name__ for package in PACKAGES]
EXPLICIT_ONLY = "archaic"
"""The subpackage applications import explicitly, so no package re-exports it."""
AGGREGATING_PACKAGES = [
    kuchka.units,
    kuchka.units.electromagnetics,
    kuchka.units.geometry,
    kuchka.units.information,
    kuchka.units.kinematics,
    kuchka.units.mechanics,
    kuchka.units.radiation,
    kuchka.units.temporal,
    kuchka.quantities,
    kuchka.quantities.electromagnetics,
    kuchka.quantities.geometry,
    kuchka.quantities.information,
    kuchka.quantities.kinematics,
    kuchka.quantities.mechanics,
    kuchka.quantities.radiation,
]


@pytest.mark.parametrize("package", PACKAGES, ids=PACKAGE_IDS)
def test_all_names_resolve_and_are_unique(package: types.ModuleType) -> None:
    names = package.__all__
    assert len(names) == len(set(names)), f"duplicates in {package.__name__}.__all__"
    for name in names:
        assert hasattr(package, name), f"{package.__name__}.__all__ lists {name}"


@pytest.mark.parametrize(
    "package",
    [*AGGREGATING_PACKAGES, kuchka.quantities.base, kuchka.errors],
    ids=lambda package: package.__name__,
)
def test_all_exports_no_module_and_no_future_feature(package: types.ModuleType) -> None:
    # `kuchka` and `kuchka.constants` are left out on purpose: both export the
    # `codata_2022` dataset namespace, a module that is part of their surface.
    for name in package.__all__:
        value = getattr(package, name)
        assert not isinstance(value, types.ModuleType), (
            f"{package.__name__}.__all__ exports the module {name}"
        )
        assert name != "annotations", (
            f"{package.__name__}.__all__ exports `annotations`"
        )


def _leaf_exports(package: types.ModuleType) -> set[str]:
    """Union of the `__all__` of every module and subpackage directly inside it."""
    names: set[str] = set()
    for info in pkgutil.iter_modules(package.__path__):
        if info.name == EXPLICIT_ONLY:
            continue
        names |= set(importlib.import_module(f"{package.__name__}.{info.name}").__all__)
    return names


@pytest.mark.parametrize(
    "package", AGGREGATING_PACKAGES, ids=[p.__name__ for p in AGGREGATING_PACKAGES]
)
def test_package_all_is_the_union_of_its_leaves(package: types.ModuleType) -> None:
    assert set(package.__all__) == _leaf_exports(package), (
        f"{package.__name__}.__all__ is out of step with its leaf modules: "
        "a leaf is missing from the package's imports and `__all__ +=` lines."
    )
