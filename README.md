# Agentic Dev Kit

A starting point for building software with AI coding agents, using Claude Code, as a team
of humans and agents. Copy this repo into a new project, fill in the blanks, and you start with
a way of working that has already been tested.

The method comes from eight months and about 1,100 commits of building a personal AI assistant
with Claude Code. Most of what is here was learned by getting it wrong first. The stories are in
[docs/PRINCIPLES.md](docs/PRINCIPLES.md).

---

## Where we are going

We want a project where:

- **Agents write most of the code, and humans make the decisions.** The agent explains the options
  and their tradeoffs. A human chooses. The agent builds what was chosen.
- **Anyone can join and understand it.** Every rule has its reason written next to it. Every
  term with two meanings is in a glossary. Nothing important lives only in one person's head or
  one person's AI settings.
- **"It works" means proven, not passed.** A green test is a claim. We say how something was
  proven (`static`, `staged` or `real`), and we keep a list of what is not proven yet.
- **The code stays modular, simple and standardized.** It has layers that only point downward,
  one way to do each common thing, and no structure added before it is needed.

## How the work flows

```
 idea ──► grill ──► map ──► decision tickets ──► build tickets ──► review ──► merge
          (talk it   (where   (questions that     (one unit of      (a human
          through)   we are   must be answered    work each, with   walks the
                     going)   before building)    its proof level)  diff)
```

1. **Grill.** Before building anything non-trivial, the agent interviews you, one round of
   questions at a time, each with its recommended answer. You decide. This is where most of the
   value is: decisions get made on purpose instead of by accident.
2. **Map.** A short document says where the work is going, in what order, and what is still
   unknown. A map decides. It does not build.
3. **Tickets.** One file per ticket. There are two kinds:
   - a **decision ticket** answers a question;
   - a **build ticket** delivers a piece of work.

   Every ticket says how it will be proven and what is out of scope.
4. **Build.** Usually one agent session, coached step by step. When more than one agent is
   really needed, one **lead** session (with a human deciding) hands settled build tickets to
   **worker** sessions. Each worker works in its own git worktree. Workers report back in their
   ticket file. They never coordinate with each other directly.
5. **Review.** The lead walks a human through each diff before it merges.

The full method, and why each step exists, is in [docs/PLAYBOOK.md](docs/PLAYBOOK.md). If you are
new to working with an AI agent, start with
[docs/WORKING_WITH_CLAUDE.md](docs/WORKING_WITH_CLAUDE.md).

## The rules, in brief

The nine principles in short. Each one has a real story in [docs/PRINCIPLES.md](docs/PRINCIPLES.md).

| # | Principle | In one line |
|---|---|---|
| 1 | **One owner for shared state** | Time, configuration and paths each have one module that answers them, read when used, not copied at startup. |
| 2 | **Prove it where it runs** | Passing on your laptop is not passing in production, in the simulator, or on the device. |
| 3 | **A pass is a claim** | Prove a check can fail before trusting that it passed, and "could not measure" is not zero. |
| 4 | **One change at a time** | When something is hard to undo, turn on one thing, watch it, then the next. |
| 5 | **Find the cause before fixing** | Measure what happened before you blame something, and one occurrence is a story, not a pattern. |
| 6 | **Read what the system reports** | The file you opened may not be the setting in force, so ask the running system. |
| 7 | **Every write needs a reader** | Data that nothing reads back is as invisible as data that was never saved. |
| 8 | **Simplest thing that works** | Add structure when the second real case arrives, not the first. |
| 9 | **Write it down, with the reason** | Decisions live in the repo next to why they were made, not in memory. |

The house rules for day-to-day work are in [CLAUDE.md](CLAUDE.md), which every agent reads at
the start of every session. A few of them:

- Imports point down the layers only, and a test enforces it.
- Commit only the files you changed, by name. Never `git add -A`.
- Agents do not push. A human does.
- Every new guard test is shown to catch the bug it is for before it is trusted.

## What is in the box

```
CLAUDE.md                  the working agreement every agent session reads first
.claude/settings.json      shared Claude Code settings: plugins and permissions for everyone
docs/
  README.md                index of every doc, one line each
  PLAYBOOK.md              the method, step by step, and why
  WORKING_WITH_CLAUDE.md   for people new to coding agents: a session, start to finish
  PRINCIPLES.md            the nine rules, each with the story that taught it
  MODEL_OUTPUT.md          optional: if your code reads what an AI model writes
  GLOSSARY.md              words that mean more than one thing here
  WHAT_TO_WATCH.md         claims not yet proven, each with a check you can run
  LESSONS.md               this project's own dated lessons
  TIMELINE.md              a short log, one entry per phase of work
  concepts/                one page per new concept, related to something familiar
  structure/README.md      the layer map: which code may depend on which
.scratch/                  the map, specs and tickets (templates included)
tests/test_layers.py       the layer guard, with its own control test
layers.toml                the layer map in data form, which the guard reads
```

## Starting a new project from this kit

1. Copy the repo and rename it.
2. Fill in the `<!-- FILL IN -->` sections of `CLAUDE.md`: what the project is, how to run
   tests, what `staged` and `real` mean for it.
3. Delete `docs/MODEL_OUTPUT.md` if your code never reads AI model output.
4. Open Claude Code and ask it to grill you on the first map.

The kit stays generic. Project knowledge (a framework, hardware, a domain) goes in the project,
never back in the kit. Improvements to the method itself come back here.
