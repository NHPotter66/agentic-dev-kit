# Glossary

Words this project uses in a specific way. **Terms with more than one meaning go first**, because
those are the ones that cause bugs and wrong conversations.

Add a term the moment you notice two people (or a person and an agent) mean different things by it.

## Terms with more than one meaning

<!-- e.g. **"task"**: (1) a background job in the code; (2) a to-do item for a person. Say which. -->

## Method terms

- **Grill**: an interview before building. Numbered questions, each with a recommended answer,
  until nothing is left to decide.
- **Map**: a document saying where an effort is going and in what order. It decides; it does not
  build.
- **Decision ticket**: a ticket that answers a question. **Build ticket**: a ticket that delivers
  work.
- **Lead / worker**: in parallel work, the lead session owns the plan; workers each do one ticket.
- **`verified_by`**: the level a change must be proven at: `static`, `staged` or `real`.
- **Guard test**: a test that enforces a rule across the codebase (for example, the layer guard).
- **Plant the bug**: break the code on purpose to prove a guard can fail, then restore it.
- **Layer**: a group of modules. Code may depend on its own layer or lower ones, never higher.

## Project terms

<!-- FILL IN -->
