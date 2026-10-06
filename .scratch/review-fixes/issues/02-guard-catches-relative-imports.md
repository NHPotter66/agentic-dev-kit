# 02: the layer guard catches relative imports

**Type:** build
**Status:** open
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
