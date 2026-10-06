# kit-dev: building the kit itself

Everything here is about developing this kit: its maps, its tickets, and (when a phase ends) its
own timeline and lessons. `scripts/new_project.py` never copies this folder into a project.

Everything outside this folder is what a project receives. `docs/TIMELINE.md`, `docs/LESSONS.md`
and `.scratch/` are blank templates for the project, so the kit's own records never go there.

```
kit-dev/
  <effort>/map.md                   where a piece of kit work is going
  <effort>/issues/01-short-name.md  one file per ticket
```

Templates for both are in `.scratch/`.
