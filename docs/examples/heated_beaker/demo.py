"""Run this file directly: `python demo.py` from this directory.

Reads the shipped spec and log, prints what the run did, then breaks the inputs
three ways to show what the boundary layer catches.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from bench_log import BenchError
from bench_log import analyse
from bench_log import load_spec
from bench_log import read_log

from kuchka.units import MILLIWATT_HOUR

HERE = Path(__file__).parent


def main() -> None:
    """Report on the shipped run, then show three broken inputs."""
    spec = load_spec(HERE / "bench_spec.toml")
    report = analyse(spec, read_log(HERE / "run_log.csv"))

    print("The run, against its spec:\n")
    print(f"  lever travel:      {report.travel} (limit {spec.max_travel})")
    print(
        f"  peak motor volts:  {report.peak_voltage} (limit {spec.max_motor_voltage})"
    )
    print(f"  peak heating rate: {report.peak_heating_rate}", end="")
    print(f" (limit {spec.max_heating_rate})")
    print(f"  time to setpoint:  {report.time_to_setpoint}")
    print(f"  left the window:   {', '.join(map(str, report.excursions))}")
    print(f"  back at home:      {report.returned_home}")
    print(f"  motor energy:      {report.motor_energy.to(MILLIWATT_HOUR):.1f}")

    print("\nThree ways an input can go wrong:\n")
    _break(
        "1. A current written in volts",
        "run_log.csv",
        "0.3 A",
        "0.3 V",
    )
    _break(
        "2. A setpoint written as a bare TOML number, with no unit",
        "bench_spec.toml",
        'setpoint = "62 °C"',
        "setpoint = 62",
    )
    _break(
        "3. A tolerance written as a temperature, not a temperature difference",
        "bench_spec.toml",
        '"0.5 ΔK"',
        '"0.5 K"',
    )


def _break(description: str, name: str, old: str, new: str) -> None:
    """Copy the shipped inputs with `old` replaced by `new` in `name`, and load them."""
    print(f"  {description}")
    with tempfile.TemporaryDirectory() as folder:
        for source in ("bench_spec.toml", "run_log.csv"):
            text = (HERE / source).read_text(encoding="utf-8")
            if source == name:
                text = text.replace(old, new)
            (Path(folder) / source).write_text(text, encoding="utf-8")
        try:
            load_spec(Path(folder) / "bench_spec.toml")
            read_log(Path(folder) / "run_log.csv")
        except BenchError as error:
            print(f"     -> BenchError: {error}\n")
        else:
            print("     -> unexpectedly succeeded\n")


if __name__ == "__main__":
    main()
