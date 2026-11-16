"""Statically valid code a consumer writes; every line must pass without a comment."""

from typing import assert_type

from kuchka import Celsius
from kuchka import Current
from kuchka import Ohm
from kuchka import Power
from kuchka import Resistance
from kuchka import Temperature
from kuchka import TemperatureDelta
from kuchka import Volt
from kuchka import Voltage

voltage: Voltage = Volt(12)
resistance: Resistance = Ohm(6)

assert_type(voltage / resistance, Current)
assert_type(voltage * (voltage / resistance), Power)

temperature: Temperature = Celsius(20)
assert_type(Celsius(25) - temperature, TemperatureDelta)
