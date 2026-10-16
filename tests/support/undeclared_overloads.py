"""Products and quotients the runtime allows and the overloads do not declare yet.

The typing contract lags the runtime for these pairs, so a type checker infers
`LinearQuantity | Fraction` for them.
Each is a decision still to be made, not an oversight to paper over: declare the
overload, or refuse the operation at runtime.
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
        ("Acceleration", "/", "Frequency", "Velocity"),
        ("Acceleration", "/", "Velocity", "Frequency"),
        ("AngularVelocity", "/", "AngularDisplacement", "Frequency"),
        ("Area", "*", "EnergyDensity", "Force"),
        ("Charge", "*", "Frequency", "Current"),
        ("Charge", "*", "Voltage", "Energy"),
        ("Conductance", "*", "Resistance", "Fraction"),
        ("Current", "/", "Charge", "Frequency"),
        ("Current", "/", "Frequency", "Charge"),
        ("Energy", "*", "Frequency", "Power"),
        ("Energy", "/", "Charge", "Voltage"),
        ("Energy", "/", "Force", "Length"),
        ("Energy", "/", "Length", "Force"),
        ("Energy", "/", "Voltage", "Charge"),
        ("EnergyDensity", "*", "Area", "Force"),
        ("EnergyDensity", "/", "Pressure", "Fraction"),
        ("Force", "*", "Length", "Energy"),
        ("Force", "*", "Velocity", "Power"),
        ("Force", "/", "EnergyDensity", "Area"),
        ("Frequency", "*", "Charge", "Current"),
        ("Frequency", "*", "Energy", "Power"),
        ("Frequency", "*", "Length", "Velocity"),
        ("Frequency", "*", "Velocity", "Acceleration"),
        ("Length", "*", "Force", "Energy"),
        ("Length", "*", "Frequency", "Velocity"),
        ("Power", "/", "Energy", "Frequency"),
        ("Power", "/", "Force", "Velocity"),
        ("Power", "/", "Frequency", "Energy"),
        ("Power", "/", "Velocity", "Force"),
        ("Pressure", "/", "EnergyDensity", "Fraction"),
        ("Resistance", "*", "Conductance", "Fraction"),
        ("Velocity", "*", "Force", "Power"),
        ("Velocity", "*", "Frequency", "Acceleration"),
        ("Velocity", "/", "Length", "Frequency"),
        ("Voltage", "*", "Charge", "Energy"),
    }
)
