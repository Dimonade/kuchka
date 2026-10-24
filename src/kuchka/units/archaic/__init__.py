"""Historical, regional, and culturally specific units of measurement.

This package collects units of measurement beyond the SI and the modern units that
`kuchka` exposes at its top level.
It holds historical and obsolete units, regional measurement systems, and units tied to
particular peoples, cultures, trades, or traditions.
*Archaic* is a practical namespace label, and a unit listed here may well remain in
use somewhere.

Importing
---------
Each unit is imported explicitly from the module of its tradition and quantity:

    from kuchka.units.archaic.russian.length import Arshin
    from kuchka.units.archaic.japanese.mass import Kan

The top-level `kuchka` namespace, `kuchka.units`, and the generated API list none of
these names.
A quantity type displays in a historical unit once the module defining it is imported,
because the module adds its units to the quantity type when it loads.
`Length(1, ARSHIN)` and `.to(ARSHIN)` therefore work after the Russian length module is
imported, and an application that imports no archaic module sees no archaic unit.

Organization
------------
Units are grouped by country, region, people, or another historical or cultural
context, with one module per quantity inside each group:

- `german`: the Meilen, with the principal miles in `german.length.meile` and the
  regional ones in `german.length.regional_meilen`,
- `hebrew`: Biblical and Talmudic lengths in three calibrations,
- `japanese`: the shakkan-hō units of length, area, volume, and mass,
- `russian`: the imperial-era units of length and land area.

Interoperability
----------------
Every module exposes a `*_UNITS` table with the interface of the tables of the main
unit families.
A table resolves unit symbols, names, and other spellings to constructors at an
application boundary, such as a configuration file or a transcribed historical record.

Archaic constructors build the ordinary `kuchka` quantity types, so values combine
arithmetically with modern units of the same quantity and convert with `.to(UNIT)`.
A historical unit needs no quantity type of its own.
Archaic units are unpublished units, so a value displayed in one copies freely and
pickles after conversion to a published unit.

Adding a unit
-------------
The pages under `docs/how-to` describe adding a unit, a quantity, a dimension, and a
new tradition, and the tests and documentation each needs.

Historical accuracy and sources
-------------------------------
The definitions are maintained on a best-effort basis from the relevant Wikipedia
articles, preferably in the language of the unit or measurement system.
These sources are a starting point for documenting the units, and scholarly
consensus can differ from them.

Historical measures varied by period, place, trade, land category, and standardization.
Some definitions are disputed or approximate, and the sources for some disagree.
Distinct calibrations are separate units where they are known, and each module
documents its assumptions and uncertainties beside the units.

A conversion scale is the particular historical definition this implementation adopts,
and exact arithmetic keeps that definition without rounding.

Versioning
----------
The definitions in this namespace are provisional and change as research improves.
A correction to a historical interpretation, a spelling, or a conversion scale is a
documented change in the changelog and leaves the compatibility version alone.
The compatibility policy of the rest of `kuchka` applies to everything outside this
namespace.
"""
