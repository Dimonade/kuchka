"""Magnetization is a distinct quantity type that uses the ampere-per-metre units.

Magnetization (M) is the magnetic dipole moment per unit volume of a material.
It has the same dimension and unit as magnetic field strength (H), but they are
different physical quantities: H is the magnetising field set by free currents, and M is
the material's own magnetic response to the total field.
In SI, magnetic flux density relates to both as B = μ0(H + M).

No unit definitions live here: `kuchka.units.electromagnetics.magnetic_field_strength`
owns the ampere per metre and its multiples.
Each entry of `MAGNETIZATION_UNITS` reads the corresponding field-strength constructor's
result through `MagneticFieldStrength.to_magnetization()`.
That conversion preserves the numerical reading and changes its quantity kind.
`Magnetization.to_magnetic_field_strength()` converts back, which is how a magnetization
joins an applied field or meets a permeability.

Ferromagnets retain magnetization after the applied field is removed, and it approaches
a saturation value as the moments align.
It also depends on temperature and on magnetic history, so the value at a given applied
field can depend on how that field was reached.

Examples
--------
Near room temperature, iron has a saturation magnetization of about 1.71 MA/m.
An iron core in a solenoid with an applied field of 7.5 kA/m is close to saturation,
so the total flux density is B = μ0(H + M).
Adding the two needs the same kind on both sides, which makes the step explicit:

>>> from kuchka import KiloamperePerMetre, MicrohenryPerMetre
>>> from kuchka.units.electromagnetics.magnetic_flux_density import TESLA
>>> from kuchka.units.electromagnetics.magnetization import MAGNETIZATION_UNITS
>>> applied = KiloamperePerMetre(7.5)
>>> iron_saturation = MAGNETIZATION_UNITS["MA/m"](1.71)
>>> vacuum_permeability = MicrohenryPerMetre(1.25663706127)
>>> total = applied + iron_saturation.to_magnetic_field_strength()
>>> f"{(vacuum_permeability * total).to(TESLA):.3f}"
'2.158 T'

The magnetization contributes almost all of it: the applied field alone would give
about 9.4 mT.
The value is an upper estimate for a core at saturation, since the real magnetization
depends on the core material, its temperature, and its magnetic history.

A paleomagnetist demagnetizes a rock core in steps of alternating field.
The natural remanent magnetization along the measured axis falls from 0.12 A/m to
0.03 A/m, and the ratio gives the fraction that survives treatment:

>>> from kuchka.units.proportion import PERCENT
>>> before = MAGNETIZATION_UNITS["A/m"](0.12)
>>> after = MAGNETIZATION_UNITS["A/m"](0.03)
>>> (after / before).to(PERCENT)
25 %

The readings are illustrative.
Such measurements let researchers investigate the history of Earth's magnetic field
recorded by rocks.

Notes
-----
`MAGNETIZATION_UNITS` accepts the same spellings as `MAGNETIC_FIELD_STRENGTH_UNITS`.
It is intended for boundary code that reads magnetization from material
characterisation, geological surveys, and magnetic simulation data.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.quantities import Magnetization
from kuchka.units.electromagnetics.magnetic_field_strength import AMPERE_PER_METRE
from kuchka.units.electromagnetics.magnetic_field_strength import (
    MAGNETIC_FIELD_STRENGTH_UNITS,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from kuchka.internal.unit_table import UnitTable
    from kuchka.numeric import Numeric
    from kuchka.quantities import MagneticFieldStrength

Magnetization._canonical_unit = AMPERE_PER_METRE  # noqa: SLF001 -- reused from MagneticFieldStrength's own AMPERE_PER_METRE


def _via_field_strength(
    constructor: Callable[[Numeric], MagneticFieldStrength],
) -> Callable[[Numeric], Magnetization]:
    """Wrap a field-strength constructor so it reads its result as a `Magnetization`."""

    def read_as_magnetization(value: Numeric) -> Magnetization:
        return constructor(value).to_magnetization()

    return read_as_magnetization


MAGNETIZATION_UNITS: UnitTable[Magnetization] = MAGNETIC_FIELD_STRENGTH_UNITS.map(
    "MAGNETIZATION_UNITS", _via_field_strength
)

__all__ = ["MAGNETIZATION_UNITS"]
