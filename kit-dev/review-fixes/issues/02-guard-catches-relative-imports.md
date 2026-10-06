# 02: the layer guard catches relative imports

**Type:** build
**Status:** resolved (2026-10-05, relative imports resolved from the importing file)
**Blocked by:** 01 (same file)
**verified_by:** static

## Goal

`imports_of()` ignores any `ImportFrom` with `level > 0` (`tests/test_layers.py:30`). So
`from ..high import ui` in a lower layer passes. Confirmed 2026-10-05 by planting exactly that.

When this is done, relative imports are resolved against the importing file's package and checked
like absolute ones.

## Acceptance

- [ ] A control test plants `from ..high import ui` in a low layer, and the guard reports it.
- [ ] `from . import sibling` and `from .mod import name` in the same layer are not reported.
- [ ] The new control was shown to fail before the fix (that is, it caught the bug), then passed after.
- [ ] `pytest` passes on the kit itself.

## Out of scope

- Dynamic imports (`importlib.import_module("...")`). A static guard cannot see them. Note this
  limit in `docs/structure/README.md`.

## Notes and progress
**2026-10-05, built.** `imports_of()` keeps the leading dots, and `resolve()` starts a dotted name
from the importing file's folder. The first attempt failed its own control: `from ..high import ui`
resolved to `high/__init__.py`, not `ui.py`. Fixed by resolving `module.name` for each imported
name, which also sharpens absolute `from a import b`. Planted the old "skip relative imports" line
from a backup → control failed (`set() == {...}`). Restored (identical to backup). Suite: 9 passed,
2 skipped. Dynamic-import limit noted in `docs/structure/README.md`.
