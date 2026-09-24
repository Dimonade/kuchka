"""A collections of symbols.

The symbols include things like:
- a degree (i.e., in Celsius),
- delta (i.e., in Delta Kelvin),
- micro (i.e., in Microvolt),
and others, to avoid redefining them everywhere.
"""

ANGLE = "\u2220"
DEGREE = "\u00b0"
DELTA = "\u0394"
DOUBLE_PRIME = "\u2033"
OMEGA = "\u03a9"
MICRO = "\u00b5"
SUPERSCRIPT_ZERO = "\u2070"
SUPERSCRIPT_ONE = "\u00b9"
SUPERSCRIPT_TWO = "\u00b2"
SUPERSCRIPT_THREE = "\u00b3"
SUPERSCRIPT_FOUR = "\u2074"
SUPERSCRIPT_FIVE = "\u2075"
SUPERSCRIPT_SIX = "\u2076"
SUPERSCRIPT_SEVEN = "\u2077"
SUPERSCRIPT_EIGHT = "\u2078"
SUPERSCRIPT_NINE = "\u2079"
SUPERSCRIPT_PLUS_SIGN = "\u207a"
SUPERSCRIPT_MINUS_SIGN = "\u207b"
SUPERSCRIPT_SMALL_I = "\u2071"
SUPERSCRIPT_SMALL_N = "\u207f"
SUPERSCRIPT_LEFT_PARENTHESIS = "\u207d"
SUPERSCRIPT_RIGHT_PARENTHESIS = "\u207e"
SMALL_MICRO = "\u03bc"
PRIME = "\u2032"
THETA = "\u0398"


_SUPERSCRIPT_TRANSLATION = str.maketrans(
    "0123456789+-",
    (
        SUPERSCRIPT_ZERO
        + SUPERSCRIPT_ONE
        + SUPERSCRIPT_TWO
        + SUPERSCRIPT_THREE
        + SUPERSCRIPT_FOUR
        + SUPERSCRIPT_FIVE
        + SUPERSCRIPT_SIX
        + SUPERSCRIPT_SEVEN
        + SUPERSCRIPT_EIGHT
        + SUPERSCRIPT_NINE
        + SUPERSCRIPT_PLUS_SIGN
        + SUPERSCRIPT_MINUS_SIGN
    ),
)


def get_superscript(exponent: int) -> str:
    """Map an integer exponent to its Unicode superscript representation."""
    if exponent == 0:
        return ""
    return str(exponent).translate(_SUPERSCRIPT_TRANSLATION)


__all__ = ["get_superscript"]
