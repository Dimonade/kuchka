"""Inductance: the henry, and the quantities it relates to.

The generic behaviour of a quantity type is covered once for every type;
this module covers what is specific to the henry.
"""

from __future__ import annotations

import pytest

from kuchka import IncompatibleDimensionError
from kuchka import Inductance
from kuchka import MagneticFlux
from kuchka import Resistance
from kuchka.units import current
from kuchka.units.electromagnetics import inductance
from kuchka.units.electromagnetics import magnetic_flux
from kuchka.units.electromagnetics import resistance
from kuchka.units.temporal import frequency
from kuchka.units.temporal import time


def test_a_flux_per_ampere_is_an_inductance() -> None:
    linked = magnetic_flux.Milliweber(6) / current.Ampere(2)
    assert isinstance(linked, Inductance)
    assert linked == inductance.Millihenry(3)


def test_an_inductance_carrying_a_current_links_a_flux() -> None:
    flux = inductance.Henry(2) * current.Ampere(3)
    assert isinstance(flux, MagneticFlux)
    assert flux == magnetic_flux.Weber(6)


def test_an_ohm_held_for_a_second_is_a_henry() -> None:
    result = resistance.Ohm(4) * time.Second(3)
    assert isinstance(result, Inductance)
    assert result == inductance.Henry(12)


def test_an_inductance_at_a_frequency_is_a_resistance() -> None:
    reactance = inductance.Millihenry(10) * frequency.Kilohertz(1)
    assert isinstance(reactance, Resistance)
    assert reactance == resistance.Ohm(10)


def test_an_inductance_is_not_a_flux() -> None:
    with pytest.raises(IncompatibleDimensionError):
        inductance.Henry(1) + magnetic_flux.Weber(1)  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_the_henry_is_known_by_its_name_at_the_boundary() -> None:
    from kuchka.units import INDUCTANCE_UNITS

    assert INDUCTANCE_UNITS["henries"] is inductance.Henry
