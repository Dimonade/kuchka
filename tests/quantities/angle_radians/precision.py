from fractions import Fraction

PRECISION = Fraction(1, 10**98)


def _true_pi(decimals: int) -> Fraction:
    """Pi from Machin's formula, in integer arithmetic, independent of `PI`."""

    def arctan_of_inverse(x: int, unity: int) -> int:
        total = term = unity // x
        x_squared = x * x
        n = 1
        sign = -1
        while term:
            term //= x_squared
            n += 2
            total += sign * (term // n)
            sign = -sign
        return total

    unity = 10 ** (decimals + 10)
    pi = 4 * (4 * arctan_of_inverse(5, unity) - arctan_of_inverse(239, unity))
    return Fraction(pi, unity)


TRUE_PI = _true_pi(130)
