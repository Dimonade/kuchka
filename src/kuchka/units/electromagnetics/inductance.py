"""Inductance constructors, from picohenries to kilohenries.

The henry (H) is the SI unit of inductance: 1 H = 1 Wb/A.
An ideal inductor relates voltage to the rate of change of current, v = L dI/dt, and
stores magnetic-field energy E = ½LI² when a current flows through it.

Different engineering fields encounter very different inductance scales.
Picohenries matter in high-speed interconnects; nanohenries appear in RF components
and power-module layouts; microhenries are common in converters and filters;
millihenries describe many actuators and larger coils.
Henries are useful for laboratory magnets, while kilohenries provide a scale for
extreme models and explicitly fictional systems.

Examples
--------
A buck converter has a 24 µH inductor with 12 V across it during a 2 µs switching
interval.
Assuming the inductor voltage is constant over that interval, the current rises by 1 A:

>>> from kuchka import Ampere, Microhenry, Microsecond, Volt
>>> choke = Microhenry(24)
>>> switch_voltage = Volt(12)
>>> on_time = Microsecond(2)
>>> current_change = switch_voltage * on_time / choke
>>> current_change
1 A

An actuator coil with 125 mH of inductance carries 4 A before being switched off.
The energy stored in its magnetic field is 1 J.
A practical driver must provide a suitable path for that energy rather than simply
opening the circuit:

>>> from kuchka import Ampere, Millihenry
>>> actuator_coil = Millihenry(125)
>>> coil_current = Ampere(4)
>>> stored_energy = actuator_coil * coil_current * coil_current / 2
>>> stored_energy
1 J

Notes
-----
The energy expression E = ½LI² assumes a linear inductor with constant inductance.
Magnetic cores can saturate, causing inductance to change with current.
Real component selection must also account for winding resistance, current ratings,
thermal limits, and self-resonance.

`INDUCTANCE_UNITS` maps symbols such as ``"pH"``, ``"nH"``, ``"µH"``,
``"mH"``, ``"H"``, and ``"kH"`` to their constructors. It is intended for
boundary code that reads a unit from configuration files, component databases,
simulation inputs, or measurement instruments.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import INDUCTANCE
from kuchka.internal import prefixes
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Inductance

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

HENRY_NAME = "henry"
HENRY_SYMBOL = "H"
HENRY_WORDS = ("henries",)
"""The plural, which prefixed names follow: `millihenries`."""

PICOHENRY = prefixed_unit(
    prefixes.PICO, HENRY_NAME, HENRY_SYMBOL, INDUCTANCE, base_words=HENRY_WORDS
)
NANOHENRY = prefixed_unit(
    prefixes.NANO, HENRY_NAME, HENRY_SYMBOL, INDUCTANCE, base_words=HENRY_WORDS
)
MICROHENRY = prefixed_unit(
    prefixes.MICRO, HENRY_NAME, HENRY_SYMBOL, INDUCTANCE, base_words=HENRY_WORDS
)
MILLIHENRY = prefixed_unit(
    prefixes.MILLI, HENRY_NAME, HENRY_SYMBOL, INDUCTANCE, base_words=HENRY_WORDS
)
HENRY = prefixed_unit(
    prefixes.UNIT, HENRY_NAME, HENRY_SYMBOL, INDUCTANCE, base_words=HENRY_WORDS
)
KILOHENRY = prefixed_unit(
    prefixes.KILO, HENRY_NAME, HENRY_SYMBOL, INDUCTANCE, base_words=HENRY_WORDS
)

Inductance._canonical_unit = HENRY  # noqa: SLF001 -- this module owns Inductance's canonical unit


def Picohenry(value: Numeric) -> Inductance:
    """Construct an inductance from picohenries.

    Parameters
    ----------
    value : Numeric
        Inductance in pH.

    Returns
    -------
    Inductance
        Inductance represented in picohenries.

    Examples
    --------
    A fast power switch changes the current through a package interconnect by 50 A in
    1 ns.
    A loop inductance of 20 pH produces an ideal inductive voltage of 1 V during that
    transition:

    >>> from kuchka import Ampere, Nanosecond, Picohenry
    >>> package_loop = Picohenry(20)
    >>> current_step = Ampere(50)
    >>> transition_time = Nanosecond(1)
    >>> package_loop * current_step / transition_time
    1 V

    """
    return Inductance(to_exact(value) * PICOHENRY.scale, PICOHENRY)


def Nanohenry(value: Numeric) -> Inductance:
    """Construct an inductance from nanohenries.

    Parameters
    ----------
    value : Numeric
        Inductance in nH.

    Returns
    -------
    Inductance
        Inductance represented in nanohenries.

    Examples
    --------
    A pulsed-power busbar loop has 2 nH of inductance and briefly carries 1000 A.
    The magnetic energy associated with that loop inductance is 1 mJ:

    >>> from kuchka import Ampere, Nanohenry
    >>> busbar_loop = Nanohenry(2)
    >>> pulse_current = Ampere(1000)
    >>> busbar_loop * pulse_current * pulse_current / 2
    0.001 J

    """
    return Inductance(to_exact(value) * NANOHENRY.scale, NANOHENRY)


def Microhenry(value: Numeric) -> Inductance:
    """Construct an inductance from microhenries.

    Parameters
    ----------
    value : Numeric
        Inductance in µH.

    Returns
    -------
    Inductance
        Inductance represented in microhenries.

    Examples
    --------
    In a switching converter, a 24 µH choke with 12 V across it for 2 µs experiences,
    ideally, a current increase of 1 A:

    >>> from kuchka import Microhenry, Microsecond, Volt
    >>> choke = Microhenry(24)
    >>> switch_voltage = Volt(12)
    >>> on_time = Microsecond(2)
    >>> switch_voltage * on_time / choke
    1 A

    """
    return Inductance(to_exact(value) * MICROHENRY.scale, MICROHENRY)


def Millihenry(value: Numeric) -> Inductance:
    """Construct an inductance from millihenries.

    Parameters
    ----------
    value : Numeric
        Inductance in mH.

    Returns
    -------
    Inductance
        Inductance represented in millihenries.

    Examples
    --------
    When an actuator coil's 4 A current falls to zero over 10 ms, a 125 mH winding has
    an ideal induced-voltage magnitude of 50 V.
    A real driver uses a flyback path or clamp to control the turn-off voltage:

    >>> from kuchka import Ampere, Millihenry, Millisecond
    >>> actuator_coil = Millihenry(125)
    >>> current_change = Ampere(4)
    >>> turn_off_time = Millisecond(10)
    >>> actuator_coil * current_change / turn_off_time
    50 V

    """
    return Inductance(to_exact(value) * MILLIHENRY.scale, MILLIHENRY)


def Henry(value: Numeric) -> Inductance:
    """Construct an inductance from henries.

    Parameters
    ----------
    value : Numeric
        Inductance in H.

    Returns
    -------
    Inductance
        Inductance represented in henries.

    Examples
    --------
    A laboratory magnet has a 2 H winding.
    Applying 10 V across an winding for 60 s changes its current by 300 A, ignoring
    resistance and other voltage drops:

    >>> from kuchka import Henry, Second, Volt
    >>> magnet_winding = Henry(2)
    >>> ramp_voltage = Volt(10)
    >>> ramp_duration = Second(60)
    >>> ramp_voltage * ramp_duration / magnet_winding
    300 A

    """
    return Inductance(to_exact(value) * HENRY.scale, HENRY)


def Kilohenry(value: Numeric) -> Inductance:
    """Construct an inductance from kilohenries.

    Parameters
    ----------
    value : Numeric
        Inductance in kH.

    Returns
    -------
    Inductance
        Inductance represented in kilohenries.

    Notes
    -----
    Kilohenry-scale inductors are outside ordinary component practice.
    The example is explicitly fictional.

    Examples
    --------
    A fictional spacecraft's magnetic-containment loop has an effective inductance of
    2 kH.
    Even with 100 V across it, changing the current by 50 A takes 1000 s in the ideal
    constant-voltage model:

    >>> from kuchka import Ampere, Kilohenry, Volt
    >>> containment_loop = Kilohenry(2)
    >>> current_step = Ampere(50)
    >>> drive_voltage = Volt(100)
    >>> containment_loop * current_step / drive_voltage
    1000 s

    """
    return Inductance(to_exact(value) * KILOHENRY.scale, KILOHENRY)


INDUCTANCE_UNITS: Mapping[str, Callable[[Numeric], Inductance]] = unit_table(
    "INDUCTANCE_UNITS",
    {
        PICOHENRY: Picohenry,
        NANOHENRY: Nanohenry,
        MICROHENRY: Microhenry,
        MILLIHENRY: Millihenry,
        HENRY: Henry,
        KILOHENRY: Kilohenry,
    },
)

__all__ = [
    "HENRY",
    "INDUCTANCE_UNITS",
    "KILOHENRY",
    "MICROHENRY",
    "MILLIHENRY",
    "NANOHENRY",
    "PICOHENRY",
    "Henry",
    "Kilohenry",
    "Microhenry",
    "Millihenry",
    "Nanohenry",
    "Picohenry",
]
