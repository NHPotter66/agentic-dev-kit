# Kit timeline

The kit's own history, one short entry per phase. Same format as the project template in
`docs/TIMELINE.md`, which stays blank for projects.

## Phase 1: review fixes (2026-10-05)
**Done:** The layer guard skips with "could not measure" on an empty map, names unmapped files and
catches relative imports. The copy script copies only git-tracked files, never `kit-dev/`, and stops
for a ZIP copy. MIT license, kept out of projects' roots. Kit records moved to `kit-dev/`.
**Learned:** Planting the bug caught a flaw in the relative-import fix itself (it resolved to the
package, not the module). A file that is both template and live record (`CLAUDE.md`, `docs/TIMELINE.md`)
can't hold the kit's own notes.
**Next:** Assess how poteto's `pstack` might fold into the kit.
