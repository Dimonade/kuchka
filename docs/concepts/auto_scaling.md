# Readable units: `auto_scale` and `clock_parts`

Arithmetic in `kuchka` is exact, and a measurement displays in the unit it was given.
Two methods choose a unit that a person reads easily: `auto_scale()` picks a prefix, and `Time.clock_parts()` splits a duration into days, hours, minutes, and seconds.
Neither runs by itself, so `str(q)` and `f"{q}"` keep showing the unit the measurement was given.

## `auto_scale`

`auto_scale()` returns the same measurement in the unit of its ladder that suits its size.

```python
from kuchka import Ampere
from kuchka import Hertz

str(Ampere(0.000045).auto_scale()) == "45 µA"  # True
str(Hertz(2_400_000_000).auto_scale()) == "2.4 GHz"  # True
```

The value is the same exact value and only the display unit changes, so the result equals the measurement it came from and has its type.
The result is a quantity like any other, so format specifications apply to it.

```python
Ampere(0.000045).auto_scale() == Ampere(0.000045)  # True
type(Hertz(2_400_000_000).auto_scale()) is type(Hertz(1))  # True
f"{Hertz(2_400_000_000).auto_scale():.1f}" == "2.4 GHz"  # True
```

### The rule

A ladder is the run of prefixed units of one family, smallest first, such as the nanoampere to the megaampere.
A measurement moves along the ladder of the unit it displays in, and the rule has four parts:

- the unit is the largest one of the ladder in which the size of the value is at least 1,
- when the value is under 1 in every unit of the ladder, the smallest unit is used, and when it is over 1 in all of them, the largest,
- the sign is left out of the size, so `-25 mV` and `25 mV` are picked alike,
- zero keeps the unit it has, since it has no size to read.

```python
from kuchka import Milliampere
from kuchka import Volt

str(Milliampere(1000).auto_scale()) == "1 A"  # True
str(Ampere(1e-15).auto_scale()) == "0.001 pA"  # True
str(Volt(-0.025).auto_scale()) == "-25 mV"  # True
str(Milliampere(0).auto_scale()) == "0 mA"  # True
```

A measurement that is already in the chosen unit comes back as the same object.
Scaling a second time changes nothing.

### Ladders

A family of prefixed units is a ladder when its prefixes step by a thousand, as the nano, micro, milli, kilo, mega, and giga prefixes do, or by 1024, as the IEC binary prefixes of data do.
A unit stands on one ladder of a quantity, and a quantity has one ladder for each family.
`Energy` has four, for the joule, the electronvolt, the watt-hour, and the tonne of TNT, and `Data` has four, for the bit and the byte in decimal and in binary.

```python
from kuchka import Byte
from kuchka import Joule
from kuchka import Kibibyte
from kuchka import WattHour

str(Byte(5000).auto_scale()) == "5 kB"  # True
str(Kibibyte(5000).auto_scale()) == "4.8828125 MiB"  # True
str(Joule(3_600_000).auto_scale()) == "3.6 MJ"  # True
str(WattHour(0.002).auto_scale()) == "2 mWh"  # True
```

A measurement stays on its own ladder: a kibibyte is scaled in the binary units, and a kilobyte in the decimal ones.
A ladder ends at its smallest unit, so `Kibibyte(0.5)` stays at `0.5 KiB`, and no ladder reaches across to another family: `Gram(1.5e6)` is `1.5 Mg`, and a parsec never becomes a length in metres.

Each ladder is declared next to the units of its quantity, as `*_LADDERS`:

```python
from kuchka.units import CURRENT_LADDERS

[unit.symbol for unit in CURRENT_LADDERS[0]] == [
    "pA",
    "nA",
    "µA",
    "mA",
    "A",
    "kA",
    "MA",
]  # True
```

A role of a quantity moves along the ladders of that quantity: `Impedance` and `Reactance` along those of `Resistance`, `Stress` along those of `Pressure`, and `SamplingPeriod` along those of `Time`.

### Units on no ladder

A unit that is on no ladder keeps its measurement.
The centimetre and the hectopascal step by a hundred, so they are on none, and neither are the inch, the minute, or the calorie.

```python
from kuchka import Centimetre
from kuchka import Minute

length = Centimetre(2)
length.auto_scale() is length  # True
duration = Minute(90)
duration.auto_scale() is duration  # True
```

A temperature on the kelvin scale has a ladder, from the microkelvin to the kelvin, because its zero is the absence of temperature.
A reading in degrees Celsius, Fahrenheit, or Rankine has none.
The size of such a reading says where it is on a scale, and `0.5 °C` is a mild day and not a small temperature, so it is never rewritten in millidegrees.
A temperature difference has no zero point, so it has a ladder on both the kelvin and the Celsius scales.

```python
from kuchka import Celsius
from kuchka import DeltaCelsius
from kuchka import Kelvin

reading = Celsius(0.5)
reading.auto_scale() is reading  # True
str(Kelvin(0.005).auto_scale()) == "5 mK"  # True
str(DeltaCelsius(0.002).auto_scale()) == "2 Δm°C"  # True
```

Modular and logarithmic quantities, the angle and the decibel, have no ladders either, because their magnitude is not a size.

### Quantities without a ladder

A quantity has no ladder when its units have no family of prefixes in steps of a thousand.
Some are not prefixed that way at all: the angular quantities, `Velocity`, `Momentum`, `Proportion`, `HeatingRate`, `MolarVolume`, `EntitiesPerAmount`, `FirstMomentOfMass`, `LuminousEfficacy`, `LuminousEnergy`, and `LuminousIntensity`.
Others have prefixes that step by a million or more, because the prefix applies to a square or a cube: `Area`, `KinematicViscosity`, `VelocitySquared`, `TimeSquared`, `TimeCubed`, and `TimeFourthPower`.
`Instant` is a point in time, whose unit starts away from zero.
Calling `auto_scale()` on any of them is allowed and returns the measurement as it is.

The reason for each is written down in the coverage test of the ladders, and the test fails for a quantity that has neither ladders nor a reason, and for a family of prefixed units that is on no ladder.
A quantity added to the library therefore starts with a decision about its ladders.

### Rounding

The unit is chosen from the exact value, and the digits are rounded afterwards, when the value is shown.
A value just under a step can therefore round up to the step of the unit below it:

```python
str(Milliampere(0.9999999).auto_scale()) == "999.9999 µA"  # True
f"{Milliampere(0.9999999).auto_scale():.1f}" == "1000.0 µA"  # True
```

The value is never changed, so what is shown is the exact value with fewer digits, and reading it as `1000.0 µA` is correct.

## `Time.clock_parts`

`clock_parts()` splits a duration into whole days, hours, minutes, seconds, milliseconds, microseconds, nanoseconds, picoseconds, and femtoseconds, the largest first.

```python
from kuchka import Millisecond
from kuchka import Picosecond
from kuchka import Second

parts = Millisecond(5_025_500).clock_parts()
" ".join(map(str, parts)) == "1 h 23 min 45 s 500 ms"  # True
" ".join(map(str, Second(100_000).clock_parts())) == "1 d 3 h 46 min 40 s"  # True
```

The split follows five rules:

- each unit but the femtosecond takes the whole counts that fit in what is left, and the femtosecond takes the exact remainder, so only the last part can hold a fraction,
- a unit with a count of zero is left out,
- every part has the sign of the duration,
- the parts add up to the duration exactly,
- a zero duration is returned as it is.

```python
duration = Picosecond(10**12 + 1)
duration.clock_parts() == (Second(1), Picosecond(1))  # True
sum(duration.clock_parts(), start=Second(0)) == duration  # True
Second(-90).clock_parts() == (Minute(-1), Second(-30))  # True
```

A day is exactly 86 400 seconds in `kuchka`, because it has no calendar, no time zone, and no daylight saving time.
The split therefore runs through days and stops there: a week is seven days, a Julian year is 365 days and 6 hours, and a span of 400 days is `400 d`.

```python
from kuchka import Day
from kuchka import Hour
from kuchka import JulianYear

Hour(25).clock_parts() == (Day(1), Hour(1))  # True
JulianYear(1).clock_parts() == (Day(365), Hour(6))  # True
```

## Why they are methods

`str(q)` and `f"{q}"` show the unit a measurement was given, so a log line, a test report, and a stored value never change their unit on their own.
A program that wants a readable display asks for it, at the point where a person reads the value, and the measurement it gets back is the same exact value in a unit that reads better.
