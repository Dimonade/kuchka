# Unit spellings

A unit read from a configuration file or a specification is rarely typed as the display symbol.
It arrives as `C`, `degC`, `degrees C`, `u` for the dalton, or `uV` for `µV`.
Each `*_UNITS` table accepts the notations people write, and refuses any that could mean more than one unit.

```python
from kuchka.units import MASS_UNITS
from kuchka.units import TEMPERATURE_UNITS
from kuchka.units import VOLTAGE_UNITS

celsius = TEMPERATURE_UNITS["degrees C"]
also_celsius = TEMPERATURE_UNITS["Degrees Celsius"]
dalton = MASS_UNITS["u"]
microvolt = VOLTAGE_UNITS["uV"]

celsius(21.5)  # 21.5 °C
also_celsius(21.5)  # the same
dalton(12)  # 12 Da
microvolt(3)  # 3 µV
```

## What a table accepts

Every unit is known by a display `symbol` and may carry more spellings, held on the unit definition itself:

| Field     | Compared      | For                  | Example (`°C`)                        |
| --------- | ------------- | -------------------- | ------------------------------------- |
| `symbol`  | exactly       | the display notation | `°C`                                  |
| `aliases` | exactly       | other symbols        | `C`, `° C`                            |
| `name`    | ignoring case | the unit's name      | `celsius`                             |
| `words`   | ignoring case | spoken forms         | `degrees C`, `degree Celsius`, `degC` |

Before anything is compared, text is normalized: characters that read the same become the same character, and runs of whitespace become one space.
The micro sign and the Greek mu are one character, so are the Ohm sign and the Greek omega, and `℃` becomes `°C`.
Leading and trailing whitespace is ignored.

A trailing plural `s` is accepted on a name or a word, so `volts`, `Degrees C`, and `inches` resolve.
It is never accepted on a symbol: `Vs` is not volts.

An SI prefix is known by its symbol and its keyboard alias, so micro is `µ`, `μ`, and `u`, and a prefixed unit accepts every pairing: `uV`, `µV`, `μV`.
A base unit's other symbols pair the same way, so `kohm`, `kOhm`, and `kΩ` are all kilohms.

## Squared and cubed units

A superscript and a plain digit are the same character after normalization, so `m²`, `m2`, and `mm²` and `mm2` all resolve.
The ASCII power forms `m^2` and `m**2` are aliases too, and so are `sq m` and `square meters`, for areas, volumes (`cm^3`, `cc`), and accelerations (`m/s^2`).

```python
from kuchka.units import AREA_UNITS
from kuchka.units import VOLUME_UNITS

area = AREA_UNITS["mm2"]
volume = VOLUME_UNITS["cm^3"]

area(12)  # 12 mm²
volume(5)  # 5 cm³
```

The table is for one quantity, so the exponent has to match: `m3` is refused by `AREA_UNITS`, and `m2` by `VOLUME_UNITS`.
The `m` and `M` of a millimetre and a megametre are told apart by case, as for any symbol: `MM2` and `Mm2` are refused.

## Case

Case is compared exactly for symbols and aliases, and ignored for names and words.
The reason is the SI itself: `mV` is a millivolt and `MV` a megavolt, `pV` a picovolt and `PV` a petavolt, `mA` and `MA` likewise.
A table that folded case on symbols would read a megavolt typed in lower case as a millivolt, silently, so it does not.
A spelling that carries no case information, a word such as `degrees celsius`, can be written in any case.

## What a table refuses

Anything that is not claimed by a unit in that table raises `KeyError`:

- a symbol in the wrong case (`mv`, `hz`, `KHz`);
- a symbol with a plural (`Vs`, `kgs`);
- a spoken form that is ambiguous within the table: `degrees` could be Celsius, Fahrenheit, or Kelvin, so `TEMPERATURE_UNITS` claims none of `deg`, `degree`, or `degrees` alone;
- a prefix on its own (`u`, `m`, `k` in `VOLTAGE_UNITS`);
- a unit of another quantity (`C` in `TIME_UNITS`, `volt` in `CURRENT_UNITS`);
- a quantity and not a unit (`5 mV`), because a table resolves a unit, and parsing a value is a separate step.

## Refused on purpose

Some spellings are common and still refused, because accepting them would mean choosing between two real meanings:

| Spelling         | Table               | Why                                                                          |
| ---------------- | ------------------- | ---------------------------------------------------------------------------- |
| `year`, `years`  | `TIME_UNITS`        | A civil, tropical, and Julian year differ; `yr` and `julian year` are exact. |
| `mwh`            | `ENERGY_UNITS`      | Milliwatt-hour or megawatt-hour; `mWh` is the former.                        |
| `calorie`        | `ENERGY_UNITS`      | A small or a large calorie; `cal` and `Cal` are exact.                       |
| `kt`, `Mt`, `t`  | `ENERGY_UNITS`      | Kilotonnes of what: the TNT equivalent has to be named, `kt TNT`.            |
| `deg`, `degrees` | `TEMPERATURE_UNITS` | Celsius, Fahrenheit, or Kelvin.                                              |
| `bhp`            | `POWER_UNITS`       | Brake horsepower is not the mechanical horsepower `hp`.                      |

A spelling that is refused today can be added to the unit definition when the meaning is settled, and it will be checked against every other spelling of the table.

## No spelling means two units

A table cannot be built while a spelling could mean two units.
Building it raises `ValueError` when:

- two units claim the same symbol, alias, name, or word, after normalizing;
- a symbol reads as another unit's word when case is ignored;
- a word is another unit's word with a plural `s` added.

So a table that exists has no ambiguity, and adding a spelling that collides fails when the library is imported.
The same spelling can mean different things in different tables, because a table is for one quantity: `C` is a coulomb in `CHARGE_UNITS` and degrees Celsius in `TEMPERATURE_UNITS`.

## Iterating a table

Iterating a table yields each unit's display symbol once, in definition order, and its length is the number of units.
Spellings other than the display symbol work for lookup and membership (`"C" in TEMPERATURE_UNITS`) and do not appear when iterating.

## Adding a spelling

A spelling is a field of the unit definition.
Add a symbol-like spelling to `aliases`, and a name or spoken form to `words`:

<!-- doc-test: skip a fragment of a unit definition, not a program -->

```python
CELSIUS = AffineUnitDef(
    "celsius",
    "°C",
    Decimal(1),
    Decimal("273.15"),
    aliases=("C",),
    words=("degC", "degrees C", "degree Celsius"),
)
```

Words are compared ignoring case, so one form of each is enough.
`prefixed_unit` takes `base_aliases` and `base_words` for a base unit that has prefixed forms.
The tests in `tests/test_unit_spellings.py` check every table for the properties above, so a new spelling that is ambiguous or loosens case fails them.
