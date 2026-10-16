"""`is_close` on logarithmic ratios."""

from __future__ import annotations

from kuchka.units import logarithmic


def test_levels_within_the_tolerance_are_close() -> None:
    assert logarithmic.Decibel(3.0).is_close(
        logarithmic.Decibel(3.04), tolerance=logarithmic.Decibel(0.05)
    )
    assert not logarithmic.Decibel(3.0).is_close(
        logarithmic.Decibel(3.06), tolerance=logarithmic.Decibel(0.05)
    )


def test_levels_compare_across_units() -> None:
    assert logarithmic.Decibel(10).is_close(
        logarithmic.Bel(1), tolerance=logarithmic.Decibel(0)
    )
