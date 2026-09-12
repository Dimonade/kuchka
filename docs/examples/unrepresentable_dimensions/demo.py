"""Run this file directly: `python demo.py` from this directory."""

from __future__ import annotations

from resistor_network import parallel
from resistor_network import power_dissipation
from resistor_network import series

from kuchka import Ohm
from kuchka import Volt


def main() -> None:
    """Show parallel/series resistance and power dissipation."""
    print(f"100 ohm || 100 ohm = {parallel(Ohm(100), Ohm(100))}")
    print(f"60 ohm || 30 ohm   = {parallel(Ohm(60), Ohm(30))}")
    print(f"60 ohm + 30 ohm    = {series(Ohm(60), Ohm(30))}")

    power = power_dissipation(Volt(10), Ohm(5))
    print(f"10 V across 5 ohm  = {power}")


if __name__ == "__main__":
    main()
