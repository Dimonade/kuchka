"""Internal constants that are used across `kuchka`."""

from decimal import Decimal
from fractions import Fraction

_PI = Fraction(Decimal("3.141592653589793"))
"""kuchka's own fixed, finite rational representation of pi.

Fifteen significant digits, the precision commonly cited by NASA/JPL for spacecraft
navigation.
See: https://www.jpl.nasa.gov/edu/news/how-many-decimals-of-pi-do-we-really-need/

Defines the scales of Degree, Turn, Gradian, ArcMinute, and ArcSecond relative to
Radian.
Otherwise, currently not used anywhere else in kuchka.
"""

__all__ = ["_PI"]
