# 2022 CODATA Fundamental Physical Constants -- Complete Listing

Taken from https://physics.nist.gov/cuu/Constants/Table/allascii.txt by:

```sh
curl https://physics.nist.gov/cuu/Constants/Table/allascii.txt -o src/kuchka/constants/codata_2022/allascii.txt
```

## Purpose

`kuchka` can expose a number of constants as pre-made `kuchka` objects and remove the need to manually build them.

## Example

```python
from kuchka import Hertz
from kuchka.constants import SPEED_OF_LIGHT_IN_VACUUM

wifi_wavelength = SPEED_OF_LIGHT_IN_VACUUM / Hertz(2_400_000_000)
```

To get a fully typed `kuchka` object back.

## Notes

### Exactness and approximation

Some constants are exact, others are an approximation.
`kuchka` currently does not have a "Kuchka Constant" object which carries this information _(should it?)_.
Currently, the exactness or approximation value is specified in a docstring of each constant.

### Not everything is implemented

There are a few hundred different constants in the definition.
Not all of them are implemented in `kuchka`.
Some of them are very specific to certain domains, others require dimensions that are neither currently implemented nor planned to be anytime soon.

If you feel that a specific constant is urgently needed, feel free to raise an Issue or PR it for review.
