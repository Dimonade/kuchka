"""Products and quotients the runtime allows and the overloads leave undeclared.

A type checker infers `LinearQuantity | Fraction` for these pairs.
Each group waits on a decision of its own:

- `Force * Length` and the quotients that undo it. A newton-metre is an energy, and
  `Torque.from_force` is the way to a torque, so the group waits on a ruling between
  declaring the pair and refusing it at runtime.
- `Conductance * Resistance` and its commuted form. The product is exactly one, so it
  waits on the ruling about dimensionless counts and ratios.

The list may only shrink: `test_overloads` fails when a pair is declared and still
listed, and when a new undeclared pair appears.

Pairs with a role kind (`BaudRate`, `SampleRate`, `SamplingPeriod`) and pairs with a
`Proportion` are excluded by rule and not listed: the runtime combines a role by
dimension and the overloads leave it to the general kind, and a `Proportion` keeps
the kind of the other operand.
"""

from __future__ import annotations

UNDECLARED: frozenset[tuple[str, str, str, str]] = frozenset(
    {
        ("Conductance", "*", "Resistance", "Fraction"),
        ("Energy", "/", "Force", "Length"),
        ("Energy", "/", "Length", "Force"),
        ("Force", "*", "Length", "Energy"),
        ("Length", "*", "Force", "Energy"),
        ("Resistance", "*", "Conductance", "Fraction"),
    }
)
