"""Products and quotients the runtime allows and the overloads leave undeclared.

A type checker infers `LinearQuantity | Fraction` for these pairs.
Each group waits on a decision of its own:

- `Force * Length` and the quotients that undo it. A newton-metre is an energy, and
  `Torque.from_force` is the way to a torque, so the group waits on a ruling between
  declaring the pair and refusing it at runtime.
- `EnergyDensity / Pressure` and its reciprocal. The two kinds share a dimension, so
  the quotient waits on dimensionless results being `Proportion`s.
- `Conductance * Resistance` and its commuted form. The product is exactly one, so it
  waits on the ruling about dimensionless counts and ratios.

The list may only shrink: `test_overloads` fails when a pair is declared and still
listed, and when a new undeclared pair appears.

Two kinds of pair are excluded by rule, and not listed:

- the quotient of two quantities of one kind, which is a plain `Fraction` until
  dimensionless results are `Proportion`s;
- any pair with a role kind (`BaudRate`, `SampleRate`, `SamplingPeriod`), which the
  runtime combines by dimension and the overloads leave to the general kind.
"""

from __future__ import annotations

UNDECLARED: frozenset[tuple[str, str, str, str]] = frozenset(
    {
        ("Conductance", "*", "Resistance", "Fraction"),
        ("Energy", "/", "Force", "Length"),
        ("Energy", "/", "Length", "Force"),
        ("EnergyDensity", "/", "Pressure", "Fraction"),
        ("Force", "*", "Length", "Energy"),
        ("Length", "*", "Force", "Energy"),
        ("Pressure", "/", "EnergyDensity", "Fraction"),
        ("Resistance", "*", "Conductance", "Fraction"),
    }
)
