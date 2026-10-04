# Playbook: how work moves through this project

This is the method, step by step, with the reason for each step. If a step feels like overhead,
read its "why". If the reason does not apply to your project, drop the step and say so in
`docs/LESSONS.md`.

---

## 1. Grill before you build

**What.** Before anything non-trivial, the agent interviews you. It asks every question it can ask
right now, numbered, each with its recommended answer. You answer. Your answers open up the next
round of questions. It ends when nothing is left to decide.

**The agent finds facts and you make decisions.** "What does the config file say?" is the agent's
job. "Should we support two config formats?" is yours.

**Why.** Most bad outcomes in the previous project were not bad code. They were decisions nobody
made on purpose: a default that was never questioned, or a scope that grew in a conversation. A
grilling session puts every decision in front of a human once, with a recommendation, and costs
minutes.

**How.** With the mattpocock skills installed, run `/grill-me` (or ask "grill me on this").

## 2. Draw a map

**What.** A short document in `.scratch/<effort>/map.md` (template in
`.scratch/TEMPLATE-map.md`). It holds:

- the destination;
- the route in phases;
- what is still unknown at each phase;
- which decision tickets must be answered before building starts.

**A map decides. It does not build.** It is done when nothing is left to decide, not when the
work is done.

**Why.** Without a map, each session picks the most interesting next thing. With one, anyone (a
coworker, or a fresh agent session with no memory) can see where the work is going and why that
order.

## 3. Write tickets, one file each

**What.** One file per ticket in `.scratch/<effort>/issues/NN-short-name.md` (template in
`.scratch/TEMPLATE-ticket.md`). There are two kinds:

| | Decision ticket | Build ticket |
|---|---|---|
| answers | a question ("what shape should X be?") | "deliver X" |
| done when | the question is answered, with evidence | the acceptance checks pass at its `verified_by` level |
| often resolved by | a prototype the human reacts to | code |

Every ticket has a **checkable acceptance list**, a **`verified_by`** level and an **out of
scope** list.

**Why one file each.** Separate files do not collide when several people or agents edit at once,
and each ticket's history stays readable.

**Why acceptance must be checkable.** If acceptance is a number like a word count, the work can
pad to meet it. Ask for something a check can verify structurally: the sections are present, every
claim cites a source, the test exists and fails without the fix.

**Why "out of scope".** It is the field people skip, and it is the one that stops a worker
wandering into the next ticket.

**Later:** tickets can move to GitHub Issues once the team works from GitHub. The map and specs
stay in the repo, next to the code.

## 4. Build, usually in one session

**Default: one agent session, coached.** It explains the approach, builds one ticket, and proves it
at its `verified_by` level.

**When more than one agent is needed**, for example several independent build tickets at once:

```
              human (decides)
                    │
              lead session ── owns the map and tickets, reviews every result
             ╱      │      ╲
     worker A   worker B   worker C ── one ticket each, own git worktree, own branch
```

- The lead hands out only **settled** build tickets, where every question is already answered.
- Each worker works in its own **git worktree** (`git worktree add ../proj-ticket-07 -b ticket-07`),
  so no two agents share a working tree or a git index.
- Workers report back by writing in **their own ticket file**: progress, blockers and questions.
  They never talk to each other and never edit shared docs.
- The lead merges, one ticket at a time.

**Why not peer agents talking to each other?** We tried two equal agents sharing one tree, talking
through a shared document. It worked but was clumsy and wasteful. They wrote the same fact in two
places. They collided on shared numbering. One agent's commit swept up the other's staged files.
Nobody was clearly in charge. A lead with a single plan, and workers who only report up, removes
all of that.

## 5. Review: walk the human through the diff

**What.** Before merging, the agent explains the diff to a human:

- what changed and why;
- what proves it;
- what is not proven yet.

The human decides. The mattpocock `/code-review` skill checks the diff two ways, separately:
against the house standards, and against the ticket.

**Why.** The review is where the human learns the codebase. Without it, a team using agents ends
up with code that nobody on the team has read.

## 6. Prove it, at the right level

Every ticket declares `verified_by`:

- **`static`**: tests, lint, type checks and review.
- **`staged`**: running in a realistic stand-in, such as a simulator or staging server.
- **`real`**: running where it will actually run, as the account that will run it.

**Anything proven below its declared level goes in `docs/WHAT_TO_WATCH.md`**, with a check someone
can run later and the result that would mean it failed. That list is the honest answer to "is X
working?".

**Prove each new guard can fail.** Plant the bug, watch the guard fail, then restore the code from
a backup copy. This is test method validation: a gauge that always reads "pass" is not a gauge.

## 7. Write it down, as you go

| Record | Holds | Written when |
|---|---|---|
| `docs/GLOSSARY.md` | words that mean two things here | you notice a term means two things |
| `docs/WHAT_TO_WATCH.md` | unproven claims, each with a runnable check | something ships below its proof level |
| `docs/LESSONS.md` | dated lessons, each a story plus the rule it taught | a mistake teaches something general |
| `docs/TIMELINE.md` | a few lines per phase | a phase ends |
| `docs/concepts/` | one page per concept learned | you learn something new |

**Keep them short.** The previous project's timeline grew to hundreds of kilobytes, and a ledger
nobody reads is clutter. Git holds the detail. The ledgers hold the meaning.

**Write for a newcomer.** Imagine a reader who has never seen the project. Translate private
shorthand into plain words.

## 8. Add rules when they are earned

Start with the house rules in `CLAUDE.md` and nothing more. When a bug teaches a general lesson:

1. write the story in `docs/LESSONS.md`;
2. if it should never happen again, add a **guard test** and prove it fails on the bug;
3. add a one-line rule to `CLAUDE.md` that points at the guard.

A rule with no story will be ignored or "fixed" by the next person. A rule with a guard does not
depend on anyone remembering it.
