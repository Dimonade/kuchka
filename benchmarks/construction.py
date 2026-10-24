"""Construction and arithmetic throughput, measured with the standard library.

This script prints a human-readable table, a Markdown version of it, and the
interpreter, platform, and `kuchka` tree the numbers came from, since throughput
numbers without that context are not comparable between machines.

Every case runs enough executions to fill a fixed time slice, is timed several times,
and reports its best time together with how far the median repeat lies above it, so a
noisy machine shows up in the table and not only in the conclusion.
"""

from __future__ import annotations

import argparse
import cProfile
import platform
import pstats
import statistics
import sys
import timeit
from dataclasses import dataclass
from decimal import Decimal

import kuchka

REPEATS = 7
"""How many times each case is timed; the best of them is the reported figure.

The best repeat is the one least disturbed by the rest of the machine, which is why the
`timeit` documentation recommends it over the mean.
"""

NOISY_SPREAD = 0.05
"""Median-over-best spread of a case above which its row is flagged."""

BATCH_SIZE = 1000
"""Size of the list used in the batch-construction case.

Used to approximate a burst read from an acquisition buffer rather than one sample at
a time.
"""

PROFILED_CONSTRUCTIONS = 20_000
"""Constructions run under the profiler by `--profile`."""


@dataclass(frozen=True)
class BenchmarkCase:
    """One timed case: a label, the code under test, and its setup."""

    label: str
    stmt: str
    setup: str
    iterations_per_call: int = 1
    """How many samples one `stmt` execution represents.

    1 for a single construction/arithmetic call;
    `BATCH_SIZE` for the batch case, so its MSa/s figure is directly comparable to the
    single-call cases instead of reporting "batches per second".
    """


@dataclass(frozen=True)
class Result:
    """The measurement of one case."""

    label: str
    seconds_per_sample: float
    spread: float
    """Median repeat over best repeat, minus one."""


CASES: list[BenchmarkCase] = [
    BenchmarkCase(
        label="raw float divide (no correctness guarantees)",
        stmt="raw / 1000.0",
        setup="raw = 2350.0",
    ),
    BenchmarkCase(
        label="Fraction(x) * scale (kuchka's own construction cost, no wrapper)",
        stmt="Fraction(raw) * SCALE",
        setup=("from fractions import Fraction\nraw = 2350\nSCALE = Fraction(1, 1000)"),
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
        label='parse("2350 mV", Voltage): reading a value from text',
        stmt='parse("2350 mV", Voltage)',
        setup="from kuchka import Voltage, parse",
    ),
    BenchmarkCase(
        label="repr(Millivolt): display cost, not construction",
        stmt="repr(value)",
        setup="from kuchka import Millivolt\nvalue = Millivolt(2350)",
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
        label="Voltage < Voltage (a threshold check)",
        stmt="a < b",
        setup="from kuchka import Volt\na = Volt(5)\nb = Volt(6)",
    ),
    BenchmarkCase(
        label="Voltage * Current -> Power (one multiplication)",
        stmt="voltage * current",
        setup="from kuchka import Volt, Ampere; voltage = Volt(5); current = Ampere(2)",
    ),
    BenchmarkCase(
        label="Voltage / Current -> Resistance (Ohm's law, one division)",
        stmt="voltage / current",
        setup="from kuchka import Volt, Ampere; voltage = Volt(5); current = Ampere(2)",
    ),
]


def run_case(case: BenchmarkCase) -> Result | None:
    """Time `case`, or return `None` when the tree under test cannot run it.

    A tree that predates a feature, such as `parse` in a release before it existed,
    skips that row, so the same script can be pointed at an older tree for a
    like-for-like comparison.
    """
    timer = timeit.Timer(case.stmt, setup=case.setup)
    try:
        number, _ = timer.autorange()
    except (ImportError, AttributeError, NameError):
        return None
    repeats = timer.repeat(repeat=REPEATS, number=number)
    best = min(repeats)
    samples = number * case.iterations_per_call
    return Result(
        label=case.label,
        seconds_per_sample=best / samples,
        spread=statistics.median(repeats) / best - 1,
    )


def loop_overhead() -> float:
    """Return the seconds `timeit` spends per iteration of an empty statement."""
    timer = timeit.Timer("pass")
    number, _ = timer.autorange()
    return min(timer.repeat(repeat=REPEATS, number=number)) / number


def print_environment() -> None:
    """Print interpreter, platform, and tree info the numbers need to be comparable."""
    print("environment:")
    print(f"  python:   {sys.version.split()[0]} ({platform.python_implementation()})")
    print(f"  platform: {platform.platform()}")
    print(f"  machine:  {platform.machine()}")
    print(f"  decimal:  {Decimal(1).__class__.__module__}")  # C or pure-python backend
    print(f"  kuchka:   {kuchka.__file__}")
    print(f"  method:   best of {REPEATS} repeats, each at least 0.2 s")
    print(f"  loop:     {loop_overhead() * 1e9:.1f} ns per empty iteration")
    print()


def print_results(results: list[Result]) -> None:
    """Print the results table, plus a ready-to-paste Markdown version."""
    label_width = max(len(result.label) for result in results)
    print(f"{'case':<{label_width}}  {'us/sample':>10}  {'MSa/s':>9}  {'spread':>7}")
    print(f"{'-' * label_width}  {'-' * 10}  {'-' * 9}  {'-' * 7}")
    for result in results:
        flag = " *" if result.spread > NOISY_SPREAD else ""
        print(
            f"{result.label:<{label_width}}  "
            f"{result.seconds_per_sample * 1e6:>10.4f}  "
            f"{1 / result.seconds_per_sample / 1e6:>9.4f}  "
            f"{result.spread:>7.1%}{flag}"
        )
    if any(result.spread > NOISY_SPREAD for result in results):
        print()
        print(
            f"* the repeats of this case differ by more than {NOISY_SPREAD:.0%}; "
            "rerun on a quieter machine."
        )
    print()
    print("Markdown, for pasting into the README's Results section:")
    print()
    print("| Case | us/sample | MSa/s | spread |")
    print("| --- | ---: | ---: | ---: |")
    for result in results:
        print(
            f"| {result.label} | {result.seconds_per_sample * 1e6:.4f} | "
            f"{1 / result.seconds_per_sample / 1e6:.4f} | {result.spread:.1%} |"
        )


def print_profile() -> None:
    """Print where the time of a `Millivolt(x)` construction goes, per function.

    The profiler slows every call down, so the figures say where the time goes and not
    how long a construction takes.
    """
    from kuchka import Millivolt  # noqa: PLC0415 -- only needed for the profile

    profiler = cProfile.Profile()
    profiler.enable()
    for _ in range(PROFILED_CONSTRUCTIONS):
        Millivolt(2350)
    profiler.disable()
    print(f"profile of {PROFILED_CONSTRUCTIONS} constructions of Millivolt(2350):")
    pstats.Stats(profiler).sort_stats("tottime").print_stats(14)


def main() -> None:
    """Run every case and print the results."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--profile",
        action="store_true",
        help="print where the time of one construction goes instead of timing",
    )
    arguments = parser.parse_args()
    if arguments.profile:
        print_profile()
        return
    print_environment()
    results = [result for case in CASES if (result := run_case(case)) is not None]
    print_results(results)


if __name__ == "__main__":
    main()
