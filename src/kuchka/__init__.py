"""kuchka -- a small pile of physically-typed units for engineering code.

    from kuchka import Volt, Milliampere

    voltage = Volt(4.2)
    current = Milliampere(150)
    power = voltage * current   # -> Power, computed and typed automatically

Everything below is the entire intended public surface.
Internal modules (``quantities``, ``dimensions``, ``numeric``, ...) are implementation
details and are not part of the supported API.
"""

from kuchka.errors import IncompatibleDimensionError
from kuchka.errors import InvalidConversionError
from kuchka.errors import InvalidMeasurementError
from kuchka.errors import MeasurementError
from kuchka.errors import UnrepresentableDimensionError
from kuchka.quantities import Current
from kuchka.quantities import Power
from kuchka.quantities import Resistance
from kuchka.quantities import TemperatureDelta
from kuchka.quantities import Voltage
from kuchka.temperature import Celsius
from kuchka.temperature import DeltaCelsius
from kuchka.temperature import DeltaKelvin
from kuchka.temperature import Kelvin
from kuchka.temperature import Temperature
from kuchka.units import Ampere
from kuchka.units import Kiloampere
from kuchka.units import Kiloohm
from kuchka.units import Kilovolt
from kuchka.units import Kilowatt
from kuchka.units import Megaohm
from kuchka.units import Microampere
from kuchka.units import Microvolt
from kuchka.units import Milliampere
from kuchka.units import Milliohm
from kuchka.units import Millivolt
from kuchka.units import Milliwatt
from kuchka.units import Ohm
from kuchka.units import Volt
from kuchka.units import Watt

__all__: list[str] = [
    "Ampere",
    "Celsius",
    "Current",
    "DeltaCelsius",
    "DeltaKelvin",
    "IncompatibleDimensionError",
    "InvalidConversionError",
    "InvalidMeasurementError",
    "Kelvin",
    "Kiloampere",
    "Kiloohm",
    "Kilovolt",
    "Kilowatt",
    "MeasurementError",
    "Megaohm",
    "Microampere",
    "Microvolt",
    "Milliampere",
    "Milliohm",
    "Millivolt",
    "Milliwatt",
    "Ohm",
    "Power",
    "Resistance",
    "Temperature",
    "TemperatureDelta",
    "UnrepresentableDimensionError",
    "Volt",
    "Voltage",
    "Watt",
]
