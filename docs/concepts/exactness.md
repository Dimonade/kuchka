# Exactness and angular units

Every magnitude in `kuchka` is stored as an exact `Fraction`.

`int` and `Decimal` values can therefore enter the system without rounding.
`float` input is parsed through its string representation first, so `Volt(4.2)` keeps the digits written by the programmer instead of the binary floating-point representation.

```python
from fractions import Fraction
from kuchka import Litre
from kuchka.units import LITRE

q = Litre(Fraction(5, 18))
q.magnitude
# Fraction(1, 3600) -- Volume's canonical unit is `CubicMetre`, not `Litre`.
q.value_in(LITRE)
# Fraction(5, 18) -- exact, recovered in the unit it was constructed with.
```

`.magnitude` reads out in the canonical unit.
`.value_in(unit)` reads out in any compatible unit.
Both stay exact regardless of which one is summoned.
The scale factor between litres and cubic metres (`1/1000`) is itself an exact `Fraction`, so nothing is lost converting between them.

`Decimal` is materialized for display:

```python
repr(q)
# 0.2777777777777777777777777778 L
```

## The boundary at pi

A finite `Fraction` cannot represent the mathematical value of pi.
Rejecting angular units or pretending that a finite decimal is mathematically exact would both be poor fits for the library's model.

`Radian` is the canonical angle unit.
The non-radian angular scales are defined from a fixed rational internal representation of pi - fifteen significant digits, the precision commonly cited by NASA/JPL.
Thus, `Degree`, `Turn`, `Gradian`, `ArcMinute`, and `ArcSecond` remain mutually exact relative to that constant, importable as `kuchka.units.angular._PI` if you need to compare against it directly.

The finite approximation becomes observable when an angle crosses into `Radian`:

```python
Radian(_PI) == Degree(180)
```

where `_PI` is kuchka's own fixed internal constant.
