"""How the text of a unit is compared: normalization and folding.

A unit arrives from outside the program as text, in a configuration file or a
specification, typed by someone using whatever notation they know.
Two steps make comparing it with the library's own spellings forgiving without
making it ambiguous:

- `normalize` puts text into one canonical form, so that characters that are the same
  to a reader are the same to the library: the micro sign and the Greek mu, the
  Ohm sign and the Greek capital omega, the `℃` ligature and `°C`, and runs of
  whitespace.
- `fold` additionally ignores letter case, and is applied only to words (unit names
  and phrases such as `degrees Celsius`), never to symbols, because case carries
  meaning in a symbol: `mV` is a millivolt and `MV` a megavolt.
"""

from __future__ import annotations

import unicodedata


def normalize(text: str) -> str:
    """Return `text` in canonical form: NFKC, with whitespace collapsed to one space."""
    return " ".join(unicodedata.normalize("NFKC", text).split())


def fold(text: str) -> str:
    """Return `text` normalized and case-folded, with underscores read as spaces."""
    return normalize(text.replace("_", " ")).casefold()


__all__ = ["fold", "normalize"]
