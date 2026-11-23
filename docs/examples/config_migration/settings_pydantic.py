"""Rung 1, Pydantic: annotate the fields, and the whole file validates.

`loads` hands the TOML to Pydantic exactly as `tomllib` returned it: nested tables and
strings that hold a number and a unit.
The annotations say which quantity each field is and how far the tester's hardware lets
it go, and Pydantic walks the file, builds the typed objects, and reports every mistake
in it at once.

Needs `pip install "kuchka[pydantic]"`.
"""

from __future__ import annotations

import tomllib
from typing import Annotated
from typing import Self

from fixture import MAX_CURRENT
from fixture import MAX_TEMPERATURE
from fixture import MAX_VOLTAGE
from fixture import MIN_TEMPERATURE
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import model_validator

from kuchka import BaudRate
from kuchka import Current
from kuchka import Frequency
from kuchka import Milliampere
from kuchka import Temperature
from kuchka import Voltage
from kuchka.pydantic import Bounds
from kuchka.pydantic import Quantity

SafeVoltage = Annotated[Voltage, Quantity, Bounds(ge=-MAX_VOLTAGE, le=MAX_VOLTAGE)]
SafeCurrent = Annotated[Current, Quantity, Bounds(ge=Milliampere(0), le=MAX_CURRENT)]
SafeTemperature = Annotated[
    Temperature, Quantity, Bounds(ge=MIN_TEMPERATURE, le=MAX_TEMPERATURE)
]


class _Section(BaseModel):
    """A table of the file: unknown keys are mistakes, and nothing changes later."""

    model_config = ConfigDict(frozen=True, extra="forbid")


class VoltageWindow(_Section):
    """The accepted voltage range of one LED."""

    minimum: SafeVoltage
    maximum: SafeVoltage

    @model_validator(mode="after")
    def _ordered(self) -> Self:
        Bounds(ge=self.minimum, le=self.maximum)  # raises ValueError when inverted
        return self


class CurrentWindow(_Section):
    """The accepted current range of one LED."""

    minimum: SafeCurrent
    maximum: SafeCurrent

    @model_validator(mode="after")
    def _ordered(self) -> Self:
        Bounds(ge=self.minimum, le=self.maximum)  # raises ValueError when inverted
        return self


class TemperatureWindow(_Section):
    """The accepted case-temperature range of one LED."""

    minimum: SafeTemperature
    maximum: SafeTemperature

    @model_validator(mode="after")
    def _ordered(self) -> Self:
        Bounds(ge=self.minimum, le=self.maximum)  # raises ValueError when inverted
        return self


class LedLimits(_Section):
    """Everything a measured LED has to stay within."""

    accepted_voltage: VoltageWindow
    accepted_current: CurrentWindow
    accepted_temperature: TemperatureWindow


class CommsSettings(_Section):
    """How fast the board talks, and how often the fixture polls it."""

    uart_baud_rate: Annotated[BaudRate, Quantity]
    sensor_poll_rate: Annotated[Frequency, Quantity]


class DeviceConfig(_Section):
    """The typed configuration the rest of the application sees."""

    red_led: LedLimits
    blue_led: LedLimits
    comms: CommsSettings


def loads(text: str) -> DeviceConfig:
    """Read a limits file from its TOML text; raises `pydantic.ValidationError`."""
    return DeviceConfig.model_validate(tomllib.loads(text))
