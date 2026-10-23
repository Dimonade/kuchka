"""kuchka -- a small pile of physically-typed units for engineering code.

    from kuchka import Volt, Milliampere

    voltage = Volt(4.2)
    current = Milliampere(150)
    power = voltage * current   # -> Power, computed and typed automatically

Two-tier export policy:
  - kuchka (this package): unit constructors (Volt, Tonne, ...), semantic quantity
  types (Voltage, Temperature, ...), the errors, and `parse` with its `ArchaicPolicy`.
  - kuchka.units / kuchka.quantities: the complete surface, including raw `UnitDef`
  constants (VOLT, KILOVOLT, ...) and `*_UNITS` boundary tables.
  _see docs/examples/config_migration for why those exist and who needs them._

Historical units live in `kuchka.units.archaic`, outside both tiers, and are imported
explicitly from the module of their tradition.

The promoted names are listed in `kuchka._api`, which `tools/generate_api.py` derives
from the `__all__` of the leaf modules under `kuchka.units` and `kuchka.quantities`.
Those lists are the only place a name is typed: a new unit constructor or quantity
type reaches the top level by being added to its leaf module and running
`just generate-api`.
`tests/test_generated_api.py` fails when the generated file is out of date, and
`tests/test_public_api_surface.py` checks the two-tier policy independently, so a
UnitDef or table can't quietly leak up a level.
"""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version

from kuchka import _api
from kuchka import errors
from kuchka import parsing
from kuchka._api import *
from kuchka.constants import codata_2022
from kuchka.errors import *
from kuchka.parsing import *
from kuchka.quantities.base.registry import _close

try:
    __version__ = version("kuchka")
except PackageNotFoundError:  # pragma: no cover -- running from an uninstalled checkout
    __version__ = "0.0.0+unknown"

_close()

__all__: list[str] = ["__version__", "codata_2022"]
__all__ += _api.__all__
__all__ += errors.__all__
__all__ += parsing.__all__
