"""Importing any entry point of the package leaves every quantity type complete.

The canonical unit of a type is bound by the unit module that defines it, so a type
must not stay incomplete because of the order in which modules are imported.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

import kuchka

# Independent of which module is imported first.

ENTRY_POINTS = [
    "kuchka",
    "kuchka.errors",
    "kuchka.constants",
    "kuchka.quantities",
    "kuchka.quantities.base",
    "kuchka.quantities.base.registry",
    "kuchka.units",
    "kuchka.units.electromagnetics.voltage",
    "kuchka.units.temporal.time",
]

CHECK = """
import importlib, sys
importlib.import_module(sys.argv[1])
from kuchka.quantities.base.storage import _ScalarStorage

def concrete(base):
    for sub in base.__subclasses__():
        if "dimension" in vars(sub):
            yield sub
        yield from concrete(sub)

unbound = (c for c in concrete(_ScalarStorage) if "_canonical_unit" not in vars(c))
missing = sorted(c.__name__ for c in unbound)
print(",".join(missing) or "complete")
"""


@pytest.mark.parametrize("module", ENTRY_POINTS)
def test_importing_any_entry_point_leaves_every_type_complete(module: str) -> None:
    location = str(Path(kuchka.__file__).resolve().parent.parent)
    environment = {**os.environ, "PYTHONPATH": location}
    result = subprocess.run(
        [sys.executable, "-c", CHECK, module],
        capture_output=True,
        text=True,
        check=True,
        env=environment,
    )
    assert result.stdout.strip() == "complete"
