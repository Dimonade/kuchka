"""Historical, regional, and culturally specific units of measurement.

This package collects units of measurement that fall outside the SI and the modern
units commonly exposed by `kuchka`.
It includes historical and obsolete units, regional measurement systems, and units
associated with particular peoples, cultures, trades, or traditions.

The term *archaic* is a practical namespace label, not a claim that every unit listed
here has disappeared from modern use.

Organization
------------
Units are grouped by their country, region, people, or another useful historical or
cultural context.
Individual modules define the relevant units, their conversion scales, alternative
spellings, and known variants.

These units are deliberately excluded from the global user-facing API.
Import them explicitly from the appropriate submodule under `kuchka.units.archaic`
when they are needed.

Interoperability
----------------
The unit families expose `*_UNITS` tables following the same interface as the tables
provided for the main unit families.
These tables can resolve supported unit symbols and names to their constructors at
application boundaries, such as when parsing configuration files or historical records.

Archaic unit constructors produce the ordinary `kuchka` quantity types.
They therefore interoperate with modern units of the same quantity:
values can be combined arithmetically and converted using `.to(UNIT)` in the usual way.
No separate quantity type is required merely because a unit is historical.

Historical accuracy and sources
-------------------------------
These definitions are maintained on a best-effort basis.
Research currently relies primarily on the relevant Wikipedia articles, preferably in
the language associated with the unit or measurement system.
These sources are a starting point for documenting the units, not a guarantee of
scholarly consensus (as far as I know).

Historical measures can vary by period, location, trade, land category, or
standardization.
Some definitions are disputed, approximate, or preserved in sources that disagree with
one another.
Where known, distinct calibrations are represented separately, and relevant assumptions
and uncertainties are documented alongside the units.

Conversion scales represent the particular historical definition adopted by this
implementation.
Exact arithmetic preserves that definition.
It does not imply that the underlying historical measurement was universal or
unambiguous.

Versioning
----------
The definitions in this namespace are provisional and may be corrected as research
improves.
Changes to historical interpretations, spellings, or conversion scales are not, by
themselves, considered breaking changes requiring a compatibility-version bump.
Such changes will still be documented in `CHANGELOG.md`.

This relaxed policy applies specifically to the historical data in this namespace.
It does not change the compatibility policy for the rest of `kuchka`.
"""