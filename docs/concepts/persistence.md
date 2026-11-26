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

Store the written form of the value, `wire.dump(value)`, and read it back with `wire.load(text, Quantity)`:

```python
import json
from fractions import Fraction

from kuchka import Millivolt
from kuchka import Voltage
from kuchka import wire

value = Millivolt(Fraction(7, 3))
text = json.dumps({"supply": wire.dump(value)})  # '{"supply": "7/3 mV"}'

restored = wire.load(json.loads(text)["supply"], Voltage)
restored == value  # True
```

A fraction written as text restores exactly, which a `float` does not.
The unit is read through the quantity's `*_UNITS` table, which accepts the display symbol and the other spellings of a unit (see [Unit spellings](unit_spellings.md)), so a file written by hand with `uV` or `degrees C` restores as well as one written by this code.
The same form works for every quantity shape and every unit, including temperatures and levels, and [The wire form](wire_form.md) describes it.
Where a column or a document wants the number and the unit as two fields, `wire.to_dict(value)` writes `{"value": "7/3", "unit": "mV"}` and `wire.from_dict(data, Voltage)` reads it back exactly.
