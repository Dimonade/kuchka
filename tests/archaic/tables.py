"""Every `*_UNITS` table of the archaic units, discovered from the package."""

from __future__ import annotations

import importlib
import pkgutil
from typing import Any

from kuchka.internal.unit_table import UnitTable
from kuchka.units import archaic


def _discover() -> dict[str, UnitTable[Any]]:
    found: dict[str, UnitTable[Any]] = {}
    for info in pkgutil.walk_packages(archaic.__path__, f"{archaic.__name__}."):
        module = importlib.import_module(info.name)
        for name in getattr(module, "__all__", ()):
            value = getattr(module, name)
            if isinstance(value, UnitTable):
                found[f"{info.name.removeprefix(archaic.__name__ + '.')}.{name}"] = (
                    value
                )
    return found


ARCHAIC_TABLES: dict[str, UnitTable[Any]] = _discover()
"""Each table of an archaic module, keyed by its module path and name."""

TABLE_IDS: list[str] = list(ARCHAIC_TABLES)
