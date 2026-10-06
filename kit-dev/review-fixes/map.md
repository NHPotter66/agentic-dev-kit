# Map: review fixes

**Charted:** 2026-10-05

## Destination

The layer guard never reports "clean" when it checked nothing, it catches relative imports, and
the copy script copies only what the kit tracks. The README describes the kit as it is.

This map decides; it does not build. It is finished when nothing is left to decide before building
starts.

## Notes

- **Terms:** "could not measure" (CLAUDE.md house rules) is a third outcome, not a pass.
- **Constraints:** the repo is now public, so people may download it as a ZIP with no `.git`.

## The route

### Phase A: fix what the review found

**Ends when:** all three build tickets are resolved and `pytest` passes.
**Decide first:** the open questions in each ticket (asked in one grilling round, 2026-10-05).
**Then build:** 01, 02, 03, in that order. 01 and 02 touch the same file.
**Unknowns:** none beyond the ticket questions.

### Phase B: small doc fixes

**Ends when:** the README's "What is in the box" and "Starting a new project" mention the copy
script, the Python version (3.11+, for `tomllib`) is stated, and the command names in
`docs/WORKING_WITH_CLAUDE.md` match the installed plugin. Add an MIT `LICENSE` (decided
2026-10-05).
**Then build:** one docs ticket, written after Phase A.

## Not on this map

- Assessing how poteto's `pstack` repo might fold into the kit. The human asked for it next, as its
  own effort, after these tickets.
