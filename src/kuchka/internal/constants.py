"""Internal constants that are used across `kuchka`."""

from decimal import Decimal
from fractions import Fraction

PI = Fraction(
    Decimal(
        "3.1415926535897932384626433832795028841971693993751058209749445923"
        "078164062862089986280348253421170679"
    )
)
"""Pi as an exact rational, the first 100 decimal places.

The error against the true value is below 1E-100.
The `Radian` scale uses it, because a radian is the one angular unit related to a turn
by an irrational number (one turn is 2 pi radians), and every other angular unit is a
plain rational fraction of a turn.
So do the units defined through a radian: the square degree, the torque per radian, the
lambert, and the parsec, which is 648000/pi astronomical units.
"""

__all__ = ["PI"]
