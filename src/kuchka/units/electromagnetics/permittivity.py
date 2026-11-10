"""Permittivity constructors: farads per metre, from pico to unit.

Permittivity (ε) describes how a dielectric responds to an electric field.
For a linear, isotropic material, electric displacement and field are related by
D = εE.
Absolute permittivity is measured in farads per metre (F/m).
Relative permittivity (εᵣ) is dimensionless, with ε = εᵣ ε₀.

F/m is also the dimension of capacitance per unit length, but these are distinct
physical quantities.
For example, the capacitance per metre of a coaxial cable depends on both the
dielectric permittivity and the conductor geometry.
This module constructs `Permittivity` only.

Examples
--------
An RF engineer estimates the absolute permittivity of the polyethylene dielectric used
in a coaxial cable.
Using the 2022 CODATA value of vacuum permittivity and a relative permittivity of 2.25
gives about 19.92 pF/m:

>>> from math import log, pi
>>> vacuum = PicofaradPerMetre(8.8541878188)
>>> polyethylene = vacuum * 2.25
>>> f"{polyethylene.to(PICOFARAD_PER_METRE):.2f}"
'19.92 pF/m'

An RF engineer models a parallel-plate capacitor with a polyethylene dielectric whose
relative permittivity is taken as 2.25.
The plates are 10 cm square and separated by 1 mm of dielectric.
Estimate the capacitance, then calculate the charge and stored energy when 100 V is
applied.
Neglect fringing fields and dielectric losses.

>>> from kuchka import Metre, Millimetre, Volt
>>> from kuchka.units.electromagnetics.capacitance import PICOFARAD
>>> vacuum = PicofaradPerMetre(8.8541878188)
>>> dielectric = vacuum * 2.25
>>> plate_side = Metre(0.1)
>>> separation = Millimetre(1)
>>> geometry_factor = plate_side * plate_side / separation
>>> capacitance = dielectric * geometry_factor
>>> f"{capacitance.to(PICOFARAD):.1f}"
'199.2 pF'
>>> charging_voltage = Volt(100)
>>> charge = capacitance * charging_voltage
>>> f"{charge:.3g}"
'1.99e-8 C'
>>> stored_energy = capacitance * charging_voltage * charging_voltage / 2
>>> f"{stored_energy:.3g}"
'9.96e-7 J'

Notes
-----
The vacuum value used above is the 2022 CODATA recommended value,
ε₀ = 8.8541878188(14) x 10⁻¹² F/m.
Material permittivity depends on the dielectric and may vary with frequency,
temperature, and measurement conditions.
The polyethylene value here is the nominal value used in the cited coaxial-cable
example, not a universal value for all polyethylene formulations.

`PERMITTIVITY_UNITS` maps symbols such as ``"pF/m"``, ``"nF/m"``, and ``"F/m"`
to their constructors. It is intended for boundary code that reads a unit
from configuration files, material data, or external instrument reports.

References
----------
NIST, 2022 CODATA value of vacuum electric permittivity:
https://physics.nist.gov/cgi-bin/cuu/Value?ep0

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import PERMITTIVITY
from kuchka.internal import prefixes
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Permittivity

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

FARAD_PER_METRE_NAME = "farad_per_metre"
FARAD_PER_METRE_SYMBOL = "F/m"
FARAD_PER_METRE_WORDS = ("farad per metre", "farad per meter")
"""Spoken forms, which prefixed names follow: `picofarad per metre`."""

PICOFARAD_PER_METRE = prefixed_unit(
    prefixes.PICO,
    FARAD_PER_METRE_NAME,
    FARAD_PER_METRE_SYMBOL,
    PERMITTIVITY,
    base_words=FARAD_PER_METRE_WORDS,
)
NANOFARAD_PER_METRE = prefixed_unit(
    prefixes.NANO,
    FARAD_PER_METRE_NAME,
    FARAD_PER_METRE_SYMBOL,
    PERMITTIVITY,
    base_words=FARAD_PER_METRE_WORDS,
)
MICROFARAD_PER_METRE = prefixed_unit(
    prefixes.MICRO,
    FARAD_PER_METRE_NAME,
    FARAD_PER_METRE_SYMBOL,
    PERMITTIVITY,
    base_words=FARAD_PER_METRE_WORDS,
)
MILLIFARAD_PER_METRE = prefixed_unit(
    prefixes.MILLI,
    FARAD_PER_METRE_NAME,
    FARAD_PER_METRE_SYMBOL,
    PERMITTIVITY,
    base_words=FARAD_PER_METRE_WORDS,
)
FARAD_PER_METRE = prefixed_unit(
    prefixes.UNIT,
    FARAD_PER_METRE_NAME,
    FARAD_PER_METRE_SYMBOL,
    PERMITTIVITY,
    base_words=FARAD_PER_METRE_WORDS,
)

Permittivity._canonical_unit = FARAD_PER_METRE  # noqa: SLF001 -- this module owns Permittivity's canonical unit


def PicofaradPerMetre(value: Numeric) -> Permittivity:
    """Construct permittivity from picofarads per metre.

    Parameters
    ----------
    value : Numeric
        Absolute permittivity in pF/m.

    Returns
    -------
    Permittivity
        The supplied value represented as a permittivity.

    Examples
    --------
    The 2022 CODATA vacuum permittivity is approximately 8.8542 pF/m:

    >>> vacuum = PicofaradPerMetre(8.8541878188)
    >>> f"{vacuum.to(PICOFARAD_PER_METRE):.4f}"
    '8.8542 pF/m'

    A 10 cm square electrode pair separated by a 1 mm vacuum gap has a capacitance of
    approximately 88.5 pF.
    The calculation uses vacuum permittivity, with fringing effects neglected:

    >>> from kuchka import Metre, Millimetre
    >>> from kuchka.units.electromagnetics.capacitance import PICOFARAD
    >>> vacuum = PicofaradPerMetre(8.8541878188)
    >>> plate_side = Metre(0.1)
    >>> separation = Millimetre(1)
    >>> geometry_factor = plate_side * plate_side / separation
    >>> capacitance = vacuum * geometry_factor
    >>> f"{capacitance.to(PICOFARAD):.1f}"
    '88.5 pF'

    """
    return Permittivity(
        to_exact(value) * PICOFARAD_PER_METRE.scale, PICOFARAD_PER_METRE
    )


def NanofaradPerMetre(value: Numeric) -> Permittivity:
    """Construct permittivity from nanofarads per metre.

    Parameters
    ----------
    value : Numeric
        Absolute permittivity in nF/m.

    Returns
    -------
    Permittivity
        The supplied value represented as a permittivity.

    Notes
    -----
    Values in nF/m are far above the permittivity of vacuum, so this scale can be
    useful when representing a high-permittivity material or a deliberately effective,
    frequency-dependent dielectric model.

    Examples
    --------
    A high-k dielectric coupon is characterised at 1 nF/m.
    A sensor capacitor uses 20 mm square electrodes separated by a 100 µm dielectric
    layer.
    Calculate its capacitance, then determine the charge and stored energy at 48 V:

    >>> from kuchka import Metre, Micrometre, Volt
    >>> from kuchka.units.electromagnetics.capacitance import NANOFARAD
    >>> dielectric = NanofaradPerMetre(1)
    >>> electrode_side = Metre(0.02)
    >>> separation = Micrometre(100)
    >>> geometry_factor = electrode_side * electrode_side / separation
    >>> capacitor = dielectric * geometry_factor
    >>> f"{capacitor.to(NANOFARAD):.1f}"
    '4.0 nF'
    >>> charging_voltage = Volt(48)
    >>> charge = capacitor * charging_voltage
    >>> f"{charge:.3g}"
    '1.92e-7 C'
    >>> stored_energy = capacitor * charging_voltage * charging_voltage / 2
    >>> f"{stored_energy:.3g}"
    '0.00000461 J'

    """
    return Permittivity(
        to_exact(value) * NANOFARAD_PER_METRE.scale, NANOFARAD_PER_METRE
    )


def MicrofaradPerMetre(value: Numeric) -> Permittivity:
    """Construct permittivity from microfarads per metre.

    Parameters
    ----------
    value : Numeric
        Absolute permittivity in µF/m.

    Returns
    -------
    Permittivity
        The supplied value represented as a permittivity.

    Notes
    -----
    This is an extreme scale for ordinary dielectrics.
    It is included for completeness and for models that deliberately use effective
    parameters.

    Examples
    --------
    A fictional spacecraft uses two 10 m square conductive panels separated by 10 cm
    of an invented field-shaping dielectric with permittivity 0.4 µF/m.
    When charged to 5 kV, how much energy is stored in the panel assembly?

    >>> from kuchka import Metre, Volt
    >>> from kuchka.units.electromagnetics.capacitance import MICROFARAD
    >>> sail_dielectric = MicrofaradPerMetre(0.4)
    >>> panel_side = Metre(10)
    >>> separation = Metre(0.1)
    >>> geometry_factor = panel_side * panel_side / separation
    >>> sail_capacitance = sail_dielectric * geometry_factor
    >>> f"{sail_capacitance.to(MICROFARAD):.0f}"
    '400 µF'
    >>> charging_voltage = Volt(5000)
    >>> charge = sail_capacitance * charging_voltage
    >>> charge
    2 C
    >>> stored_energy = sail_capacitance * charging_voltage * charging_voltage / 2
    >>> stored_energy
    5000 J

    """
    return Permittivity(
        to_exact(value) * MICROFARAD_PER_METRE.scale, MICROFARAD_PER_METRE
    )


def MillifaradPerMetre(value: Numeric) -> Permittivity:
    """Construct permittivity from millifarads per metre.

    Parameters
    ----------
    value : Numeric
        Absolute permittivity in mF/m.

    Returns
    -------
    Permittivity
        The supplied value represented as a permittivity.

    Notes
    -----
    This scale is not representative of ordinary engineering dielectrics.
    A value this large should be understood as an effective model parameter or as part
    of an explicitly fictional setting.

    Examples
    --------
    A fictional electromagnetic braking system uses a plate assembly with a 1 m²
    electrode area, a 10 cm gap, and an effective permittivity of 3 mF/m.
    A 20 Ω dump resistor discharges the resulting capacitor.
    Calculate the circuit's RC time constant:

    >>> from kuchka import Metre, Ohm
    >>> braking_dielectric = MillifaradPerMetre(3)
    >>> electrode_side = Metre(1)
    >>> separation = Metre(0.1)
    >>> geometry_factor = electrode_side * electrode_side / separation
    >>> dump_capacitor = braking_dielectric * geometry_factor
    >>> dump_resistor = Ohm(20)
    >>> time_constant = dump_resistor * dump_capacitor
    >>> time_constant
    0.6 s

    """
    return Permittivity(
        to_exact(value) * MILLIFARAD_PER_METRE.scale, MILLIFARAD_PER_METRE
    )


def FaradPerMetre(value: Numeric) -> Permittivity:
    """Construct permittivity from farads per metre.

    Parameters
    ----------
    value : Numeric
        Absolute permittivity in F/m.

    Returns
    -------
    Permittivity
        The supplied value represented as a permittivity.

    Notes
    -----
    One F/m is roughly 113 billion times the permittivity of vacuum.
    In this scale, a material example should be treated as speculative or fictional,
    not as a known ordinary dielectric.

    Examples
    --------
    A fictional reactor's pulse-buffer bank uses a field-confinement dielectric with an
    effective permittivity of 0.75 F/m.
    Its plates are 2 m square, separated by 10 cm.
    At a charging voltage of 24 V, calculate the stored charge and energy:

    >>> from kuchka import Metre, Volt
    >>> reactor_dielectric = FaradPerMetre(0.75)
    >>> plate_side = Metre(2)
    >>> separation = Metre(0.1)
    >>> geometry_factor = plate_side * plate_side / separation
    >>> buffer_capacitance = reactor_dielectric * geometry_factor
    >>> charging_voltage = Volt(24)
    >>> charge = buffer_capacitance * charging_voltage
    >>> charge
    720 C
    >>> stored_energy = buffer_capacitance * charging_voltage * charging_voltage / 2
    >>> stored_energy
    8640 J

    """
    return Permittivity(to_exact(value) * FARAD_PER_METRE.scale, FARAD_PER_METRE)


PERMITTIVITY_UNITS: Mapping[str, Callable[[Numeric], Permittivity]] = unit_table(
    "PERMITTIVITY_UNITS",
    {
        PICOFARAD_PER_METRE: PicofaradPerMetre,
        NANOFARAD_PER_METRE: NanofaradPerMetre,
        MICROFARAD_PER_METRE: MicrofaradPerMetre,
        MILLIFARAD_PER_METRE: MillifaradPerMetre,
        FARAD_PER_METRE: FaradPerMetre,
    },
)

__all__ = [
    "FARAD_PER_METRE",
    "MICROFARAD_PER_METRE",
    "MILLIFARAD_PER_METRE",
    "NANOFARAD_PER_METRE",
    "PERMITTIVITY_UNITS",
    "PICOFARAD_PER_METRE",
    "FaradPerMetre",
    "MicrofaradPerMetre",
    "MillifaradPerMetre",
    "NanofaradPerMetre",
    "PicofaradPerMetre",
]
