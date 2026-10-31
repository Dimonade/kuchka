"""Unit constructors for geometric measures derived from length.

The module groups two geometric quantity families:

- `Area` (L²) measures the extent of a two-dimensional surface.
- `Volume` (L³) measures the space occupied or enclosed by a three-dimensional region.

Both are derived entirely from length.
Multiplying two lengths produces an area.
Multiplying an area by another length produces a volume.

Examples
--------
Land surveying and agricultural planning commonly express large areas in hectares.
A rectangular solar installation occupying 200 metres by 150 metres has a footprint of
30,000 square metres, equivalent to three hectares:

>>> from kuchka import Metre
>>> from kuchka import Hectare
>>> field = Metre(200) * Metre(150)
>>> field
30000 m²
>>> field.to(HECTARE)
3 ha

The same relationship between area and length is useful in hydrology.
A rainfall depth of 20 millimetres over one hectare deposits 200 cubic metres of water,
assuming the rainfall is uniform across the entire area:

>>> from kuchka import Hectare, Millimetre, Litre
>>> rainfall_volume = Hectare(1) * Millimetre(20)
>>> rainfall_volume
200 m³
>>> rainfall_volume.to(LITRE)
200000 L

Volume units also reflect different measurement traditions.
Laboratory work commonly uses millilitres, while geometric calculations and material
pecifications often use cubic centimetres.
The two scales are numerically identical:

>>> from kuchka import Millilitre
>>> from kuchka.units import CUBIC_CENTIMETRE
>>> sample = Millilitre(250)
>>> sample.to(CUBIC_CENTIMETRE)
250 cm³

Notes
-----
The canonical SI units are:

    Area:   square metre (m²)
    Volume: cubic metre (m³)

Area units include square metric units, square inches, acres, and hectares.
Volume units include cubic metric units and litre-based units, from microlitres to
kilolitres.

Some volume units have numerically identical scales but arise from different
measurement traditions:

    1 mL = 1 cm³
    1 L  = 1000 cm³
    1 kL = 1 m³

Likewise, large-area units provide convenient representations of the same underlying
measure:

    1 ha = 10,000 m²
    1 km² = 100 ha

The relationship between area and volume is especially useful in engineering,
construction, agriculture, and environmental science:

    volume = area * depth
    area = volume / depth

For example, excavation quantities can be calculated from a site footprint and
excavation depth, while water collection estimates can be derived from rainfall depth
and catchment area.

American and British spellings are provided where applicable, including
`SquareMeter` / `SquareMetre`, `CubicMeter` / `CubicMetre`, and
`Liter` / `Litre`.

`AREA_UNITS` and `VOLUME_UNITS` map unit symbols to their constructors for
applications that resolve units dynamically from external input.

See Also
--------
~kuchka.quantities.Area
Quantity type representing a two-dimensional measure.

~kuchka.quantities.Volume
Quantity type representing a three-dimensional measure.

~kuchka.quantities.Length
Quantity type representing linear distance and the basis of area and volume.

"""

from __future__ import annotations

from kuchka.units.geometry import area
from kuchka.units.geometry import volume
from kuchka.units.geometry.area import *
from kuchka.units.geometry.volume import *

__all__: list[str] = []
__all__ += area.__all__
__all__ += volume.__all__
