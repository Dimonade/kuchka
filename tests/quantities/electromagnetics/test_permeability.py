"""Permeability: the henry per metre, as an inductance per length.

The generic behaviour of a quantity type is covered once for every type;
this module covers what is specific to permeability.
"""

from __future__ import annotations

import pytest

from kuchka import IncompatibleDimensionError
from kuchka import Inductance
from kuchka import Length
from kuchka import Permeability
from kuchka.units import length
from kuchka.units.electromagnetics import inductance
from kuchka.units.electromagnetics import permeability


def test_an_inductance_per_length_is_a_permeability() -> None:
    material = inductance.Microhenry(5) / length.Metre(2)
    assert isinstance(material, Permeability)
    assert material == permeability.MicrohenryPerMetre(2.5)


def test_a_permeability_over_a_length_is_an_inductance() -> None:
    wound = permeability.NanohenryPerMetre(1250) * length.Metre(2)
    assert isinstance(wound, Inductance)
    assert wound == inductance.Nanohenry(2500)


def test_an_inductance_over_a_permeability_is_a_length() -> None:
    reach = inductance.Henry(6) / permeability.HenryPerMetre(3)
    assert isinstance(reach, Length)
    assert reach == length.Metre(2)


def test_a_permeability_is_not_an_inductance() -> None:
    with pytest.raises(IncompatibleDimensionError):
        permeability.HenryPerMetre(1) + inductance.Henry(1)  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_the_boundary_reads_the_spoken_forms() -> None:
    assert (
        permeability.PERMEABILITY_UNITS["henry per meter"] is permeability.HenryPerMetre
    )
