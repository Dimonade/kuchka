"""Magnetization constructors, from microamperes per metre to megaamperes per metre.

Magnetization (M) is the magnetic dipole moment per unit volume of a material.
Its SI unit is the ampere per metre (A/m), the same unit as magnetic
field strength (H).
The two quantities are physically distinct: H describes the applied magnetic field,
while M describes the material's magnetic response.

In SI, magnetic flux density is related to both quantities by B = μ₀(H + M).
Ferromagnetic materials can retain magnetization after the applied field is removed,
and their magnetization approaches a saturation value as their magnetic moments become
increasingly aligned.

Examples
--------
A paleomagnetist measures a rock core before and after alternating-field
demagnetization.
The component along the measured axis falls from 0.12 A/m to 0.03 A/m.
The difference estimates the component removed by treatment:

>>> from kuchka import AmperePerMetre
>>> before_treatment = AmperePerMetre(0.12)
>>> after_treatment = AmperePerMetre(0.03)
>>> before_treatment - after_treatment
0.09 A/m

The readings are illustrative.
In practice, paleomagnetic measurements help researchers investigate the history of
Earth's magnetic field recorded by rocks.

Near room temperature, iron has a saturation magnetization of approximately 1.71 MA/m.
Multiplying this by vacuum permeability gives the μ₀M contribution to the
magnetic-flux-density relation, about 2.15 T:

>>> from kuchka import MegaamperePerMetre, MicrohenryPerMetre
>>> from kuchka.units.electromagnetics.magnetic_flux_density import TESLA
>>> iron_saturation = MegaamperePerMetre(1.71)
>>> vacuum_permeability = MicrohenryPerMetre(1.25663706127)
>>> (vacuum_permeability * iron_saturation).to(TESLA)
2.1488493747717 T

This is the μ₀M term, not a prediction of the total flux density in an arbitrary iron
specimen.
The applied field, sample geometry, and magnetic state also affect the measured result.

Notes
-----
Magnetization depends on material composition, temperature, magnetic history, and
applied field.
Ferromagnets exhibit hysteresis, so the magnetization at a given applied field can
depend on how that field was reached.

`MAGNETIZATION_UNITS` maps symbols such as ``"µA/m"``, ``"mA/m"``, ``"A/m"``,
``"kA/m"``, and ``"MA/m"`` to their constructors.
It is intended for boundary code that reads measurements from geological surveys,
material characterisation, and magnetic simulation data.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import MAGNETIZATION
from kuchka.internal import prefixes
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Magnetization

if TYPE_CHECKING:
    from kuchka.internal.unit_table import UnitTable

AMPERE_PER_METRE_NAME = "ampere_per_metre"
AMPERE_PER_METRE_SYMBOL = "A/m"
AMPERE_PER_METRE_WORDS = ("ampere per metre", "ampere per meter")
"""Spoken forms, which prefixed names follow: `milliampere per metre`."""

MICROAMPERE_PER_METRE = prefixed_unit(
    prefixes.MICRO,
    AMPERE_PER_METRE_NAME,
    AMPERE_PER_METRE_SYMBOL,
    MAGNETIZATION,
    base_words=AMPERE_PER_METRE_WORDS,
)
MILLIAMPERE_PER_METRE = prefixed_unit(
    prefixes.MILLI,
    AMPERE_PER_METRE_NAME,
    AMPERE_PER_METRE_SYMBOL,
    MAGNETIZATION,
    base_words=AMPERE_PER_METRE_WORDS,
)
AMPERE_PER_METRE = prefixed_unit(
    prefixes.UNIT,
    AMPERE_PER_METRE_NAME,
    AMPERE_PER_METRE_SYMBOL,
    MAGNETIZATION,
    base_words=AMPERE_PER_METRE_WORDS,
)
KILOAMPERE_PER_METRE = prefixed_unit(
    prefixes.KILO,
    AMPERE_PER_METRE_NAME,
    AMPERE_PER_METRE_SYMBOL,
    MAGNETIZATION,
    base_words=AMPERE_PER_METRE_WORDS,
)
MEGAAMPERE_PER_METRE = prefixed_unit(
    prefixes.MEGA,
    AMPERE_PER_METRE_NAME,
    AMPERE_PER_METRE_SYMBOL,
    MAGNETIZATION,
    base_words=AMPERE_PER_METRE_WORDS,
)

Magnetization._canonical_unit = AMPERE_PER_METRE  # noqa: SLF001 -- this module owns Magnetization's canonical unit


def MicroamperePerMetre(value: Numeric) -> Magnetization:
    """Construct magnetization from a magnitude in microamperes per metre.

        Examples
    --------
    After background correction, a weakly magnetized specimen has a component of
    80 µA/m.
    A second measurement after treatment gives 30 µA/m.
    The difference is the component removed during treatment:

    >>> from kuchka import MicroamperePerMetre
    >>> initial = MicroamperePerMetre(80)
    >>> treated = MicroamperePerMetre(30)
    >>> initial - treated
    50 µA/m

    """
    return Magnetization(
        to_exact(value) * MICROAMPERE_PER_METRE.scale, MICROAMPERE_PER_METRE
    )


def MilliamperePerMetre(value: Numeric) -> Magnetization:
    """Construct magnetization from a magnitude in milliamperes per metre."""
    return Magnetization(
        to_exact(value) * MILLIAMPERE_PER_METRE.scale, MILLIAMPERE_PER_METRE
    )


def AmperePerMetre(value: Numeric) -> Magnetization:
    """Construct magnetization from a magnitude in amperes per metre."""
    return Magnetization(to_exact(value) * AMPERE_PER_METRE.scale, AMPERE_PER_METRE)


def KiloamperePerMetre(value: Numeric) -> Magnetization:
    """Construct magnetization from a magnitude in kiloamperes per metre."""
    return Magnetization(
        to_exact(value) * KILOAMPERE_PER_METRE.scale, KILOAMPERE_PER_METRE
    )


def MegaamperePerMetre(value: Numeric) -> Magnetization:
    """Construct magnetization from a magnitude in megaamperes per metre."""
    return Magnetization(
        to_exact(value) * MEGAAMPERE_PER_METRE.scale, MEGAAMPERE_PER_METRE
    )


MAGNETIZATION_UNITS: UnitTable[Magnetization] = unit_table(
    "MAGNETIZATION_UNITS",
    {
        MICROAMPERE_PER_METRE: MicroamperePerMetre,
        MILLIAMPERE_PER_METRE: MilliamperePerMetre,
        AMPERE_PER_METRE: AmperePerMetre,
        KILOAMPERE_PER_METRE: KiloamperePerMetre,
        MEGAAMPERE_PER_METRE: MegaamperePerMetre,
    },
)

__all__ = [
    "AMPERE_PER_METRE",
    "KILOAMPERE_PER_METRE",
    "MAGNETIZATION_UNITS",
    "MEGAAMPERE_PER_METRE",
    "MICROAMPERE_PER_METRE",
    "MILLIAMPERE_PER_METRE",
    "AmperePerMetre",
    "KiloamperePerMetre",
    "MegaamperePerMetre",
    "MicroamperePerMetre",
    "MilliamperePerMetre",
]
