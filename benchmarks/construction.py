"""Construction and arithmetic throughput, measured with the standard library.

This script prints both a human-readable table and the interpreter/platform
info needed to make the numbers reproducible, since throughput numbers
without that context are not comparable between machines.
"""

from __future__ import annotations

import platform
import sys
import timeit
from dataclasses import dataclass
from decimal import Decimal

SAMPLE_COUNT = 200_000
"""Iterations per timed case. Large enough that per-call overhead in
`timeit` itself is negligible relative to the measured work, small enough
that the whole script runs in a few seconds.
"""

BATCH_SIZE = 1000
"""Size of the list used in the batch-construction case, to approximate a
burst read from an acquisition buffer rather than one sample at a time.
"""


@dataclass(frozen=True)
class BenchmarkCase:
    """One timed case: a label, the code under test, and its setup."""

    label: str
    stmt: str
    setup: str
    iterations_per_call: int = 1
    """How many samples one `stmt` execution represents.

    1 for a single construction/arithmetic call; `BATCH_SIZE` for the batch
    case, so its MSa/s figure is directly comparable to the single-call
    cases instead of reporting "batches per second".
    """


CASES: list[BenchmarkCase] = [
    BenchmarkCase(
        label="raw float divide (no correctness guarantees)",
        stmt="raw / 1000.0",
        setup="raw = 2350.0",
    ),
    BenchmarkCase(
        label="Decimal(str(x)) * scale (kuchka's own cost, no wrapper)",
        stmt="Decimal(str(raw)) * SCALE",
        setup="from decimal import Decimal; raw = 2350.0; SCALE = Decimal('0.001')",
    ),
    BenchmarkCase(
        label="Millivolt(x): a single kuchka construction",
        stmt="Millivolt(2350)",
        setup="from kuchka import Millivolt",
    ),
    BenchmarkCase(
        label=f"Millivolt(x) over a batch of {BATCH_SIZE} raw readings",
        stmt="[Millivolt(v) for v in readings]",
        setup=(
            f"from kuchka import Millivolt\nreadings = list(range(1, {BATCH_SIZE} + 1))"
        ),
        iterations_per_call=BATCH_SIZE,
    ),
    BenchmarkCase(
        label="Voltage + Voltage (steady-state hot-loop addition)",
        stmt="a + b",
        setup=(
            "from decimal import Decimal\n"
            "from kuchka import Volt\n"
            "a = Volt(5)\n"
            "b = Volt(Decimal('0.2'))"
        ),
    ),
    BenchmarkCase(
        label="Voltage / Current -> Resistance (Ohm's law, one division)",
        stmt="voltage / current",
        setup="from kuchka import Volt, Ampere; voltage = Volt(5); current = Ampere(2)",
    ),
]


def run_case(case: BenchmarkCase) -> tuple[float, float]:
    """Return (seconds per single call, million-samples-per-second)."""
    elapsed = timeit.timeit(case.stmt, setup=case.setup, number=SAMPLE_COUNT)
    samples = SAMPLE_COUNT * case.iterations_per_call
    seconds_per_sample = elapsed / samples
    msamples_per_second = samples / elapsed / 1_000_000
    return seconds_per_sample, msamples_per_second


def print_environment() -> None:
    """Print interpreter/platform info the numbers below need to be comparable."""
    print("environment:")
    print(f"  python:   {sys.version.split()[0]} ({platform.python_implementation()})")
    print(f"  platform: {platform.platform()}")
    print(f"  machine:  {platform.machine()}")
    print(f"  decimal:  {Decimal(1).__class__.__module__}")  # C or pure-python backend
    print()


def print_results(rows: list[tuple[str, float, float]]) -> None:
    """Print the results table, plus a ready-to-paste Markdown version."""
    label_width = max(len(label) for label, _, _ in rows)
    print(f"{'case':<{label_width}}  {'us/sample':>12}  {'MSa/s':>10}")
    print(f"{'-' * label_width}  {'-' * 12}  {'-' * 10}")
    for label, seconds_per_sample, msamples_per_second in rows:
        print(
            f"{label:<{label_width}}  "
            f"{seconds_per_sample * 1_000_000:>12.4f}  "
            f"{msamples_per_second:>10.4f}"
        )
    print()
    print("Markdown, for pasting into the README's Performance section:")
    print()
    print("| Case | us/sample | MSa/s |")
    print("| --- | ---: | ---: |")
    for label, seconds_per_sample, msamples_per_second in rows:
        print(
            f"| {label} | {seconds_per_sample * 1_000_000:.4f} | "
            f"{msamples_per_second:.4f} |"
        )


def main() -> None:
    """Run every case and print the results."""
    print_environment()
    rows = [(case.label, *run_case(case)) for case in CASES]
    print_results(rows)


if __name__ == "__main__":
    main()
