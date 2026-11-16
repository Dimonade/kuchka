"""The generated overloads are current, and the generator edits only what it owns.

`tools/generate_overloads.py` writes the `*` and `/` overloads of every linear quantity
type from the registry.
The first test catches an overload list that fell out of step with the registry, and
the rest exercise the generator on small modules of its own.
"""

from __future__ import annotations

import importlib.util
import textwrap
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from types import ModuleType

    import pytest

GENERATOR_PATH = Path(__file__).resolve().parents[2] / "tools" / "generate_overloads.py"


def _load_generator() -> ModuleType:
    spec = importlib.util.spec_from_file_location("generate_overloads", GENERATOR_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


generator = _load_generator()

CLASS = textwrap.dedent(
    """\
    class Thing:
        value = 1

    {body}
    """
)


def _source(body: str) -> list[str]:
    return CLASS.format(
        body=textwrap.indent(textwrap.dedent(body), "    ")
    ).splitlines()


def test_every_overload_list_is_current() -> None:
    assert generator.generate() == {}, "run `just generate-overloads`"


def test_a_stale_region_is_replaced_and_the_rest_of_the_class_is_kept() -> None:
    lines = _source(
        """\
        # BEGIN GENERATED __mul__
        @overload
        def __mul__(self, other: Old) -> Old: ...
        # END GENERATED

        def other_method(self) -> None: ...
        """
    )
    new = generator.place(
        lines, "Thing", "__mul__", ["    @overload", "    def n(): ..."]
    )
    text = "\n".join(new)
    assert "Old" not in text
    assert "def n(): ..." in text
    assert "def other_method" in text


def test_hand_written_overloads_are_wrapped_in_a_region_on_first_run() -> None:
    lines = _source(
        """\
        @overload
        def __mul__(self, other: A) -> A: ...
        @overload
        def __mul__(self, other: B) -> B: ...
        @override
        def __mul__(self, other): return super().__mul__(other)
        """
    )
    new = generator.place(
        lines, "Thing", "__mul__", ["    @overload", "    def n(): ..."]
    )
    text = "\n".join(new)
    assert text.count("# BEGIN GENERATED __mul__") == 1
    assert "other: A" not in text
    assert "return super().__mul__(other)" in text


def test_a_missing_method_is_added_with_the_standard_implementation() -> None:
    new = generator.place(
        _source("def keep(self) -> None: ...\n"), "Thing", "__truediv__", ["    x"]
    )
    text = "\n".join(new)
    assert "# BEGIN GENERATED __truediv__" in text
    assert "return super().__truediv__(other)" in text
    assert "def keep" in text


def test_a_missing_power_is_added_with_its_own_parameter() -> None:
    new = generator.place(_source("value = 2\n"), "Thing", "__pow__", ["    x"])
    text = "\n".join(new)
    assert "def __pow__(self, exponent: int) -> LinearQuantity | Fraction:" in text
    assert "return super().__pow__(exponent)" in text


def test_literal_is_imported_when_a_module_names_it() -> None:
    text = textwrap.dedent(
        """\
        from __future__ import annotations

        from typing import TYPE_CHECKING

        if TYPE_CHECKING:
            from fractions import Fraction


        class Thing:
            def __pow__(self, exponent: Literal[2]) -> Fraction: ...
        """
    )
    fixed = generator.fix_imports(text, {})
    assert fixed.count("from typing import Literal") == 1
    assert generator.fix_imports(fixed, {}).count("from typing import Literal") == 1


def test_a_custom_implementation_after_the_region_is_left_alone() -> None:
    lines = _source(
        """\
        # BEGIN GENERATED __rtruediv__
        @overload
        def __rtruediv__(self, other: Old) -> Old: ...
        # END GENERATED

        def __rtruediv__(self, other):
            return custom(other)
        """
    )
    new = generator.place(
        lines, "Thing", "__rtruediv__", ["    @overload", "    def n(): ..."]
    )
    assert "return custom(other)" in "\n".join(new)


def test_the_quantity_imports_are_recomputed_from_the_names_a_module_uses() -> None:
    text = textwrap.dedent(
        """\
        from __future__ import annotations

        from typing import TYPE_CHECKING

        if TYPE_CHECKING:
            from fractions import Fraction
            from kuchka.quantities.length import Length
            from kuchka.quantities.mass import Mass


        class Thing:
            def a(self, other: Time) -> Fraction: ...
        """
    )
    homes = {"Length": "kuchka.quantities.length", "Time": "kuchka.quantities.temporal"}
    fixed = generator.fix_imports(text, homes)
    assert "import Time" in fixed
    assert "import Length" not in fixed
    assert "import Mass" not in fixed
    assert "from fractions import Fraction" in fixed


def test_a_wrapped_quantity_import_is_replaced_whole() -> None:
    text = textwrap.dedent(
        """\
        from __future__ import annotations

        from typing import TYPE_CHECKING

        if TYPE_CHECKING:
            from fractions import Fraction
            from kuchka.quantities.mass import (
                Mass,
            )


        class Thing:
            def a(self, other: Time) -> Fraction: ...
        """
    )
    fixed = generator.fix_imports(text, {"Time": "kuchka.quantities.temporal"})
    compile(fixed, "<fixed>", "exec")
    assert "Mass" not in fixed
    assert "import Time" in fixed


def test_a_runtime_import_is_not_repeated_under_type_checking() -> None:
    text = textwrap.dedent(
        """\
        from __future__ import annotations

        from typing import TYPE_CHECKING

        from kuchka.quantities.temporal import Time

        if TYPE_CHECKING:
            from fractions import Fraction


        class Thing:
            def a(self, other: Time) -> Fraction: ...
        """
    )
    fixed = generator.fix_imports(text, {"Time": "kuchka.quantities.temporal"})
    assert fixed.count("import Time") == 1


def test_check_mode_reports_a_stale_module_and_exits_nonzero(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    stale = {GENERATOR_PATH.parent.parent / "src" / "kuchka" / "x.py": "text\n"}
    monkeypatch.setattr(generator, "generate", lambda: stale)
    monkeypatch.setattr("sys.argv", ["generate_overloads", "--check"])
    assert generator.main() == 1
    assert "x.py is out of date" in capsys.readouterr().err
