"""Test Kuchka as an independently installed consumer dependency."""

import sys
import unittest
from importlib.util import find_spec

from kuchka import Ampere
from kuchka import Ohm
from kuchka import Volt
from kuchka import Watt


class ConsumerContractTests(unittest.TestCase):
    """Exercise documented public functionality."""

    def test_resistive_load_calculation(self) -> None:
        """Calculate current and power for a resistive load."""
        supply = Volt(12)
        resistance = Ohm(6)

        current = supply / resistance
        power = supply * current

        self.assertEqual(current, Ampere(2))  # noqa: PT009
        self.assertEqual(power, Watt(24))  # noqa: PT009

    def test_mypy_is_not_a_runtime_dependency(self) -> None:
        """A consumer must not need the development type checker."""
        self.assertIsNone(find_spec("mypy"))  # noqa: PT009

    @unittest.skipIf(
        sys.version_info >= (3, 12),
        "typing_extensions is only required below Python 3.12",
    )
    def test_typing_extensions_is_available_on_python_311(self) -> None:
        """Check the conditional runtime dependency."""
        self.assertIsNotNone(find_spec("typing_extensions"))  # noqa: PT009


if __name__ == "__main__":
    unittest.main()
