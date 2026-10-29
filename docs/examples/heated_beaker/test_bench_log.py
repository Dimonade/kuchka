"""Tests for bench_log.py.

This directory is documentation, not part of the installed `kuchka` package,
so `bench_log` is imported by adding this directory to `sys.path`.

Run with `pytest docs/examples/heated_beaker` from the repository root, or `pytest`
from inside this directory.
"""

from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pytest
from bench_log import BenchError
from bench_log import Sample
from bench_log import analyse
from bench_log import load_spec
from bench_log import read_log

from kuchka import Celsius
from kuchka import Degree
from kuchka import DegreeDisplacement
from kuchka import DeltaKelvin
from kuchka import Joule
from kuchka import KelvinPerSecond
from kuchka import Milliampere
from kuchka import Second
from kuchka import Volt

HERE = Path(__file__).parent
SPEC = (HERE / "bench_spec.toml").read_text(encoding="utf-8")
LOG = (HERE / "run_log.csv").read_text(encoding="utf-8")


def spec_with(tmp_path: Path, old: str, new: str) -> Path:
    path = tmp_path / "bench_spec.toml"
    path.write_text(SPEC.replace(old, new), encoding="utf-8")
    return path


def log_with(tmp_path: Path, old: str, new: str) -> Path:
    path = tmp_path / "run_log.csv"
    path.write_text(LOG.replace(old, new), encoding="utf-8")
    return path


def test_the_shipped_spec_is_typed_quantities() -> None:
    spec = load_spec(HERE / "bench_spec.toml")
    assert spec.setpoint == Celsius(62)
    assert spec.setpoint_tolerance == DeltaKelvin(Decimal("0.5"))
    assert spec.max_motor_voltage == Volt(12)


def test_cells_in_different_units_read_as_the_same_kind_of_quantity() -> None:
    samples = read_log(HERE / "run_log.csv")
    assert samples[5].voltage == Volt(Decimal("11.7"))  # Written as 11700 mV.
    assert samples[5].current == Milliampere(300)  # Written as 0.3 A.
    reading = samples[7].temperature  # Written as 143.8 °F.
    assert reading.is_close(
        Celsius(Decimal("62.1")), tolerance=DeltaKelvin(Decimal("0.05"))
    )


def test_the_report_of_the_shipped_run() -> None:
    report = analyse(
        load_spec(HERE / "bench_spec.toml"), read_log(HERE / "run_log.csv")
    )
    assert report.travel == DegreeDisplacement(Decimal("22.2"))
    assert report.peak_voltage == Volt(Decimal("11.9"))
    assert report.peak_heating_rate == KelvinPerSecond(Decimal("0.88"))
    assert report.time_to_setpoint == Second(50)
    assert report.excursions == tuple(Second(s).to_instant() for s in (80, 110, 120))
    assert report.returned_home
    assert report.motor_energy == Joule(Decimal("296.81"))


def test_travel_is_measured_across_the_encoder_wrap() -> None:
    spec = load_spec(HERE / "bench_spec.toml")
    samples = [
        Sample(
            Second(t).to_instant(), Degree(angle), Volt(0), Milliampere(0), Celsius(62)
        )
        for t, angle in ((0, 350), (1, 4))
    ]
    assert analyse(spec, samples).travel == DegreeDisplacement(14)


@pytest.mark.parametrize(
    ("old", "new", "match"),
    [
        ('"12 V"', '"12 A"', "motor.max_voltage.*not a unit of Voltage"),
        ('"62 °C"', "62", "liquid.setpoint: expected a number with its unit as text"),
        ('"0.5 ΔK"', '"0.5 K"', "setpoint_tolerance.*not a unit of TemperatureDelta"),
        ('"62 °C"', '"70 °C"', "setpoint lies outside"),
        ("[motor]", "[engine]", "motor.max_voltage: missing"),
    ],
)
def test_a_broken_spec_fails_at_load_naming_the_field(
    tmp_path: Path, old: str, new: str, match: str
) -> None:
    with pytest.raises(BenchError, match=match):
        load_spec(spec_with(tmp_path, old, new))


@pytest.mark.parametrize(
    ("old", "new", "match"),
    [
        ("0.3 A", "0.3 V", "line 7, motor_current.*not a unit of Current"),
        ("61.8 °C", "61.8", "line 7, temperature"),
        ("10 s,355 deg", "10 s,355 gradle", "line 3, lever_angle"),
        ("motor_current", "motor_amps", "missing column 'motor_current'"),
    ],
)
def test_a_broken_log_fails_at_read_naming_the_line_and_column(
    tmp_path: Path, old: str, new: str, match: str
) -> None:
    with pytest.raises(BenchError, match=match):
        read_log(log_with(tmp_path, old, new))
