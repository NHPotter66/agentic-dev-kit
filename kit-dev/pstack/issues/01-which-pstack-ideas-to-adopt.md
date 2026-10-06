# 01: which pstack ideas to adopt

**Type:** decision
**Status:** open
**Blocked by:** none
**verified_by:** static

## Question

pstack (https://github.com/cursor/plugins/tree/main/pstack, read at commit `df58112`, v0.15.15,
MIT, Lauren Tan) is a Cursor plugin of ~50 skills built around one router, `/poteto-mode`. The
human does not want to pull it in whole. Which of its ideas, if any, should the kit adopt, in the
kit's own words, and where should each one go?

## What we found (2026-10-05)

Read in full: the README, guide index and setup page, `poteto-mode` core rules, and `correct`,
`encode-lessons-in-structure`, `prove-it-works`, `never-block-on-the-human`,
`test-behavior-not-implementation`, `show-me-your-work` and `create-verification-skill`. The rest
from their descriptions only.

- **Runs in Claude Code?** Inferred, not tried: the `SKILL.md` text ports, but the plumbing is
  Cursor's (`/add-plugin`, `~/.cursor/rules`, Grok/Opus model routing, a `cursor-team-kit`
  dependency). 16 skill folders reference something Cursor-specific.
- **Agrees with the kit:** P2 ↔ `prove-it-works`; P3 ↔ `test-behavior-not-implementation` and
  `correct`'s "prove each check fails"; P5 ↔ `fix-root-causes`; P8 ↔ `laziness-protocol`;
  PLAYBOOK §8 ↔ `encode-lessons-in-structure`; claim labels ↔ "every claim carries its evidence".
- **Disagrees with the kit:** `never-block-on-the-human` and its autonomy rules (act, then show)
  versus "offer options, the human chooses"; multi-model fan-out by default versus one session;
  playbooks that open, babysit and merge PRs versus "agents never push".

## Candidates, with recommendations to grill on

1. **The "return nothing" test check.** Would this test still pass if every function it calls
   returned nothing? If so, it cannot catch a bug. *Recommend: adopt, one paragraph in
   PRINCIPLES.md P3, next to plant-the-bug.*
2. **The `correct` ladder and rule table.** Fix a repeated mistake at the strongest level that
   works: architecture, types, a lint whose error names the fix, a test, docs last. Pair each rule
   in `CLAUDE.md` with what enforces it. *Recommend: adopt the ladder in PLAYBOOK §8, and add an
   "enforced by" column to the house rules.*
3. **`create-verification-skill`.** A recipe for a project-local skill that drives the real app
   (launch, doctor, drive, evidence, cleanup), which is what `staged` and `real` need. *Recommend:
   adopt as a short guide in docs for filling in the proof levels; decide separately whether to
   ship a Claude Code skill.*
4. **`show-me-your-work` decision log** and **`explain-the-number`.** *Recommend: not yet. Record in
   "Not adopted" and revisit when the kit meets unattended runs or perf work.*
5. **Skip:** the `/poteto-mode` router, model routing, PR babysit/shipping playbooks, and
   `never-block-on-the-human`, which conflicts with how the kit works. *Recommend: record each as
   declined, with its reason (Principle 9).*

## Acceptance

- [ ] Each candidate has a recorded answer: adopt (with where), not yet, or declined, each with
      its reason.
- [ ] Each "adopt" becomes its own build ticket in `kit-dev/pstack/issues/`.
- [ ] Any text copied rather than reworded keeps pstack's MIT notice.

## Out of scope

- Installing or running pstack.
- Writing the adopted changes (those are the build tickets).

## Notes and progress
