"""Permittivity: the farad per metre, as a capacitance per length.

The generic behaviour of a quantity type is covered once for every type;
this module covers what is specific to permittivity.
"""

from __future__ import annotations

import pytest

from kuchka import Capacitance
from kuchka import IncompatibleDimensionError
from kuchka import Length
from kuchka import Permittivity
from kuchka.units import length
from kuchka.units.electromagnetics import capacitance
from kuchka.units.electromagnetics import permittivity


def test_a_capacitance_per_length_is_a_permittivity() -> None:
    material = capacitance.Picofarad(20) / length.Metre(2)
    assert isinstance(material, Permittivity)
    assert material == permittivity.PicofaradPerMetre(10)


def test_a_permittivity_over_a_length_is_a_capacitance() -> None:
    stored = permittivity.NanofaradPerMetre(3) * length.Metre(2)
    assert isinstance(stored, Capacitance)
    assert stored == capacitance.Nanofarad(6)


def test_a_capacitance_over_a_permittivity_is_a_length() -> None:
    reach = capacitance.Nanofarad(6) / permittivity.NanofaradPerMetre(3)
    assert isinstance(reach, Length)
    assert reach == length.Metre(2)


def test_a_permittivity_is_not_a_capacitance() -> None:
    with pytest.raises(IncompatibleDimensionError):
        permittivity.FaradPerMetre(1) + capacitance.Farad(1)  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_the_boundary_reads_the_spoken_forms() -> None:
    assert permittivity.PERMITTIVITY_UNITS["pF/m"] is permittivity.PicofaradPerMetre
    assert (
        permittivity.PERMITTIVITY_UNITS["picofarad per meter"]
        is permittivity.PicofaradPerMetre
    )
