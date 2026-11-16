"""Boundary layer for device-limits configuration: TOML in, typed settings out.

This is the only place in an application that reads a unit as text.
Everything below `load_device_config` returns typed `kuchka` quantities;
nothing downstream of it ever sees a bare number again.

Three rules, matching `kuchka`'s own design:

1. Every measurement is one string, such as `"2800 mV"`, read by `parse` through the
    unit table of the quantity the field expects:
    a voltage field reads `"mA"` as nothing, the way it reads a typo, and a bare TOML
    number, which is a binary float with no unit, is refused.
2. `parse` reads the digits exactly, so what an engineer typed is what is stored.
3. Unknown keys are treated the same as missing ones.
    A typo'd section or field name fails loudly at load time, not silently three
    functions later when something expected is `None`.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import Any
from typing import TypeVar

from kuchka import BaudRate
from kuchka import Current
from kuchka import Frequency
from kuchka import Temperature
from kuchka import Voltage
from kuchka import parse
from kuchka.errors import ParseError

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path

_QuantityT = TypeVar("_QuantityT", BaudRate, Current, Frequency, Temperature, Voltage)


class ConfigError(Exception):
    """A device-limits config file could not be parsed into typed settings."""


def _read(
    section: Mapping[str, Any],
    path: str,
    quantity: type[_QuantityT],
    *,
    field: str,
) -> _QuantityT:
    """Read the measurement at `path` in `section` as a `quantity`, or fail with why."""
    node: Any = section
    for key in path.split("."):
        try:
            node = node[key]
        except (KeyError, TypeError) as exc:
            msg = f"{field}.{path}: missing"
            raise ConfigError(msg) from exc

    if not isinstance(node, str):
        msg = f"{field}.{path}: expected a number with its unit as text, got {node!r}"
        raise ConfigError(msg)

    try:
        return parse(node, quantity)
    except ParseError as exc:
        msg = f"{field}.{path}: {exc}"
        raise ConfigError(msg) from exc


@dataclass(frozen=True)
class VoltageLimits:
    """The accepted voltage range for one device, min and max inclusive."""

    minimum: Voltage
    maximum: Voltage

    def __post_init__(self) -> None:
        if self.minimum > self.maximum:
            msg = f"minimum voltage {self.minimum!r} exceeds maximum {self.maximum!r}"
            raise ConfigError(msg)


@dataclass(frozen=True)
class CurrentLimits:
    """The accepted current range for one device, min and max inclusive."""

    minimum: Current
    maximum: Current

    def __post_init__(self) -> None:
        if self.minimum > self.maximum:
            msg = f"minimum current {self.minimum!r} exceeds maximum {self.maximum!r}"
            raise ConfigError(msg)


@dataclass(frozen=True)
class TemperatureLimits:
    """The accepted case-temperature range for one device, min and max inclusive."""

    minimum: Temperature
    maximum: Temperature

    def __post_init__(self) -> None:
        if self.minimum > self.maximum:
            msg = (
                f"minimum temperature {self.minimum!r} exceeds maximum {self.maximum!r}"
            )
            raise ConfigError(msg)


@dataclass(frozen=True)
class LedLimits:
    """The full set of accepted operating limits for one LED."""

    voltage: VoltageLimits
    current: CurrentLimits
    temperature: TemperatureLimits


@dataclass(frozen=True)
class CommsSettings:
    """Communication settings shared across the device: how fast, how often."""

    uart_baud_rate: BaudRate
    sensor_poll_rate: Frequency


@dataclass(frozen=True)
class DeviceConfig:
    """The fully typed device configuration: what the rest of the application sees."""

    red_led: LedLimits
    blue_led: LedLimits
    comms: CommsSettings


def _parse_led_limits(raw: Mapping[str, Any], *, led_name: str) -> LedLimits:
    def read(path: str, quantity: type[_QuantityT]) -> _QuantityT:
        return _read(raw, path, quantity, field=led_name)

    return LedLimits(
        voltage=VoltageLimits(
            minimum=read("accepted_voltage.min", Voltage),
            maximum=read("accepted_voltage.max", Voltage),
        ),
        current=CurrentLimits(
            minimum=read("accepted_current.min", Current),
            maximum=read("accepted_current.max", Current),
        ),
        temperature=TemperatureLimits(
            minimum=read("accepted_temperature.min", Temperature),
            maximum=read("accepted_temperature.max", Temperature),
        ),
    )


def _parse_comms(raw: Mapping[str, Any]) -> CommsSettings:
    return CommsSettings(
        uart_baud_rate=_read(raw, "uart_baud_rate", BaudRate, field="comms"),
        sensor_poll_rate=_read(raw, "sensor_poll_rate", Frequency, field="comms"),
    )


_KNOWN_TOP_LEVEL_SECTIONS = frozenset({"red_led", "blue_led", "comms"})


def load_device_config(path: Path) -> DeviceConfig:
    """Load and fully validate a device-limits TOML file into a `DeviceConfig`.

    Raises `ConfigError` for anything wrong with the file:
    an unknown section, a missing field, an unreadable measurement, or a unit that
    does not belong to the field it was written for.
    """
    with path.open("rb") as handle:
        raw = tomllib.load(handle)

    unknown_sections = set(raw) - _KNOWN_TOP_LEVEL_SECTIONS
    if unknown_sections:
        msg = f"unknown top-level section(s): {', '.join(sorted(unknown_sections))}"
        raise ConfigError(msg)

    missing_sections = _KNOWN_TOP_LEVEL_SECTIONS - set(raw)
    if missing_sections:
        msg = f"missing top-level section(s): {', '.join(sorted(missing_sections))}"
        raise ConfigError(msg)

    return DeviceConfig(
        red_led=_parse_led_limits(raw["red_led"], led_name="red_led"),
        blue_led=_parse_led_limits(raw["blue_led"], led_name="blue_led"),
        comms=_parse_comms(raw["comms"]),
    )
