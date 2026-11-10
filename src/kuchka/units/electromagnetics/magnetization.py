"""Magnetization units: the ampere-per-metre units, read as a magnetization.

Magnetization (M) is the magnetic dipole moment per unit volume of a material.
Its SI unit is the ampere per metre (A/m), the same unit as
magnetic field strength (H).
The quantities are physically distinct: H describes the magnetising field associated
with free currents, while M describes the material's magnetic response.

In SI, magnetic flux density is related to both by B = μ₀(H + M).
In `kuchka`'s quantity-kind model, `Magnetization` is registered as a role of
`MagneticFieldStrength`.
The two types share dimensions and units, while the role conversion preserves the
numerical reading.
It does not calculate magnetization from an applied field or assert that H and M are
the same physical quantity.

No unit definitions live here: `kuchka.units.electromagnetics.magnetic_field_strength`
owns the ampere per metre and its multiples.
Each entry of `MAGNETIZATION_UNITS` reads the corresponding field-strength
constructor's result through `MagneticFieldStrength.to_magnetization()`.
`Magnetization.to_magnetic_field_strength()` converts back to the field-strength role
when dimensional arithmetic needs H and M to be expressed as compatible terms in an
equation such as B = μ₀(H + M).

Examples
--------
Near room temperature, iron's saturation magnetization is approximately 1.71 MA/m.
To illustrate the SI relationship, consider a sample already at that magnetization with
an applied field strength of 7.5 kA/m.
Expressing the magnetization as a field-strength role allows the two A/m terms to be
combined before applying vacuum permeability:

>>> from kuchka import KiloamperePerMetre, MicrohenryPerMetre
>>> from kuchka.units.electromagnetics.magnetic_flux_density import TESLA
>>> from kuchka.units.electromagnetics.magnetization import MAGNETIZATION_UNITS
>>> applied = KiloamperePerMetre(7.5)
>>> iron_saturation = MAGNETIZATION_UNITS["MA/m"](1.71)
>>> vacuum_permeability = MicrohenryPerMetre(1.25663706127)
>>> total = applied + iron_saturation.to_magnetic_field_strength()
>>> (vacuum_permeability * total).to(TESLA)
2.158274152731225 T

The example assumes the specimen is already at saturation; it does not claim that the
applied field alone drives an arbitrary iron core to that state.
The applied-field contribution on its own is about 9.4 mT.

A paleomagnetist measures a rock core before and after alternating-field
demagnetization.
The magnetization component along the measured axis falls from 0.12 A/m to 0.03 A/m.
The remaining component is one quarter of the initial reading:

>>> from kuchka.units.proportion import PERCENT
>>> before = MAGNETIZATION_UNITS["A/m"](0.12)
>>> after = MAGNETIZATION_UNITS["A/m"](0.03)
>>> (after / before).to(PERCENT)
25 %

These readings are illustrative.
Paleomagnetic measurements of natural remanent magnetization help researchers
investigate the history of Earth's magnetic field recorded by rocks.

Notes
-----
Magnetization depends on material composition, temperature, applied field, and magnetic
history.
Ferromagnets exhibit hysteresis, so magnetization at a given applied field may depend
on how that field was reached.

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
