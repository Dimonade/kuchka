"""Tests for migrate.py, rung 4: the unit tables, and writing the file back."""

from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import migrate
import pytest

from kuchka import Ampere
from kuchka import Celsius
from kuchka import Hertz
from kuchka import Kelvin
from kuchka import Millivolt
from kuchka import Volt
from kuchka import wire

LEGACY = (HERE / "config_legacy.ini").read_text(encoding="utf-8")
MODERN = (HERE / "config_modern.toml").read_text(encoding="utf-8")


def test_the_shipped_modern_file_is_what_the_migration_writes() -> None:
    assert migrate.migrate(LEGACY) == MODERN


def test_each_value_keeps_the_unit_the_legacy_key_named() -> None:
    tables = migrate.read_legacy(LEGACY)
    assert tables["red_led.accepted_voltage"]["minimum"] == Millivolt(-1)
    assert tables["red_led.accepted_voltage"]["minimum"].unit.symbol == "mV"
    assert tables["blue_led.accepted_voltage"]["maximum"] == Volt(Decimal("3.3"))
    assert tables["red_led.accepted_temperature"]["minimum"] == Celsius(15)
    assert tables["blue_led.accepted_temperature"]["minimum"] == Kelvin(
        Decimal("288.15")
    )
    assert tables["blue_led.accepted_current"]["maximum"] == Ampere(Decimal("0.05"))
    assert tables["comms"]["sensor_poll_rate"] == Hertz(500)


def test_the_digits_are_the_digits_that_were_typed() -> None:
    legacy = LEGACY.replace(
        "accepted_voltage_max_v = 3.300", "accepted_voltage_max_v = 0.1"
    )
    written = migrate.migrate(legacy)
    assert 'maximum = "0.1 V"' in written


def test_a_value_that_is_not_a_float_survives_the_round_trip() -> None:
    tables = {"t": {"v": Volt(1) / 3}}
    assert migrate.write_modern(tables).splitlines()[-1] == 'v = "1/3 V"'
    assert wire.load("1/3 V", type(tables["t"]["v"])) == Volt(1) / 3


@pytest.mark.parametrize(
    ("old", "new", "message"),
    [
        (
            "accepted_voltage_min_mv",
            "accepted_voltage_min_ma",
            "red_led.accepted_voltage_min_ma: 'ma' is not a unit of voltage",
        ),
        (
            "accepted_voltage_min_mv",
            "accepted_voltage_min_xx",
            "'xx' is not a unit of voltage",
        ),
        (
            "accepted_voltage_min_mv",
            "accepted_volts_min_mv",
            "no quantity is known for 'accepted_volts'",
        ),
        ("-1.000", "minus one", "'minus one' is not a number"),
    ],
)
def test_what_the_convention_never_checked_is_refused(
    old: str, new: str, message: str
) -> None:
    with pytest.raises(migrate.MigrationError, match=message):
        migrate.migrate(LEGACY.replace(old, new, 1))
