"""Charge: the arithmetic that produces it, its two inverses, and its prefixes.

Generic algebraic properties (commutativity, associativity, prefix conversion, ...)
are covered once for every registered quantity family elsewhere;
this module covers what is specific to Charge:
the `Current * Time` relationship and its inverses.
"""

import pytest

from kuchka import Charge
from kuchka import IncompatibleDimensionError
from kuchka.units.electromagnetics import charge as charge_units
from kuchka.units.electromagnetics import voltage


def test_charge_prefixes_scale_correctly():
    assert charge_units.Microcoulomb(1000) == charge_units.Millicoulomb(1)
    assert charge_units.Millicoulomb(1000) == charge_units.Coulomb(1)


def test_charge_is_incompatible_with_voltage():
    with pytest.raises(IncompatibleDimensionError):
        charge_units.Coulomb(1) + voltage.Volt(1)  # type: ignore[operator]  # not (yet) flagged by ty across sibling quantity types


def test_isinstance_of_charge():
    assert isinstance(charge_units.Coulomb(1), Charge)


def test_ampere_second_and_coulomb_are_the_same_function():
    """Test AmpereSecond and Coulomb not merely equal-behaving -- the same object."""
    assert charge_units.AmpereSecond is charge_units.Coulomb


def test_ampere_second_is_coulomb():
    assert charge_units.AmpereSecond(1) == charge_units.Coulomb(1)
    assert charge_units.AmpereSecond(5) == charge_units.Coulomb(5)


def test_ampere_second_displays_as_coulomb():
    """AmpereSecond is a plain alias, so it carries Coulomb's symbol, not its own."""
    assert charge_units.AmpereSecond(1).unit is charge_units.Coulomb(1).unit
    assert repr(charge_units.AmpereSecond(1)) == "1 C"


def test_ampere_second_is_resolvable_at_the_charge_units_boundary():
    from kuchka.units import CHARGE_UNITS

    assert CHARGE_UNITS["As"] is charge_units.AmpereSecond
    assert CHARGE_UNITS["As"](5) == charge_units.Coulomb(5)
