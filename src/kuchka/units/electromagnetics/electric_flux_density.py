"""Electric flux density units: the coulomb-per-area units, read as a flux density.

The electric flux density (D), also called the electric displacement field, is the free
charge per area a field displaces: in a linear medium `D = εE`.
Its SI unit is the coulomb per square metre (C/m²), the unit of surface charge density.

In `kuchka`'s quantity-kind model, `ElectricFluxDensity` is registered as a role of
`SurfaceChargeDensity`.
The two types share a dimension and units, and the role conversion keeps the numerical
reading.

No unit definitions live here: `kuchka.units.electromagnetics.surface_charge_density`
owns the coulomb per square metre and its multiples.
Each entry of `ELECTRIC_FLUX_DENSITY_UNITS` reads the corresponding constructor's result
through `SurfaceChargeDensity.to_electric_flux_density()`.
The ampere-hour units of battery capacity have no entry.

Examples
--------
A field of 2 kV/m in a medium of permittivity 8.85 pF/m displaces 17.7 nC/m²:

>>> from kuchka import KilovoltPerMetre
>>> from kuchka import PicofaradPerMetre
>>> flux = PicofaradPerMetre(8.85) * KilovoltPerMetre(2)
>>> flux.to_surface_charge_density().to(NANOCOULOMB_PER_SQUARE_METRE)
17.7 nC/m²

A 10 µC/cm² displacement through a 2 cm² electrode area encloses 20 µC:

>>> from kuchka import SquareCentimetre
>>> ELECTRIC_FLUX_DENSITY_UNITS["uC/cm2"](10) * SquareCentimetre(2)
0.00002 C

`ELECTRIC_FLUX_DENSITY_UNITS` accepts the spellings of the matching
`SURFACE_CHARGE_DENSITY_UNITS` entries, for boundary code that reads a displacement
field from simulation or measurement data.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.internal.unit_table import unit_table
from kuchka.quantities import ElectricFluxDensity
from kuchka.units.electromagnetics.surface_charge_density import (
    COULOMB_PER_SQUARE_CENTIMETRE,
)
from kuchka.units.electromagnetics.surface_charge_density import (
    COULOMB_PER_SQUARE_METRE,
)
from kuchka.units.electromagnetics.surface_charge_density import (
    MICROCOULOMB_PER_SQUARE_CENTIMETRE,
)
from kuchka.units.electromagnetics.surface_charge_density import (
    MICROCOULOMB_PER_SQUARE_METRE,
)
from kuchka.units.electromagnetics.surface_charge_density import (
    MILLICOULOMB_PER_SQUARE_CENTIMETRE,
)
from kuchka.units.electromagnetics.surface_charge_density import (
    MILLICOULOMB_PER_SQUARE_METRE,
)
from kuchka.units.electromagnetics.surface_charge_density import (
    NANOCOULOMB_PER_SQUARE_METRE,
)
from kuchka.units.electromagnetics.surface_charge_density import (
    CoulombPerSquareCentimetre,
)
from kuchka.units.electromagnetics.surface_charge_density import CoulombPerSquareMetre
from kuchka.units.electromagnetics.surface_charge_density import (
    MicrocoulombPerSquareCentimetre,
)
from kuchka.units.electromagnetics.surface_charge_density import (
    MicrocoulombPerSquareMetre,
)
from kuchka.units.electromagnetics.surface_charge_density import (
    MillicoulombPerSquareCentimetre,
)
from kuchka.units.electromagnetics.surface_charge_density import (
    MillicoulombPerSquareMetre,
)
from kuchka.units.electromagnetics.surface_charge_density import (
    NanocoulombPerSquareMetre,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from kuchka.numeric import Numeric
    from kuchka.quantities import SurfaceChargeDensity

ElectricFluxDensity._canonical_unit = COULOMB_PER_SQUARE_METRE  # noqa: SLF001 -- reused from SurfaceChargeDensity's own coulomb per square metre


def _via_surface_charge_density(
    constructor: Callable[[Numeric], SurfaceChargeDensity],
) -> Callable[[Numeric], ElectricFluxDensity]:
    """Wrap a charge-density constructor so it reads its result as a flux density."""

    def read_as_flux_density(value: Numeric) -> ElectricFluxDensity:
        return constructor(value).to_electric_flux_density()

    return read_as_flux_density


ELECTRIC_FLUX_DENSITY_UNITS = unit_table(
    "ELECTRIC_FLUX_DENSITY_UNITS",
    {
        COULOMB_PER_SQUARE_METRE: _via_surface_charge_density(CoulombPerSquareMetre),
        MILLICOULOMB_PER_SQUARE_METRE: _via_surface_charge_density(
            MillicoulombPerSquareMetre
        ),
        MICROCOULOMB_PER_SQUARE_METRE: _via_surface_charge_density(
            MicrocoulombPerSquareMetre
        ),
        NANOCOULOMB_PER_SQUARE_METRE: _via_surface_charge_density(
            NanocoulombPerSquareMetre
        ),
        COULOMB_PER_SQUARE_CENTIMETRE: _via_surface_charge_density(
            CoulombPerSquareCentimetre
        ),
        MILLICOULOMB_PER_SQUARE_CENTIMETRE: _via_surface_charge_density(
            MillicoulombPerSquareCentimetre
        ),
        MICROCOULOMB_PER_SQUARE_CENTIMETRE: _via_surface_charge_density(
            MicrocoulombPerSquareCentimetre
        ),
    },
)

__all__ = ["ELECTRIC_FLUX_DENSITY_UNITS"]
