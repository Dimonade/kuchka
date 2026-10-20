"""Archaic units stay out of the library until a program imports them."""

from __future__ import annotations

import subprocess
import sys

PROGRAM = """
import sys
import kuchka
import kuchka.units
from kuchka.quantities import Length

def names():
    return {unit.name for unit in Length._applicable_units}

assert not [m for m in sys.modules if "archaic" in m], "archaic imported by kuchka"
assert "arshin" not in names()
assert not hasattr(kuchka, "Arshin") and "Arshin" not in kuchka.units.__all__

from kuchka.units.archaic.russian.length import Arshin

assert "arshin" in names()
assert Arshin(1).value_in(Arshin(1).unit) == 1
assert not hasattr(kuchka, "Arshin") and "Arshin" not in kuchka.units.__all__
"""


def test_a_unit_is_reachable_only_after_its_module_is_imported() -> None:
    result = subprocess.run(
        [sys.executable, "-c", PROGRAM], capture_output=True, text=True, check=False
    )
    assert result.returncode == 0, result.stderr
