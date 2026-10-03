"""Force: the reciprocals of Newton's second law, and its non-SI/imperial units.

Generic algebraic properties (commutativity, associativity, prefix conversion, ...)
are covered once for every registered quantity family elsewhere, and F = ma itself is
covered in the Acceleration tests since Mass is the multiplicand there;
this module covers what is specific to Force: its prefixed SI units and the two
non-SI units, `Dyne` and `PoundForce`.
"""

from decimal import Decimal

import pytest

from kuchka import Acceleration
from kuchka import Dyne
from kuchka import Force
from kuchka import IncompatibleDimensionError
from kuchka import InvalidMeasurementError
from kuchka import Kilogram
from kuchka import KilogramForce
from kuchka import Kilonewton
from kuchka import Mass
from kuchka import Meganewton
from kuchka import MetrePerSecondSquared
from kuchka import Micronewton
from kuchka import Millinewton
from kuchka import Newton
from kuchka import PoundForce
from kuchka import Volt


def test_force_prefixes_scale_correctly():
    assert Millinewton(1000) == Newton(1)
    assert Kilonewton(1) == Newton(1000)


def test_dyne_is_exact():
    """The CGS unit of force: exactly 1e-5 N by definition."""
    assert Dyne(100_000) == Newton(1)


def test_kilogram_force_converts_exactly_to_newtons() -> None:
    assert KilogramForce(1) == Newton(Decimal("9.80665"))


def test_pound_force_is_exact():
    """1 lbf = 1 avoirdupois pound accelerated at standard gravity, both exact."""
    assert PoundForce(1) == Newton(Decimal("4.4482216152605"))


def test_isinstance_of_force():
    assert isinstance(Newton(5), Force)
    assert isinstance(Millinewton(5), Force)
    assert isinstance(Dyne(5), Force)
    assert isinstance(PoundForce(5), Force)


def test_scalar_multiplication_and_division():
    assert Newton(2) * 3 == Newton(6)
    assert Newton(6) / 3 == Newton(2)


def test_ordering_within_force():
    assert Millinewton(500) < Newton(1)
    assert Kilonewton(1) > Newton(500)
    assert PoundForce(1) > Newton(4)


def test_force_divided_by_mass_and_acceleration_are_reciprocal_operands():
    force = Newton(10)
    acceleration = force / Kilogram(2)
    mass = force / MetrePerSecondSquared(5)
    assert isinstance(acceleration, Acceleration)
    assert isinstance(mass, Mass)
    assert force / mass == acceleration
    assert force / acceleration == mass


def test_naked_number_addition_is_rejected():
    with pytest.raises(InvalidMeasurementError, match="wrap it in a unit constructor"):
        Newton(5) + 4.2  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_force_is_incompatible_with_voltage():
    with pytest.raises(IncompatibleDimensionError):
        Newton(1) + Volt(1)  # type: ignore[operator]  # not (yet) flagged by ty across sibling quantity types


def test_micronewton_and_meganewton_span_six_orders_of_magnitude() -> None:
    assert Micronewton(1_000_000) == Newton(1)
    assert Meganewton(1) == Newton(1_000_000)
