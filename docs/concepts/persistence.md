# Copying, pickling, and persistence

A quantity is an immutable value, and `copy`, `copy.deepcopy`, and `pickle` all work on it.
They are meant for moving values around inside one program or between processes that run the same version of `kuchka`: caches, `multiprocessing`, and the like.
To store a value in a file or a database, store the exact magnitude and the unit's symbol.

## Copying and pickling

A unit definition is an immutable value.
Two units with the same fields are equal and hash alike, and copying one returns the same object, so a copy keeps the library's own unit:

```python
import copy
import pickle

from kuchka import Volt
from kuchka.units import VOLT

copy.deepcopy(Volt(5)).unit is VOLT  # True
pickle.loads(pickle.dumps(Volt(5))).unit is VOLT  # True
```

A pickled quantity holds the name `kuchka.quantities` publishes its class under, its exact magnitude, and the name `kuchka.units` publishes its unit under, which are `Voltage` and `VOLT` here.
It holds neither the module that defines the class nor the fields behind the unit, so moving a class between modules or changing how a unit is built does not change what a pickle contains.
Unpickling accepts only names of published quantity types and published units.

A unit that `kuchka.units` does not publish copies normally and cannot be pickled, and raises `pickle.PicklingError` if pickling is attempted.

## Pickle is not a storage format

A pickle names quantity types and unit constants, so it stops loading when one of them is renamed or removed in a later version, and loading an untrusted pickle runs code.
It is a way to transport a value, and the file or database is better served by a form that does not depend on `kuchka`'s internals.

## Storing a value

Store two things: the magnitude in the display unit as exact text, and the unit's symbol.

```python
import json
from fractions import Fraction

from kuchka import Millivolt
from kuchka.units import VOLTAGE_UNITS

value = Millivolt(Fraction(7, 3))
stored = {"value": str(value.value_in(value.unit)), "unit": value.unit.symbol}
text = json.dumps(stored)  # '{"value": "7/3", "unit": "mV"}'

loaded = json.loads(text)
constructor = VOLTAGE_UNITS[loaded["unit"]]
restored = constructor(Fraction(loaded["value"]))
restored == value  # True
```

A `Fraction` written as text restores exactly, which a `float` does not.
The symbol is read through the quantity's `*_UNITS` table, which accepts the display symbol and the other spellings of a unit (see [Unit spellings](unit_spellings.md)), so a file written by hand with `uV` or `degrees C` restores as well as one written by this code.
The same two fields work for every quantity shape and every unit, including temperatures and levels.
