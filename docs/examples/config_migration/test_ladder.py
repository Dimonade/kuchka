"""The three rungs read the same file the same way, and refuse the same mistakes.

This directory is documentation, not part of the installed `kuchka` package, so the
example modules are imported by adding this directory to `sys.path`.

Run with `pytest docs/examples/config_migration` from the repository root, or `pytest`
from inside this directory.
"""

from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path
from typing import Any

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import pytest

pytest.importorskip("pydantic")
pytest.importorskip("attrs")

import settings_attrs
import settings_parse
import settings_pydantic
from pydantic import ValidationError

from kuchka import Celsius
from kuchka import Kelvin
from kuchka import Millivolt
from kuchka import wire

MODERN = (HERE / "config_modern.toml").read_text(encoding="utf-8")

# Each rung, and the error it raises: Pydantic reports a ValidationError, attrs raises
# the first kuchka error, and the parse rung raises the application's own ConfigError.
RUNGS = {
    "pydantic": (settings_pydantic.loads, ValidationError),
    "attrs": (settings_attrs.loads, (ValueError, TypeError)),
    "parse": (settings_parse.loads, settings_parse.ConfigError),
}

MISTAKES = {
    "a current's unit in a voltage field": ('minimum = "-1 mV"', 'minimum = "-1 mA"'),
    "a number with no unit": ('minimum = "-1 mV"', "minimum = -1.0"),
    "text with no number": ('minimum = "-1 mV"', 'minimum = "mV"'),
    "a limit beyond what the fixture can do": (
        'maximum = "20 mA"',
        'maximum = "0.5 A"',
    ),
    "a voltage beyond what the fixture can do": ('maximum = "1 mV"', 'maximum = "6 V"'),
    "a swapped range": (
        'minimum = "15 °C"\nmaximum = "45 °C"',
        'minimum = "45 °C"\nmaximum = "15 °C"',
    ),
    "a frequency written as a baud rate": ('"9600 Bd"', '"500 Hz"'),
    "a missing key": ('maximum = "20 mA"\n', ""),
    "an unknown key": ("[comms]\n", '[comms]\nparity = "none"\n'),
}


def limits(config: Any) -> dict[str, str]:  # noqa: ANN401 -- any rung's classes
    """Write every limit of a configuration as text, whichever rung built it."""
    written = {}
    for led in ("red_led", "blue_led"):
        for field in ("accepted_voltage", "accepted_current", "accepted_temperature"):
            window = getattr(getattr(config, led), field)
            written[f"{led}.{field}"] = (
                f"{wire.dump(window.minimum)} .. {wire.dump(window.maximum)}"
            )
    written["baud"] = wire.dump(config.comms.uart_baud_rate)
    written["poll"] = wire.dump(config.comms.sensor_poll_rate)
    return written


def test_every_rung_reads_the_shipped_file_into_the_same_limits() -> None:
    read = {name: limits(loads(MODERN)) for name, (loads, _) in RUNGS.items()}
    assert read["pydantic"] == read["attrs"] == read["parse"]
    assert read["pydantic"]["red_led.accepted_voltage"] == "-1 mV .. 1 mV"
    assert read["pydantic"]["blue_led.accepted_temperature"] == "288.15 K .. 318.15 K"


@pytest.mark.parametrize("rung", RUNGS)
def test_every_unit_stays_as_it_was_written(rung: str) -> None:
    config = RUNGS[rung][0](MODERN)
    assert config.red_led.accepted_voltage.minimum.unit.symbol == "mV"
    assert config.blue_led.accepted_voltage.maximum.unit.symbol == "V"
    assert config.red_led.accepted_temperature.minimum == Celsius(15)
    assert config.red_led.accepted_temperature.minimum.unit.symbol == "°C"
    assert config.blue_led.accepted_temperature.minimum.unit.symbol == "K"


@pytest.mark.parametrize("rung", RUNGS)
def test_limits_in_different_units_compare_without_conversion(rung: str) -> None:
    config = RUNGS[rung][0](MODERN)
    assert (
        config.red_led.accepted_voltage.maximum
        < config.blue_led.accepted_voltage.maximum
    )
    assert config.red_led.accepted_voltage.maximum == Millivolt(1)
    assert config.blue_led.accepted_temperature.minimum == Kelvin(Decimal("288.15"))


@pytest.mark.parametrize("rung", RUNGS)
@pytest.mark.parametrize("mistake", MISTAKES)
def test_every_rung_refuses_every_mistake(rung: str, mistake: str) -> None:
    loads, error = RUNGS[rung]
    old, new = MISTAKES[mistake]
    assert old in MODERN, old
    with pytest.raises(error):
        loads(MODERN.replace(old, new, 1))


@pytest.mark.parametrize("rung", RUNGS)
def test_a_value_written_by_hand_in_another_spelling_is_read(rung: str) -> None:
    text = MODERN.replace('"15 °C"', '"15 C"').replace('"500 Hz"', '"0.5 kHz"')
    config = RUNGS[rung][0](text)
    assert config.red_led.accepted_temperature.minimum == Celsius(15)
    assert wire.dump(config.comms.sensor_poll_rate) == "0.5 kHz"
