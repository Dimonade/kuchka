"""The code in the documentation runs, and says what it does.

Every Python block of the README and of `docs/concepts` is run, so an example cannot
drift from the library: a renamed method, a changed result, or a comparison documented
as true that is not, fails here.
Blocks that cannot run as written carry a `<!-- doc-test: skip ... -->` marker with the
reason.
The worked examples under `docs/examples` have tests of their own, and the design
proposal describes the library as it was.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.docs import runner

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
EXCLUDED = ("examples", "design_proposal.md")


def is_checked(path: Path) -> bool:
    """Return whether `path` is a document that is run, and not a worked example."""
    relative = path.relative_to(DOCS)
    return relative.parts[0] != EXCLUDED[0] and path.name != EXCLUDED[1]


DOCUMENTS = [ROOT / "README.md", *filter(is_checked, sorted(DOCS.rglob("*.md")))]
IDS = [str(path.relative_to(ROOT)) for path in DOCUMENTS]


@pytest.mark.parametrize("document", DOCUMENTS, ids=IDS)
def test_the_code_in_a_document_runs_and_says_what_it_does(document: Path) -> None:
    failures = runner.run(document)
    assert not failures, "\n".join(failures)
