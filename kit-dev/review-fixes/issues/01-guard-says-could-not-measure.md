# 01: the layer guard says "could not measure" instead of "clean"

**Type:** build
**Status:** open
**Blocked by:** none
**verified_by:** static

## Goal

Today `upward_imports()` skips any file that is not in a layer (`tests/test_layers.py:67-69`). With
no layers mapped, which is how the kit ships, the guard checks nothing and passes. That is the
false "clean" that Principle 3 warns about. Confirmed 2026-10-05: an upward import with no layers
mapped returned `set()`.

When this is done:

- with no layers mapped, the guard reports that it could not measure, which is not a pass;
- a `.py` file under a source root that is in no layer is reported by name, never silently skipped.

## Acceptance

- [ ] With an empty `[[layer]]` list, `test_imports_point_down_only` does not pass. It reports
      that no layers are mapped (exact outcome per the decision below).
- [ ] A control test plants an unmapped file and shows the guard names it.
- [ ] Each new check was shown to fail on its planted bug, then the code was restored from a backup.
- [ ] `pytest` passes on the kit itself.

## Out of scope

- Relative imports (ticket 02).

## Notes and progress

**Decided 2026-10-05 (human):** no layers mapped → the guard tests *skip* with "could not
measure". A file in a source root that is in no layer → *fail*, naming the file.

**2026-10-05, built, awaiting review.** Planted both bugs from a backup: unmapped files skipped
again → `test_the_guard_names_a_file_in_no_layer` failed (`[] == ['src/stray.py']`); empty map not
skipped → `test_the_guard_skips_when_no_layers_are_mapped` failed (`DID NOT RAISE Skipped`).
Restored (identical to backup). Suite: 8 passed, 2 skipped with "could not measure".
