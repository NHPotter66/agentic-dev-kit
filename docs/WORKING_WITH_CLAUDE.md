# Working with Claude Code here

For anyone new to coding agents. Fifteen minutes to read.

## What it is

Claude Code is an AI agent that runs in your terminal, inside this repo. It can read files, run
commands and tests, and edit code. It reads `CLAUDE.md` at the start of every session. That file
is how the project tells it the rules.

It does not remember previous sessions on its own. Anything it should know next time must be
written in the repo, which is why this project writes so much down.

## A session, start to finish

1. **Start it in the repo:** `claude`.
2. **Say what you want, plainly.** "I want to add X" or "this is broken, here is the error". Paste
   errors in full.
3. **For anything non-trivial, let it grill you.** It asks numbered questions, each with its
   recommendation. Answer the ones you have opinions on. "Your recommendation is fine" is a real
   answer.
4. **It explains, then builds.** It should tell you the approach before it writes code. If it
   doesn't, ask: "Explain the approach first."
5. **It proves the change.** Ask what proved it, and at which level: `static`, `staged` or `real`.
6. **It walks you through the diff.** You decide whether to commit. It commits only the files it
   changed. **You push.**

## Useful commands

| Command | What it does |
|---|---|
| `/grill-me` | Interviews you on a design until nothing is left undecided. |
| `/mattpocock-skills:code-review` | Reviews a diff against the house rules and against the ticket, separately. (Plain `/code-review` is Claude Code's own bug review.) |
| `/plan` | Plans before touching files. |
| `/compact` | Shrinks a long conversation so it can continue. |
| `/resume` | Picks up an earlier session. |
| `/model`, `/effort` | Choose the model and how hard it thinks. |

## How to work well with it

- **Ask it to show, not tell.** "What proves that?" and "Show me the line" are the most useful
  questions you can ask.
- **Short answers are fine once it has offered options.** "Option 2" or "go for it" works because
  the thinking is already on the table.
- **Correct it once, in writing.** If it gets something wrong in a way that will come back, ask it
  to add the rule to `CLAUDE.md` or a doc, with the reason. Then it won't happen again next
  session, for anyone.
- **Interrupt freely.** "Wait, before you do that" is normal.
- **Be suspicious of "all tests pass".** Ask whether the test could have failed. See principle 3
  in `PRINCIPLES.md`.

## What it should not do here

- Push to the remote. A human pushes.
- `git add -A`. It commits named files only.
- Start several test runs at once.
- Make a decision that is yours. If it does, say so. That's a bug in how it was asked.

## Several agents at once

Mostly you won't need this. When you do, read `PLAYBOOK.md` §4: one lead session, workers in
separate git worktrees, and workers report only through their ticket files.
