# Principles, and the stories behind them

Nine rules, each learned the hard way while building a personal AI assistant with Claude Code over
eight months. That project ran on a home server: a web app, AI agents, a scheduled overnight job,
and a store of notes. Each story is told without that project's private vocabulary.

Every principle has the same parts:

- **the rule**;
- **the story** that taught it;
- **how to apply it** here.

---

## 1. One owner for shared state, read when used

**Rule.** Things the whole program shares, like the current time, configuration and data paths,
each come from exactly one module. Code asks that module at the moment it needs the answer, and
never keeps its own copy.

**Story: two clocks.** Two parts of the system each worked out "what day is it". One used UTC and
the other used local time. A daily check compared them, and for the hours when the two dates
disagreed, it thought it had already run. It ran every *other* night for four weeks before anyone
noticed.

**Story: the stale copy.** A module took its own copy of a configuration function at startup
(`from config import get_path`). One test replaced that function with a stand-in pointing at a
temporary folder. If that test happened to load the module first, the module kept the stand-in for
the whole run. Every later file write went to a temporary folder, and six unrelated tests failed,
but only when the tests ran in a certain order.

**Apply.**
- Make one `clock` module and one `config` module. Everything else calls them.
- Call `config.get_path()` where you need it. Don't copy it at import time.
- When a default argument is a date, a path or an ID, that's a second clock hiding. Require it
  from the caller instead.

## 2. Prove it where it runs

**Rule.** A test passing on your machine, as your user, is not evidence it works in production, in
the simulator, or on the device. Prove things in the environment, and as the account, that will
run them.

**Story.** A feature passed every unit test and every live check, all run as the developer's admin
account. In production it failed three ways. The service account couldn't read the folders the
feature read. The service's security sandbox blocked a folder it wrote to. And a check meant to
prove "the service can do this" was actually checking a root process, so it proved the wrong
thing. The user found the first two by clicking around.

**Apply.**
- Every ticket says how it will be proven: `static`, `staged` or `real`.
- Before saying "done", ask: which user, which machine, which sandbox? Test there, or write in
  `WHAT_TO_WATCH.md` that you couldn't.
- Prefer asking a running service over reading its files.

## 3. A pass is a claim

**Rule.** A green check means the check ran. It does not mean the thing is true. Before trusting a
check, show that it *can* fail. When a check found nothing to look at, report "could not measure",
never zero.

**Story.** Nine overnight jobs ran and all nine reported "ok". One of them reported that the
search index was completely broken. The index held 6,733 entries and worked fine. "ok" meant the
job finished, not that what it said was true.

**Story.** A report was written to list problems in a folder of documents. If the folder path was
wrong, it would read an empty folder and print "0 problems, clean", which looks exactly like
success. It was rebuilt to say `CANNOT MEASURE` instead, and a test checks that it never prints
"clean" in that case.

**Apply.**
- **Plant the bug.** For every new guard test, break the code on purpose, confirm that specific
  test fails, then restore from a backup. In quality terms, this validates the test method: a
  gauge that cannot read "fail" is not a gauge.
- Checks have three outcomes: pass, fail, and could-not-measure.
- **Expect a specific change.** If a fix should move a number and the number didn't move, that's
  data, not noise.

## 4. One change at a time, when undoing is hard

**Rule.** When a change is hard to reverse, or its effects are hard to see, turn on one thing,
watch it, then turn on the next. Each one needs a written check that shows it is doing the right
thing.

**Story.** After the nine-"ok" night, every overnight job was switched off. Each one came back
only after it had a written check proving its output was *true*, not just produced, and only one
per night. If several come back at once and something is wrong, you can't tell which one is lying.

**Apply.** For hardware, production data, and anything with a cost per run: one behavior at a
time, each with its check written down first.

## 5. Find the cause before you fix it

**Rule.** Before blaming a cause, measure what actually happened. Before calling something a
pattern, check how often it happens anyway. One occurrence is a story, not a finding.

**Story.** An agent kept failing to finish its task. The obvious cause was that its input was too
long. Before building a fix, someone measured: the input was nowhere near the limit. The agent was
going in circles. The planned fix would have changed nothing.

**Story.** The test suite seemed to hang. It wasn't a test. Several test runs had been started at
once and were fighting over the same graphics card. A single clean run proved it. Running tests one
at a time is now a house rule.

**Apply.** "What did the logs, counts or telemetry actually show?" comes before "here is the fix".
When you have one example, look for the base rate before you act on it.

## 6. Read what the running system reports

**Rule.** The file you opened may not be the setting that is in force. Configuration is usually
layered: defaults, then overrides, then environment. Ask the running system what it is actually
using.

**Story.** A config file said a key setting was empty, and a blocker was raised: "the system is
using the wrong model". The file was only the base layer. An override file sat on top, and the
setting in force was fine. The blocker was false and cost a review cycle.

**Apply.** Prefer an endpoint, a status command or a log line that reports the effective value.
When the answer surprises you, check whether you are reading one layer too low.

## 7. Every write needs a reader

**Rule.** Data that is written but never read back is as invisible as data that was never saved.
When you add a record, add the thing that reads it, or ask who will.

**Story.** A tool decided that pairs of documents were "not duplicates", and wrote a careful reason
for each decision to a log: 23 of them. Nothing ever read that log. The user disagreed with some of
the decisions and had no way to see the reasons or overturn them. The fix was a reader and a
report, not more writing.

**Story.** A self-improvement loop "promoted" 60 improvements. None of them took effect, because
the final step quietly failed. The loop kept producing promotions anyway. A loop that cannot take
effect will still produce output forever.

**Apply.** For every log, record or status field, name its reader. For every automated loop, check
the last step actually changes something.

## 8. Simplest thing that works

**Rule.** Don't add structure for a need you don't have yet. Add the abstraction when the second
real case arrives, not the first. When a setup grows exceptions, look for a simpler general rule.

**Story.** A feature was switched on agent by agent, and the list grew three named exceptions. It
was replaced by "every agent gets it", with only real structural limits still applying. There was
one rule instead of a list to keep in sync.

**Story.** Two proposed extension points for a plugin format were examined and declined, in
writing, because nothing yet needed them. That note stopped them from being proposed again for
months.

**Story, the other side.** The *structure* rule (layers, imports point down) is the one exception
worth setting up early. Added after eight months, it meant untangling 57 wrong-direction imports.
It costs almost nothing on day one.

**Apply.** Keep code modular, simple and standardized: layers from the start, one way to do each
common thing, and everything else only when needed.

## 9. Write it down, with the reason

**Rule.** Decisions, rules and lessons live in the repo, next to *why* they were made. Not in a
chat, not in one person's head, not in one person's AI settings.

**Story.** In the previous project, the corrections taught to the AI were saved in the developer's
personal AI settings. They worked well, for one person. A coworker's AI would never have seen them.
That is why this kit puts every rule in `CLAUDE.md` and `docs/`.

**Story.** A decision *not* to build something was written down with its evidence. It was never
proposed again, and nobody had to argue it twice.

**Apply.**
- A rule always carries its reason. A rule without a reason gets "fixed" by the next person.
- A decision *against* something is worth recording too.
- Mark the strength of every claim: **measured** (with a comparison), **observed** (seen, no
  comparison) or **inferred** (reasoned).
