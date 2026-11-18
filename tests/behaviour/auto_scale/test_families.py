"""`auto_scale` along the ladders of every family of prefixed units.

Each case builds a measurement in a unit of a family, and the unit it expects is
written out as the symbol it is displayed with.
"""

from __future__ import annotations

import pytest

import kuchka


def ladders(cls: type) -> tuple:
    """Return the ladders a quantity type binds."""
    return cls._ladders


@pytest.mark.parametrize(
    ("constructor", "value", "text"),
    [
        ("Byte", 5000, "5 kB"),
        ("Megabyte", 2_000_000, "2 TB"),
        ("Bit", 8000, "8 kbit"),
        ("Kibibyte", 5000, "4.8828125 MiB"),
        ("Joule", 3_600_000, "3.6 MJ"),
        ("WattHour", 0.002, "2 mWh"),
        ("Electronvolt", 2_500_000_000, "2.5 GeV"),
        ("Metre", 0.00003, "30 µm"),
        ("Metre", 3000, "3 km"),
        ("Parsec", 3000, "3 kpc"),
        ("Kilogram", 0.0005, "500 mg"),
        ("Gram", 1_500_000, "1.5 Mg"),
        ("Second", 0.002, "2 ms"),
        ("Pascal", 5_000_000, "5 MPa"),
        ("Litre", 0.0004, "400 µL"),
        ("Ohm", 4700, "4.7 kΩ"),
        ("Farad", 0.0000047, "4.7 µF"),
        ("Henry", 0.002, "2 mH"),
        ("Newton", 2500, "2.5 kN"),
        ("Watt", 2_500_000_000, "2.5 GW"),
    ],
)
def test_a_measurement_moves_along_the_ladder_of_its_family(
    constructor: str, value: float, text: str
) -> None:
    measurement = getattr(kuchka, constructor)(value)
    assert str(measurement.auto_scale()) == text
    assert measurement.auto_scale() == measurement


@pytest.mark.parametrize(
    ("constructor", "value", "text"),
    [
        ("Kibibyte", 0.5, "0.5 KiB"),
        ("Mebibyte", 0.0005, "0.512 KiB"),
        ("Bar", 0.0004, "0.4 mbar"),
        ("Parsec", 0.001, "0.001 pc"),
    ],
)
def test_a_family_ends_at_its_smallest_unit(
    constructor: str, value: float, text: str
) -> None:
    assert str(getattr(kuchka, constructor)(value).auto_scale()) == text


@pytest.mark.parametrize(
    ("constructor", "value"),
    [
        ("Centimetre", 2),
        ("Inch", 100_000),
        ("Minute", 90),
        ("Hectopascal", 0.002),
        ("Calorie", 5000),
        ("Pound", 4000),
    ],
)
def test_a_unit_outside_every_family_keeps_its_measurement(
    constructor: str, value: float
) -> None:
    measurement = getattr(kuchka, constructor)(value)
    assert measurement.auto_scale() is measurement


def test_a_binary_unit_stays_binary_and_a_decimal_unit_stays_decimal() -> None:
    assert kuchka.Kibibyte(5_000_000).auto_scale().unit.symbol == "GiB"
    assert kuchka.Kilobyte(5_000_000).auto_scale().unit.symbol == "GB"
    assert kuchka.Kibibit(5_000_000).auto_scale().unit.symbol == "Gibit"
    assert kuchka.Kilobit(5_000_000).auto_scale().unit.symbol == "Gbit"


def test_a_role_of_a_quantity_moves_along_the_ladders_of_that_quantity() -> None:
    roles = {
        kuchka.Impedance: kuchka.Resistance,
        kuchka.Reactance: kuchka.Resistance,
        kuchka.Stress: kuchka.Pressure,
        kuchka.Magnetization: kuchka.MagneticFieldStrength,
        kuchka.ElectricFluxDensity: kuchka.SurfaceChargeDensity,
        kuchka.SamplingPeriod: kuchka.Time,
        kuchka.Entropy: kuchka.HeatCapacity,
        kuchka.SpecificEntropy: kuchka.SpecificHeatCapacity,
    }
    for role, quantity in roles.items():
        assert ladders(role) == ladders(quantity)
