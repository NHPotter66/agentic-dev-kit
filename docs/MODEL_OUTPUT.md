# When your code reads what an AI model writes

**Optional.** Delete this file if your project never parses, files or acts on model output.

This is about prompts whose output *code* consumes, like a step whose text gets parsed, saved or
checked. It is not about chatting. For a chat, rewording a prompt is a matter of style. For a
pipeline step, rewording the prompt changes the contract.

Each rule below came from a measurement or a failure in a previous project.

---

## 1. Ask for a literal token, with its evidence right next to it

Don't ask the model to "be careful" or "give a fix for each problem". Ask for a fixed marker on its
own line, with its evidence on the very next line:

```
PROPOSE: <the recommendation>
CHECK: <file> | <what to look for> | <what you expect to find>
```

**Measured.** Same task, same 24 inputs, only the instruction changed.

| | Proposals | Backed by evidence a machine could check |
|---|---|---|
| asked for "care" | 53 | **0** |
| asked for the token with adjacent evidence | 47 | **27 (57%)** |

The careful-sounding version produced *more* output and none of it was checkable. The model did
cite things, but in the narrative, not attached to any proposal.

## 2. Every record carries its own evidence

If the output becomes a list of records, each record must carry its evidence. A citation in the
summary does not verify a claim in item 7.

## 3. Make it cite first, then conclude

Telling a model it may answer "nothing found" is not enough. It will still invent something.
Make the structure force the order: first the exact quote from the source, then the conclusion
drawn from it. Then check in code that the quote really appears in the source.

**Measured.** A model told plainly it could return nothing made something up in 4 out of 4 runs.
The same model, asked for `{quote, then gist}` in that order with a code check on the quote,
correctly returned nothing in 4 out of 4.

## 4. Never ask a model for a fact your code already has

If the code knows the date, the count or the previous score, the code supplies it. Asking the model
to restate it invites a confident wrong number.

**Observed.** A scoring prompt asked the model to report a baseline that had never been run. It
made one up every time (239 of 239 reports), and 63 of those made-up numbers passed the gate.

## 5. A demonstration can't be faked; a judgement can

Prefer gates the work itself produces, like "the test runs and passes" or "the file exists and
parses", over a model's opinion of the work. A model judge is useful, but it is never the only
gate.

## 6. Start each work item from a clean workspace

Leftover output from earlier tasks in an agent's working memory isn't helpful context. The model
treats it as an example to follow.

**Observed.** An agent's notes still held earlier, rejected drafts, and it copied them 15 times in
a row. Each run now starts from an empty workspace, and anything it needs is passed in explicitly.

## 7. Label how strong each claim is

- **measured**: a comparison with a control, with the numbers;
- **observed**: seen happening, with a date, but nothing to compare against;
- **inferred**: reasoned from the above.

A claim marked *measured* names its control. Without a comparison, many runs are still only
*observed*.

## 8. Read what the tools returned before tuning the prompt

When an agent gives a bad answer, check what its tools handed it before rewriting the prompt. More
than once, the "model problem" was a tool returning empty or wrong data.
