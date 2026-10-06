"""Copy this kit into a project: a new empty folder, or a repo that already has files.

    python scripts/new_project.py <target-dir>

It never overwrites. A file that already exists in the target is skipped and listed, so you can
merge it by hand (an existing CLAUDE.md is the usual one). If the target already has a README.md,
the kit's README lands at docs/METHOD.md instead, with its links fixed for the new location.

The kit's MIT LICENSE lands at docs/KIT-LICENSE, so it covers the kit's files without becoming the
project's own license.

It copies only the files git tracks, so the kit must be a `git clone`, not a ZIP download. The
kit's own development records in kit-dev/ are never copied.

It does not commit or push. Review the result, then commit it yourself.
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]

# The kit's own machinery and development records, which a project does not need.
SKIP_DIRS = ("kit-dev/",)
SKIP_FILES = {"scripts/new_project.py", "tests/test_new_project.py"}


class NotAGitClone(Exception):
    pass


def git(kit: Path, *args: str) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(["git", "-C", str(kit), *args], capture_output=True, text=True)
    except FileNotFoundError:
        raise NotAGitClone("git is not installed, so the kit's files cannot be listed.") from None


def kit_files(kit: Path = KIT) -> list[str]:
    """The files git tracks in the kit, minus the kit's own machinery.

    Asking git, not walking the folder, leaves out whatever local tools left behind (caches,
    virtual environments). A copy with no git history cannot tell the two apart, so it stops.
    """
    top = git(kit, "rev-parse", "--show-toplevel")
    if top.returncode != 0 or Path(top.stdout.strip()).resolve() != kit.resolve():
        raise NotAGitClone(f"{kit} is not a git clone of the kit, so its own files cannot be told "
                           "apart from leftovers. Get it with `git clone <kit-url>` and run this "
                           "again.")
    tracked = git(kit, "ls-files", "-z").stdout.split("\0")
    return sorted(rel for rel in tracked
                  if rel and (kit / rel).is_file()
                  and not rel.startswith(SKIP_DIRS) and rel not in SKIP_FILES)


def readme_as_method(text: str) -> str:
    """The kit README, with links rewritten to work from docs/METHOD.md."""
    def fix(m: re.Match) -> str:
        target = m.group(1)
        if re.match(r"[a-z]+://|#", target):
            return m.group(0)
        if target.startswith("docs/"):
            return f"]({target[len('docs/'):]})"
        return f"](../{target})"
    return re.sub(r"\]\(([^)]*)\)", fix, text)


def copy_kit(target: Path) -> tuple[list[str], list[str]]:
    """Copy the kit into `target`. Returns (copied, skipped), as paths relative to the target."""
    files = kit_files()
    target.mkdir(parents=True, exist_ok=True)
    copied, skipped = [], []
    for rel in files:
        dest_rel = rel
        if rel == "README.md" and (target / "README.md").exists():
            dest_rel = "docs/METHOD.md"
        elif rel == "LICENSE":
            dest_rel = "docs/KIT-LICENSE"   # the kit's license, kept with its docs; not the project's
        dest = target / dest_rel
        if dest.exists():
            skipped.append(dest_rel)
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest_rel == "docs/METHOD.md":
            dest.write_text(readme_as_method((KIT / rel).read_text(encoding="utf-8")),
                            encoding="utf-8")
        else:
            shutil.copy2(KIT / rel, dest)
        copied.append(dest_rel)
    return copied, skipped


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    target = Path(sys.argv[1]).expanduser().resolve()
    if target == KIT or KIT in target.parents:
        print("The target must be outside the kit.")
        return 2
    try:
        copied, skipped = copy_kit(target)
    except NotAGitClone as e:
        print(e)
        return 2
    print(f"Copied {len(copied)} files into {target}.")
    if "docs/METHOD.md" in copied:
        print("  The target had a README.md, so the kit's README is at docs/METHOD.md.")
    if skipped:
        print(f"\nSkipped {len(skipped)} that already exist (merge these by hand):")
        for s in skipped:
            print(f"  {s}")
    print("\nNext:\n"
          "  1. Fill in the <!-- FILL IN --> parts of CLAUDE.md.\n"
          "  2. Delete docs/MODEL_OUTPUT.md if the code never reads AI model output.\n"
          "  3. Review, commit the files by name, and push.\n"
          "  4. Start Claude Code there and ask it to grill you on the first map.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
