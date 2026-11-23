"""Rung 3, parse: no framework, one function that reads a measurement.

This is what the first two rungs do for you.
`parse(text, Voltage)` reads one measurement and refuses what is no voltage; everything
else here is ordinary Python around it: finding the key, naming it in the message, and
building the objects.
It is the rung to take when the file is read by a program that already has its own
configuration classes, or when the error messages have to be written by hand.

Nothing here needs more than kuchka.
"""

from __future__ import annotations

import tomllib
from collections.abc import Iterator
from collections.abc import Mapping
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any

from fixture import MAX_CURRENT
from fixture import MAX_TEMPERATURE
from fixture import MAX_VOLTAGE
from fixture import MIN_TEMPERATURE

from kuchka import BaudRate
from kuchka import Current
from kuchka import Frequency
from kuchka import Milliampere
from kuchka import Temperature
from kuchka import Voltage
from kuchka import parse
from kuchka.bounds import Bounds

SAFE_VOLTAGE = Bounds(ge=-MAX_VOLTAGE, le=MAX_VOLTAGE)
SAFE_CURRENT = Bounds(ge=Milliampere(0), le=MAX_CURRENT)
SAFE_TEMPERATURE = Bounds(ge=MIN_TEMPERATURE, le=MAX_TEMPERATURE)


class ConfigError(Exception):
    """Something is wrong with the limits file; the message says where and why."""


@contextmanager
def _at(where: str) -> Iterator[None]:
    """Name `where` in the `ValueError` raised inside: bad text, a bound, a swap."""
    try:
        yield
    except ValueError as exc:
        msg = f"{where}: {exc}"
        raise ConfigError(msg) from exc


def _table(parent: Mapping[str, Any], key: str, where: str) -> Mapping[str, Any]:
    """Return the table `key` of `parent`, which has to be there."""
    here = f"{where}.{key}" if where else key
    table = parent.get(key)
    if not isinstance(table, Mapping):
        msg = f"{here}: expected a table"
        raise ConfigError(msg)
    return table


def _only(table: Mapping[str, Any], names: set[str], where: str) -> None:
    """Refuse a key the format does not know, which is a typo until proven otherwise."""
    unknown = set(table) - names
    if unknown:
        msg = f"{where}: unknown key(s) {', '.join(sorted(unknown))}"
        raise ConfigError(msg)


def _read(
    table: Mapping[str, Any],
    key: str,
    quantity: type[Any],
    *,
    where: str,
    within: Bounds[Any] | None = None,
) -> Any:  # noqa: ANN401 -- an instance of `quantity`
    """Read one measurement: its text, as the quantity, within the hardware's range."""
    here = f"{where}.{key}"
    if key not in table:
        msg = f"{here}: missing"
        raise ConfigError(msg)
    text = table[key]
    if not isinstance(text, str):
        msg = f"{here}: expected a number and its unit as text, got {text!r}"
        raise ConfigError(msg)
    with _at(here):
        value = parse(text, quantity)
        return value if within is None else within.check(value)


@dataclass(frozen=True)
class VoltageWindow:
    """The accepted voltage range of one LED."""

    minimum: Voltage
    maximum: Voltage

    def __post_init__(self) -> None:
        Bounds(ge=self.minimum, le=self.maximum)  # raises ValueError when inverted


@dataclass(frozen=True)
class CurrentWindow:
    """The accepted current range of one LED."""

    minimum: Current
    maximum: Current

    def __post_init__(self) -> None:
        Bounds(ge=self.minimum, le=self.maximum)  # raises ValueError when inverted


@dataclass(frozen=True)
class TemperatureWindow:
    """The accepted case-temperature range of one LED."""

    minimum: Temperature
    maximum: Temperature

    def __post_init__(self) -> None:
        Bounds(ge=self.minimum, le=self.maximum)  # raises ValueError when inverted


@dataclass(frozen=True)
class LedLimits:
    """Everything a measured LED has to stay within."""

    accepted_voltage: VoltageWindow
    accepted_current: CurrentWindow
    accepted_temperature: TemperatureWindow


@dataclass(frozen=True)
class CommsSettings:
    """How fast the board talks, and how often the fixture polls it."""

    uart_baud_rate: BaudRate
    sensor_poll_rate: Frequency


@dataclass(frozen=True)
class DeviceConfig:
    """The typed configuration the rest of the application sees."""

    red_led: LedLimits
    blue_led: LedLimits
    comms: CommsSettings


def _window(
    cls: type[Any], parent: Mapping[str, Any], key: str, within: Bounds[Any], where: str
) -> Any:  # noqa: ANN401 -- an instance of `cls`
    """Read the `minimum` and `maximum` under `key`, and build the window."""
    here = f"{where}.{key}"
    table = _table(parent, key, where)
    _only(table, {"minimum", "maximum"}, here)
    minimum = _read(table, "minimum", within.quantity, where=here, within=within)
    maximum = _read(table, "maximum", within.quantity, where=here, within=within)
    with _at(here):
        return cls(minimum=minimum, maximum=maximum)


def _led(table: Mapping[str, Any], where: str) -> LedLimits:
    names = {"accepted_voltage", "accepted_current", "accepted_temperature"}
    _only(table, names, where)
    return LedLimits(
        accepted_voltage=_window(
            VoltageWindow, table, "accepted_voltage", SAFE_VOLTAGE, where
        ),
        accepted_current=_window(
            CurrentWindow, table, "accepted_current", SAFE_CURRENT, where
        ),
        accepted_temperature=_window(
            TemperatureWindow, table, "accepted_temperature", SAFE_TEMPERATURE, where
        ),
    )


def _comms(table: Mapping[str, Any], where: str) -> CommsSettings:
    _only(table, {"uart_baud_rate", "sensor_poll_rate"}, where)
    return CommsSettings(
        uart_baud_rate=_read(table, "uart_baud_rate", BaudRate, where=where),
        sensor_poll_rate=_read(table, "sensor_poll_rate", Frequency, where=where),
    )


def loads(text: str) -> DeviceConfig:
    """Read a limits file from its TOML text; raises `ConfigError`."""
    raw = tomllib.loads(text)
    _only(raw, {"red_led", "blue_led", "comms"}, "file")
    return DeviceConfig(
        red_led=_led(_table(raw, "red_led", ""), "red_led"),
        blue_led=_led(_table(raw, "blue_led", ""), "blue_led"),
        comms=_comms(_table(raw, "comms", ""), "comms"),
    )
