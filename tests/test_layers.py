"""The layer guard: imports point down only.

`layers.toml` lists the layers, lowest first. A file may import from its own layer or any lower
layer. An import that points UP fails this test, unless it is listed under `accepted` with a reason.

The guard is proven, not assumed: the control tests at the bottom build tiny projects with a
planted bug and check it is caught (see docs/PRINCIPLES.md, principle 3).

"Could not measure" is its own answer: with no layers mapped, the guard skips rather than passes,
and a source file in no layer fails rather than going unchecked.

To adapt to another language, replace `imports_of()` only (see docs/structure/README.md).
"""

import ast
import tomllib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def load_map(root: Path) -> dict:
    with open(root / "layers.toml", "rb") as f:
        return tomllib.load(f)


def imports_of(path: Path) -> list[str]:
    """Every module name this Python file imports, at any depth."""
    names = []
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Import):
            names += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            names.append(node.module)
    return names


def resolve(module: str, root: Path, source_roots: list[str]) -> Path | None:
    """The repo file a module name points at, or None for a third-party module."""
    parts = module.split(".")
    for src in source_roots:
        base = root / src
        for n in range(len(parts), 0, -1):
            stem = base.joinpath(*parts[:n])
            for candidate in (stem.with_suffix(".py"), stem / "__init__.py"):
                if candidate.exists():
                    return candidate
    return None


def layer_of(path: Path, root: Path, layers: list[dict]) -> int | None:
    """Index of the layer a file belongs to (longest matching path wins), or None if unmapped."""
    rel = path.relative_to(root).as_posix()
    best, best_len = None, -1
    for i, layer in enumerate(layers):
        for p in layer["paths"]:
            if (rel == p or rel.startswith(p.rstrip("/") + "/")) and len(p) > best_len:
                best, best_len = i, len(p)
    return best


def upward_imports(root: Path) -> set[tuple[str, str]]:
    """Every (file, imported file) pair where the import points to a higher layer."""
    cfg = load_map(root)
    layers = cfg.get("layer", [])
    source_roots = cfg.get("roots", ["src"])
    found = set()
    for src in source_roots:
        for path in (root / src).rglob("*.py"):
            mine = layer_of(path, root, layers)
            if mine is None:
                continue
            for module in imports_of(path):
                target = resolve(module, root, source_roots)
                if target is None:
                    continue
                theirs = layer_of(target, root, layers)
                if theirs is not None and theirs > mine:
                    found.add((path.relative_to(root).as_posix(),
                               target.relative_to(root).as_posix()))
    return found


def unmapped_files(root: Path) -> list[str]:
    """Every source file that is in no layer, so the guard cannot check it."""
    cfg = load_map(root)
    layers = cfg.get("layer", [])
    return sorted(path.relative_to(root).as_posix()
                  for src in cfg.get("roots", ["src"])
                  for path in (root / src).rglob("*.py")
                  if layer_of(path, root, layers) is None)


def require_layers(root: Path) -> None:
    """Skip, not pass, when there is no layer map to check against."""
    if not load_map(root).get("layer"):
        pytest.skip("could not measure: layers.toml maps no layers yet "
                    "(fill it in at the first grilling session)")


def accepted(root: Path) -> set[tuple[str, str]]:
    return {(a["file"], a["imports"]) for a in load_map(root).get("accepted", [])}


# --- the guard, on this repo -------------------------------------------------------------------

def test_imports_point_down_only():
    require_layers(ROOT)
    new = upward_imports(ROOT) - accepted(ROOT)
    assert not new, (f"upward imports: {sorted(new)}. Pass the dependency in, or move the shared "
                     "piece down a layer (docs/structure/README.md).")


def test_accepted_exceptions_only_shrink():
    stale = accepted(ROOT) - upward_imports(ROOT)
    assert not stale, f"fixed, so remove from `accepted` in layers.toml: {sorted(stale)}"


def test_every_mapped_path_exists():
    """A layer map that names a path that is not there checks nothing (principle 3)."""
    missing = [p for layer in load_map(ROOT).get("layer", []) for p in layer["paths"]
               if not (ROOT / p).exists()]
    assert not missing, f"layers.toml names paths that do not exist: {missing}"


def test_every_source_file_is_in_a_layer():
    require_layers(ROOT)
    unmapped = unmapped_files(ROOT)
    assert not unmapped, (f"not in any layer, so the guard cannot check them: {unmapped}. "
                          "Add each to a layer in layers.toml.")


# --- the controls: prove the guard can fail -----------------------------------------------------

def test_the_guard_catches_an_upward_import(tmp_path):
    (tmp_path / "layers.toml").write_text(
        'roots = ["src"]\n'
        '[[layer]]\nname = "low"\npaths = ["src/low"]\n'
        '[[layer]]\nname = "high"\npaths = ["src/high"]\n')
    for pkg in ("low", "high"):
        (tmp_path / "src" / pkg).mkdir(parents=True)
        (tmp_path / "src" / pkg / "__init__.py").write_text("")
    (tmp_path / "src" / "high" / "ui.py").write_text("from low import core\n")   # down: fine
    (tmp_path / "src" / "low" / "core.py").write_text("import high.ui\n")       # up: planted

    assert upward_imports(tmp_path) == {("src/low/core.py", "src/high/ui.py")}


def test_the_guard_names_a_file_in_no_layer(tmp_path):
    (tmp_path / "layers.toml").write_text('roots = ["src"]\n[[layer]]\nname = "low"\n'
                                          'paths = ["src/low"]\n')
    (tmp_path / "src" / "low").mkdir(parents=True)
    (tmp_path / "src" / "low" / "core.py").write_text("")
    (tmp_path / "src" / "stray.py").write_text("")                              # planted

    assert unmapped_files(tmp_path) == ["src/stray.py"]


def test_the_guard_skips_when_no_layers_are_mapped(tmp_path):
    (tmp_path / "layers.toml").write_text('roots = ["src"]\n')                  # planted: empty map

    with pytest.raises(pytest.skip.Exception, match="could not measure"):
        require_layers(tmp_path)
