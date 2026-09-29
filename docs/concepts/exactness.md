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
The non-radian angular scales are defined from a fixed rational internal representation of pi - fifteen decimal places, the precision commonly cited by NASA/JPL.
Thus, `Degree`, `Turn`, `Gradian`, `ArcMinute`, and `ArcSecond` remain mutually exact relative to that constant, importable as `kuchka.units.angular._PI` if you need to compare against it directly.

The finite approximation becomes observable when an angle crosses into `Radian`:

```python
import math
from decimal import Decimal

from kuchka import Degree
from kuchka import Radian
from kuchka.units.angular import _PI

 Radian(_PI) == Degree(180)
# True -- `_PI` is kuchka's own fixed internal constant.
Radian(math.pi) == Degree(180)
# True -- `math.pi` is read as its shortest decimal string, 3.141592653589793, which is `_PI`.
Radian(Decimal("3.14159265358979323846")) == Degree(180)
# False -- a pi with more digits differs from `_PI`.
```

## Logarithmic conversions

Levels (`LogarithmicRatio`) store an exact `Fraction` and every combination of levels is exact.
Converting a level to or from a linear ratio evaluates a logarithm, which is irrational for a general ratio.
That conversion runs in `Decimal` at the active context precision and stores the exact `Fraction` of the resulting `Decimal`.
Whole multiples of 10 dB (power) or 20 dB (field) convert to exact powers of ten.
