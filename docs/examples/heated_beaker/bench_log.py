"""Boundary layer and analysis for a heated-beaker run.

A stepper-driven lever carries a beaker of liquid toward and away from a heat source.
The encoder reports the lever angle, the driver reports its voltage and current, and a
temperature sensor reports the liquid.
A TOML file holds the limits and a CSV file holds the run.
Every cell of both is a number with its unit, read once by `parse`;
past `load_spec` and `read_log` nothing is a bare number or a unit string.
"""

from __future__ import annotations

import csv
import tomllib
from dataclasses import dataclass
from itertools import pairwise
from typing import TYPE_CHECKING
from typing import TypeVar

from kuchka import Angle
from kuchka import AngularDisplacement
from kuchka import Current
from kuchka import Energy
from kuchka import HeatingRate
from kuchka import Instant
from kuchka import Joule
from kuchka import Temperature
from kuchka import TemperatureDelta
from kuchka import Time
from kuchka import Voltage
from kuchka import parse
from kuchka.errors import ParseError

if TYPE_CHECKING:
    from collections.abc import Sequence
    from pathlib import Path

_QuantityT = TypeVar(
    "_QuantityT",
    Angle,
    AngularDisplacement,
    Current,
    HeatingRate,
    Instant,
    Temperature,
    TemperatureDelta,
    Voltage,
)


class BenchError(Exception):
    """A spec or a log could not be read into typed values."""


def _read(text: object, quantity: type[_QuantityT], *, where: str) -> _QuantityT:
    """Read `text` as a `quantity`, or fail naming `where` and why."""
    if not isinstance(text, str):
        msg = f"{where}: expected a number with its unit as text, got {text!r}"
        raise BenchError(msg)
    try:
        return parse(text, quantity)
    except ParseError as exc:
        msg = f"{where}: {exc}"
        raise BenchError(msg) from exc


@dataclass(frozen=True)
class BenchSpec:
    """The limits of one run, in the units of the quantities they are."""

    home: Angle
    max_travel: AngularDisplacement
    position_tolerance: Angle
    window_min: Temperature
    window_max: Temperature
    setpoint: Temperature
    setpoint_tolerance: TemperatureDelta
    max_heating_rate: HeatingRate
    max_motor_voltage: Voltage

    def __post_init__(self) -> None:
        if not self.window_min <= self.setpoint <= self.window_max:
            msg = "the setpoint lies outside the liquid's window"
            raise BenchError(msg)


def load_spec(path: Path) -> BenchSpec:
    """Read the limits of a run from a TOML file."""
    with path.open("rb") as handle:
        raw = tomllib.load(handle)

    def field(section: str, key: str, quantity: type[_QuantityT]) -> _QuantityT:
        try:
            text = raw[section][key]
        except KeyError as exc:
            msg = f"{section}.{key}: missing"
            raise BenchError(msg) from exc
        return _read(text, quantity, where=f"{section}.{key}")

    return BenchSpec(
        home=field("lever", "home", Angle),
        max_travel=field("lever", "max_travel", AngularDisplacement),
        position_tolerance=field("lever", "position_tolerance", Angle),
        window_min=field("liquid", "window_min", Temperature),
        window_max=field("liquid", "window_max", Temperature),
        setpoint=field("liquid", "setpoint", Temperature),
        setpoint_tolerance=field("liquid", "setpoint_tolerance", TemperatureDelta),
        max_heating_rate=field("liquid", "max_heating_rate", HeatingRate),
        max_motor_voltage=field("motor", "max_voltage", Voltage),
    )


@dataclass(frozen=True)
class Sample:
    """One row of the log."""

    time: Instant
    angle: Angle
    voltage: Voltage
    current: Current
    temperature: Temperature


def _cell(
    row: dict[str, str], column: str, quantity: type[_QuantityT], *, where: str
) -> _QuantityT:
    """Read one cell of a log row as a `quantity`."""
    if column not in row:
        msg = f"{where}: missing column {column!r}"
        raise BenchError(msg)
    return _read(row[column], quantity, where=f"{where}, {column}")


def read_log(path: Path) -> list[Sample]:
    """Read the samples of a run from a CSV file."""
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    samples = []
    for line, row in enumerate(rows, start=2):
        where = f"{path.name}, line {line}"
        samples.append(
            Sample(
                time=_cell(row, "time", Instant, where=where),
                angle=_cell(row, "lever_angle", Angle, where=where),
                voltage=_cell(row, "motor_voltage", Voltage, where=where),
                current=_cell(row, "motor_current", Current, where=where),
                temperature=_cell(row, "temperature", Temperature, where=where),
            ),
        )
    return samples


@dataclass(frozen=True)
class Report:
    """What a run did, measured against its spec."""

    travel: AngularDisplacement
    peak_voltage: Voltage
    peak_heating_rate: HeatingRate
    time_to_setpoint: Time | None
    excursions: tuple[Instant, ...]
    returned_home: bool
    motor_energy: Energy


def analyse(spec: BenchSpec, samples: Sequence[Sample]) -> Report:
    """Measure a run against its spec."""
    first = samples[0]
    swing = (s.angle.difference(spec.home).to_angular_displacement() for s in samples)
    settled = next(
        (
            s
            for s in samples
            if s.temperature.is_close(spec.setpoint, tolerance=spec.setpoint_tolerance)
        ),
        None,
    )
    inside = [spec.window_min <= s.temperature <= spec.window_max for s in samples]
    entered = inside.index(True) if True in inside else len(samples)
    return Report(
        travel=max(abs(d) for d in swing),
        peak_voltage=max(s.voltage for s in samples),
        peak_heating_rate=max(
            (b.temperature - a.temperature) / (b.time - a.time)
            for a, b in pairwise(samples)
        ),
        time_to_setpoint=None if settled is None else settled.time - first.time,
        excursions=tuple(
            s.time
            for s, ok in zip(samples[entered:], inside[entered:], strict=True)
            if not ok
        ),
        returned_home=samples[-1].angle.is_close(
            spec.home, tolerance=spec.position_tolerance
        ),
        motor_energy=sum(
            (a.voltage * a.current * (b.time - a.time) for a, b in pairwise(samples)),
            Joule(0),
        ),
    )
