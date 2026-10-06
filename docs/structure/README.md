# Structure: the layers

The code is arranged in layers. **A module may depend on its own layer or any lower one, never a
higher one.** That keeps the code modular: you can understand, test or replace a lower layer
without reading anything above it.

The layers are listed, lowest first, in `layers.toml` at the repo root. `tests/test_layers.py`
enforces them.

## The layers

<!-- FILL IN at the first grilling session. A typical shape, lowest first:
1. foundation: config, clock, logging, shared types
2. adapters: talking to hardware, services, files
3. core logic
4. orchestration: putting the pieces together into tasks
5. surfaces: CLI, UI, API
-->

## When a lower layer needs something from a higher one

Don't import upward. The usual fixes:

- **Pass it in.** The higher layer hands the lower one what it needs, such as a function, a value
  or a callback.
- **Declare and collect.** The lower layer declares what it offers, for example in a config entry,
  and a higher layer collects it.
- **Move it down.** If both layers need it, it probably belongs in a lower layer.

A genuine exception goes in `layers.toml` under `accepted`, with its reason. That list should only
ever shrink.

## Adapting the guard to another language

`tests/test_layers.py` reads Python imports. For another language, keep `layers.toml` as it is and
replace only the `imports_of()` function with one that lists a file's dependencies, for example by
reading `#include` lines or a build file's dependency list. Then plant an upward dependency and
confirm the guard catches it.

## What the guard cannot see

It reads `import` lines, absolute and relative. It cannot see an import built at run time, such as
`importlib.import_module(name)`. Keep those rare, and say in a comment which layer they reach.
