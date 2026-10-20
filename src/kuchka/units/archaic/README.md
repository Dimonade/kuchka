# Archaic units

Historical, regional, and culturally specific units of measurement.
_Archaic_ is a practical label for the namespace, and a unit listed here may well remain in use somewhere.

## Importing

Each unit is imported explicitly from the module of its tradition and quantity:

```python
from kuchka.units.archaic.japanese.mass import Kan
from kuchka.units.archaic.russian.length import Arshin
```

The top-level `kuchka` namespace, `kuchka.units`, and the generated API list none of these names.
A quantity type displays in an archaic unit once the module that defines it is imported, so `Length(1, ARSHIN)` and `.to(ARSHIN)` work after the Russian length module is imported, and a program that imports no archaic module sees no archaic unit.

Archaic constructors build the ordinary quantity types, so values combine with modern units and convert with `.to(UNIT)`.
Each module exposes a `*_UNITS` table that resolves symbols, names, and other spellings to constructors at a boundary such as a configuration file or a transcribed record.
Archaic units are unpublished units: a value displayed in one copies freely, and it pickles after conversion to a published unit.

## What is here

| Tradition  | Module                                      | Units                                                           |
| ---------- | ------------------------------------------- | --------------------------------------------------------------- |
| `german`   | `german.length.meile`                       | the four principal miles: geographic, Prussian, Reich, Austrian |
| `german`   | `german.length.regional_meilen`             | the regional miles, and a table joining all 27                  |
| `hebrew`   | `hebrew.length`                             | Biblical and Talmudic lengths in three calibrations             |
| `japanese` | `japanese.length`, `area`, `volume`, `mass` | the shakkan-hō units                                            |
| `russian`  | `russian.length`, `russian.area`            | imperial-era lengths and land areas                             |

## Historical accuracy

Definitions are maintained on a best-effort basis from the relevant Wikipedia articles, preferably in the language of the unit or measurement system.
Scholarly consensus can differ from these sources, and historical measures varied by period, place, trade, and standardization.
Distinct calibrations are separate units where they are known, and each module documents its assumptions and uncertainties beside the units.
A conversion scale is the one historical definition the module adopts, held as an exact fraction.

## Adding units

[How to extend kuchka](../../../../docs/how-to/README.md) describes the steps, and [Adding archaic units](../../../../docs/how-to/adding_archaic_units.md) covers a new tradition from the first file to the tests.
