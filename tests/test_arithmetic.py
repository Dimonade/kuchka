"""Arithmetic: the runtime dimension algebra behind +, -, *, /, and comparisons."""

from decimal import Decimal

import pytest

from kuchka.errors import IncompatibleDimensionError
from kuchka.errors import InvalidMeasurementError
from kuchka.errors import UnrepresentableDimensionError
from kuchka.quantities import Conductance
from kuchka.quantities import Current
from kuchka.quantities import Power
from kuchka.quantities import Resistance
from kuchka.quantities import Voltage
from kuchka.units import conductance
from kuchka.units import current
from kuchka.units import power
from kuchka.units import resistance
from kuchka.units import voltage


def test_addition_within_same_unit():
    assert voltage.Volt(5) + voltage.Volt(1) == voltage.Volt(6)


def test_addition_across_prefixes_is_exact():
    one_point_five_volts = voltage.Volt(1) + voltage.Millivolt(500)
    assert one_point_five_volts == voltage.Volt(1.5)
    assert one_point_five_volts == voltage.Millivolt(1500)


def test_addition_across_many_prefixes_stays_exact():
    total = voltage.Millivolt(100) + voltage.Millivolt(200) + voltage.Millivolt(300)
    assert total == voltage.Volt(Decimal("0.6"))


def test_subtraction():
    assert voltage.Volt(5) - voltage.Volt(2) == voltage.Volt(3)


def test_incompatible_addition_raises():
    with pytest.raises(IncompatibleDimensionError):
        voltage.Volt(5) + current.Ampere(1)  # type: ignore[operator]  # not (yet) flagged by ty across sibling quantity types


def test_incompatible_subtraction_raises():
    with pytest.raises(IncompatibleDimensionError):
        voltage.Volt(5) - current.Ampere(1)  # type: ignore[operator]  # not (yet) flagged by ty across sibling quantity types


def test_naked_number_addition_is_rejected_with_a_helpful_message():
    with pytest.raises(InvalidMeasurementError, match="wrap it in a unit constructor"):
        voltage.Volt(5) + 4.2  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_ohms_law_round_trip_stays_exact_with_prefixed_units():
    v = voltage.Volt(5)
    i = current.Milliampere(2)
    r = v / i
    assert r == resistance.Kiloohm(Decimal("2.5"))


@pytest.mark.parametrize(
    ("compute", "expected_type", "expected"),
    [
        pytest.param(
            lambda: voltage.Volt(5) * current.Ampere(2),
            Power,
            power.Watt(10),
            id="voltage*current=power",
        ),
        pytest.param(
            lambda: voltage.Volt(10) / current.Ampere(2),
            Resistance,
            resistance.Ohm(5),
            id="voltage/current=resistance",
        ),
        pytest.param(
            lambda: power.Watt(20) / voltage.Volt(5),
            Current,
            current.Ampere(4),
            id="power/voltage=current",
        ),
        pytest.param(
            lambda: resistance.Ohm(5) * current.Ampere(2),
            Voltage,
            voltage.Volt(10),
            id="resistance*current=voltage",
        ),
        pytest.param(
            lambda: power.Watt(20) / current.Ampere(4),
            Voltage,
            voltage.Volt(5),
            id="power/current=voltage",
        ),
        pytest.param(
            lambda: 1 / resistance.Ohm(5),
            Conductance,
            conductance.Siemens(Decimal("0.2")),
            id="1/resistance=conductance",
        ),
        pytest.param(
            lambda: 1 / conductance.Siemens(Decimal("0.2")),
            Resistance,
            resistance.Ohm(5),
            id="1/conductance=resistance",
        ),
        pytest.param(
            lambda: voltage.Volt(10) * conductance.Siemens(Decimal("0.5")),
            Current,
            current.Ampere(5),
            id="voltage*conductance=current",
        ),
        pytest.param(
            lambda: current.Ampere(5) / voltage.Volt(10),
            Conductance,
            conductance.Siemens(Decimal("0.5")),
            id="current/voltage=conductance",
        ),
        pytest.param(
            lambda: current.Ampere(5) / conductance.Siemens(Decimal("0.5")),
            Voltage,
            voltage.Volt(10),
            id="current/conductance=voltage",
        ),
    ],
)
def test_derived_dimension_arithmetic(compute, expected_type, expected):
    result = compute()
    assert isinstance(result, expected_type)
    assert result == expected


def test_scalar_multiplication():
    assert voltage.Volt(2) * 3 == voltage.Volt(6)
    assert 3 * voltage.Volt(2) == voltage.Volt(6)


def test_scalar_division():
    assert voltage.Volt(6) / 3 == voltage.Volt(2)


def test_same_dimension_division_is_dimensionless():
    ratio = resistance.Ohm(10) / resistance.Ohm(5)
    assert not hasattr(ratio, "magnitude")  # it's a plain Decimal, not a Resistance
    assert ratio == Decimal(2)


def test_negation_and_abs():
    assert -voltage.Volt(5) == voltage.Volt(-5)
    assert abs(voltage.Volt(-5)) == voltage.Volt(5)


def test_ordering_within_same_dimension():
    assert voltage.Volt(1) < voltage.Volt(2)
    assert voltage.Millivolt(1500) > voltage.Volt(1)


def test_ordering_across_dimensions_raises():
    with pytest.raises(IncompatibleDimensionError):
        voltage.Volt(1) < current.Ampere(1)  # noqa: B015


def test_equality_across_dimensions_is_false_not_an_error():
    assert (voltage.Volt(5) == current.Ampere(5)) is False


def test_current_times_resistance_derives_voltage_commutatively():
    assert current.Ampere(2) * resistance.Ohm(5) == resistance.Ohm(5) * current.Ampere(
        2
    )


def test_multiplication_by_unregistered_dimension_has_no_registered_type():
    """Resistance * Resistance is dimensionally valid but has no registered type.

    This is a scope boundary (see UnrepresentableDimensionError), not a
    dimensional-analysis bug: the exponent-vector algebra behind the scenes
    happily computes the result, but nothing in this version of the
    library has a name for it yet.
    """
    match = "no registered engineering type"
    with pytest.raises(UnrepresentableDimensionError, match=match):
        # Statically valid: Resistance * Resistance falls through to the
        # generic `object` overload (LinearQuantity | Decimal), so this is
        # a runtime-only scope-boundary error, not a static type error.
        resistance.Ohm(5) * resistance.Ohm(2)


def test_naked_number_subtraction_is_rejected_with_a_helpful_message():
    with pytest.raises(InvalidMeasurementError, match="wrap it in a unit constructor"):
        voltage.Volt(5) - 4.2  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_zero_division_by_a_measurement_raises_zero_division_error():
    with pytest.raises(ZeroDivisionError):
        voltage.Volt(5) / current.Ampere(0)


def test_zero_division_by_a_plain_number_raises_zero_division_error():
    with pytest.raises(ZeroDivisionError):
        voltage.Volt(5) / 0


def test_arithmetic_results_are_new_immutable_objects():
    a = voltage.Volt(1)
    b = voltage.Volt(2)
    result = a + b
    assert result is not a
    assert result is not b
    assert a == voltage.Volt(1)  # `a` itself was not mutated


def test_equal_measurements_in_different_prefixes_hash_equal():
    """Equal measurements must hash equal to be usable as dict keys or set members."""
    assert hash(voltage.Volt(1)) == hash(voltage.Millivolt(1000))


@pytest.mark.parametrize(
    ("left", "right"),
    [
        (voltage.Volt(1), voltage.Volt(2)),
        (voltage.Millivolt(500), voltage.Volt(1)),
        (voltage.Volt(-5), voltage.Volt(-1)),
    ],
    ids=["volt<volt", "millivolt<volt", "negative_volt<negative_volt"],
)
def test_ordering_operators_agree_with_each_other(left, right):
    assert (left < right) == (not (left >= right))
    assert (left <= right) == (not (left > right))
    assert (left < right) or (left == right) or (left > right)


def test_ordering_operators_all_raise_across_dimensions():
    with pytest.raises(IncompatibleDimensionError):
        voltage.Volt(1) <= current.Ampere(1)  # noqa: B015

    with pytest.raises(IncompatibleDimensionError):
        voltage.Volt(1) > current.Ampere(1)  # noqa: B015

    with pytest.raises(IncompatibleDimensionError):
        voltage.Volt(1) >= current.Ampere(1)  # noqa: B015


def test_reflected_addition():
    """`3 + Volt(2)`-style reflected addition falls back to `__radd__`."""
    assert voltage.Volt(1) + voltage.Volt(2) == voltage.Volt(2) + voltage.Volt(1)


def test_unsupported_operand_type_raises_type_error():
    """An operand kuchka has no opinion about is Python's problem, not ours."""
    with pytest.raises(TypeError):
        voltage.Volt(5) + object()  # type: ignore[operator]  # ty: ignore[unsupported-operator]

    with pytest.raises(TypeError):
        # Statically valid: falls through to the fallback `object` overload
        # (LinearQuantity | Decimal), so no ignore is needed here -- the
        # TypeError only shows up once `to_decimal` runs at call time.
        voltage.Volt(5) * object()

    with pytest.raises(TypeError):
        # Same reasoning as above, for the reflected form.
        object() * voltage.Volt(5)


def test_naked_number_addition_reflected_is_also_rejected():
    """`3 + Volt(2)` falls to `__radd__`, rejecting it the same as `__add__`."""
    with pytest.raises(InvalidMeasurementError, match="wrap it in a unit constructor"):
        3 + voltage.Volt(2)  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_division_by_an_unsupported_operand_type_raises_type_error():
    with pytest.raises(TypeError):
        # Statically valid: falls through to the fallback `object` overload
        # (LinearQuantity | Decimal), so no ignore is needed -- the
        # TypeError only shows up once `to_decimal` runs at call time.
        voltage.Volt(5) / object()
