"""Statically invalid code; every line carries `# type: ignore` and must be an error.

A checker that reports an unused ignore turns a line that stopped being an error into
a failure, so the file passes only while each of its lines is rejected.
"""

from kuchka import Ampere
from kuchka import Celsius
from kuchka import Current
from kuchka import Volt

Volt(5) + Ampere(1)  # type: ignore[operator]
Celsius(20) + Celsius(5)  # type: ignore[operator]
current: Current = Volt(1)  # type: ignore[assignment]
