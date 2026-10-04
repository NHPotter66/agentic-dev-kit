# CLAUDE.md

Every Claude Code session in this repo reads this file first. It is the working agreement between
the humans and the agents. Keep it short: each rule here has a reason, and the longer stories live
in `docs/PRINCIPLES.md`.

## What this project is

<!-- FILL IN: two or three sentences. What it does, who it is for, what "done" looks like. -->

## Working style

- **Coach, step by step.** The humans here are learning the domain. Explain the concept and the
  tradeoffs before writing code, and relate new ideas to something the person already knows.
- **Offer options, the human chooses.** After each piece lands, present the next options with a
  recommendation. Do not race ahead.
- **Grill before building anything non-trivial.** Ask one round of numbered questions at a time,
  each with a recommended answer. Look facts up yourself; only ask for decisions.
- **Cut complexity that is not needed yet.** Add structure when the second real case appears.
- **Humans make changes too.** Expect files to move under you, and re-read before editing.

## The loop

1. Grill → map → decision tickets → build tickets (see `docs/PLAYBOOK.md`).
2. Build one ticket. Prove it at its `verified_by` level.
3. Walk the human through the diff. They decide whether it merges.
4. Update the docs the change touched. Add a short `docs/TIMELINE.md` entry at the end of a phase.
5. Offer the next options.

## House rules

Each rule has a reason. Add a rule when its bug first bites, with the story in `docs/LESSONS.md`.

- **Layers point down.** `layers.toml` lists the layers, lowest first. Code may import its own
  layer or any lower one. `tests/test_layers.py` enforces it. *Why:* untangling upward imports late
  is expensive. The previous project had 57 to undo after eight months.
- **One owner for shared state.** Time, configuration and paths each come from one module, and are
  looked up when used, never copied into a module at import. *Why:* a copy taken at import time
  keeps whatever a test had swapped in, and the bug only shows up in some test orders.
- **A new guard is proven before it is trusted.** Plant the bug it is for, watch the guard fail,
  then restore the code from a backup copy. *Why:* a guard that cannot fail protects nothing.
- **"Could not measure" is its own answer.** A check that found nothing to look at says so. It
  never reports zero or "clean".
- **Every ticket states `verified_by`.** Anything proven below that level goes in
  `docs/WHAT_TO_WATCH.md`.

## One way to do each thing

<!-- FILL IN as the project picks them. One line each, with the reason. Example rows: -->

| Thing | The one way | Why |
|---|---|---|
| Reading the time | <!-- e.g. `clock.now()` --> | one timezone, testable |
| Reading config | <!-- e.g. `config.get(...)` at call time --> | tests can swap it safely |
| Logging | <!-- --> | |
| Paths to data | <!-- --> | |

## Proof levels

<!-- FILL IN what each level means for this project. -->

| Level | Means | Example |
|---|---|---|
| `static` | unit tests, lint, type checks, review | <!-- --> |
| `staged` | runs in a realistic stand-in | <!-- e.g. a simulator, a staging server --> |
| `real` | runs where it will actually run, as the account that will run it | <!-- --> |

## Git

- Commit only your own files, by name: `git commit -m "…" -- path/a path/b` (run `git add` first
  for new files). Never `git add -A` or `git add .`.
- Agents never push. A human pushes.
- Commit messages: `type(scope): what changed`, with `type` one of feat, fix, refactor, docs, test
  or chore.

## Parallel work

Use one session unless more than one agent is genuinely needed. If it is:

- A **lead** session owns the map and the tickets. A human decides.
- Each **worker** takes one settled build ticket and works in its own git worktree, on its own
  branch.
- Workers write progress and questions into their ticket file. They never edit the map, other
  tickets, or shared ledgers, and never coordinate with each other.
- Name things by what they are, never by a shared counter that two sessions might both increment.

## Tests & lint

<!-- FILL IN the exact commands, with how long the suite takes. -->

```bash
pytest          # runs the layer guard and the project's tests
```

Run one test process at a time, in the foreground, with a timeout.

## Where things are

- `docs/README.md`: index of every doc.
- `docs/GLOSSARY.md`: read before naming anything.
- `docs/structure/README.md`: the layer map. Read before moving code between modules.
- `docs/WHAT_TO_WATCH.md`: check here first when asked "is X working?"
- `.scratch/`: the map and tickets.
