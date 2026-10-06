# 04: README, command names and an MIT license

**Type:** build
**Status:** resolved (2026-10-05, README, command name and MIT license; LICENSE copies to docs/KIT-LICENSE)
**Blocked by:** 03 (the README describes the script's new behavior)
**verified_by:** static

## Goal

The docs describe the kit as it is now, and the kit carries an MIT license (decided 2026-10-05,
human), without that license becoming the license of every project made from it.

## Acceptance

- [ ] README "What is in the box" lists `scripts/new_project.py`, `kit-dev/` and `LICENSE`.
- [ ] README "Starting a new project" says to `git clone` the kit, then run the script, and states
      Python 3.11+ (`tomllib`).
- [ ] The docs name the two-axis review as `/mattpocock-skills:code-review`, because a bare
      `/code-review` runs Claude Code's built-in review. (`/grill-me` was checked and is correct:
      the plugin ships it as a user-only skill.)
- [ ] `LICENSE` is MIT. The copy script puts it at `docs/KIT-LICENSE` in a project, never at the
      project's root. A test covers this, and was shown to fail without the rename.
- [ ] Every relative link in README.md and the docs still resolves.

## Out of scope

- `CLAUDE.md` pointing at `kit-dev/` (decided 2026-10-05: leave it until it is missed).

## Notes and progress
**2026-10-05, built.** README covers cloning, the script, Python 3.11+, and what stays in the kit.
The PLAYBOOK and WORKING_WITH_CLAUDE docs name `/mattpocock-skills:code-review`. MIT `LICENSE` is
added, with copyright "npotter66" taken from git config. Planted LICENSE-to-root from a backup →
test failed (`assert False` on KIT-LICENSE). Restored (identical to backup). Suite: 11 passed, 2
skipped. All 15 relative links in tracked markdown resolve.
