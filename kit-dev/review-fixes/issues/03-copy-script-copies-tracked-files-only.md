# 03: the copy script copies only tracked files

**Type:** build
**Status:** open
**Blocked by:** none
**verified_by:** static

## Goal

`kit_files()` walks the folder on disk (`scripts/new_project.py:24-30`), so local junk such as
`.ruff_cache/` lands in the new project. Confirmed 2026-10-05: `.ruff_cache` appeared in a fresh
target. A skip list misses the next cache folder someone's tools create.

When this is done, the script copies what git tracks and nothing else. It says clearly what
happens when the kit is not a git checkout (for example, a ZIP download).

## Acceptance

- [ ] An untracked file in the kit (a planted `.junk_cache/x`) is not copied. This test failed
      before the fix.
- [ ] The behavior without `.git` matches the decision below, and a test covers it.
- [ ] Existing tests in `tests/test_new_project.py` still pass.

## Out of scope

- Changing the never-overwrite or README-to-METHOD.md behavior.

## Notes and progress

**Decided 2026-10-05 (human):** no `.git` → stop with a clear message telling the person to
`git clone` the kit. No fallback to walking the folder.

**Added 2026-10-05 (human):** the kit's own development records (its maps, tickets, and any
timeline or lessons about building the kit) must never be copied into a project. Only the
templates are. **Decided 2026-10-05 (human):** those records live in `kit-dev/`, which the
script never copies. Acceptance adds: a planted tracked file in `kit-dev/` is not copied.
