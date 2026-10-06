"""The copy script: copies the tracked kit into a folder, never overwrites an existing file."""

import re
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import new_project  # noqa: E402


def test_only_tracked_files_are_copied_and_never_kit_dev(tmp_path):
    for rel in ("README.md", "kit-dev/some-effort/map.md"):
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_text("x\n")
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "add", "README.md", "kit-dev"], check=True)
    (tmp_path / ".junk_cache").mkdir()
    (tmp_path / ".junk_cache" / "x").write_text("junk\n")                       # planted: untracked

    assert new_project.kit_files(tmp_path) == ["README.md"]


def test_a_copy_without_git_stops_and_says_clone(tmp_path):
    (tmp_path / "README.md").write_text("x\n")                                  # planted: a ZIP copy

    with pytest.raises(new_project.NotAGitClone, match="git clone"):
        new_project.kit_files(tmp_path)


def test_an_empty_target_gets_the_whole_kit_and_none_of_its_machinery(tmp_path):
    _, skipped = new_project.copy_kit(tmp_path)
    assert not skipped
    for must in ("CLAUDE.md", "README.md", "layers.toml", "tests/test_layers.py",
                 "docs/PRINCIPLES.md", ".claude/settings.json", ".scratch/TEMPLATE-ticket.md"):
        assert (tmp_path / must).is_file(), must
    assert not (tmp_path / "scripts" / "new_project.py").exists()
    assert not (tmp_path / "tests" / "test_new_project.py").exists()
    assert not (tmp_path / ".git").exists()
    assert not (tmp_path / "kit-dev").exists()


def test_an_existing_repo_keeps_its_files(tmp_path):
    (tmp_path / "README.md").write_text("our project\n")
    (tmp_path / "CLAUDE.md").write_text("our rules\n")
    copied, skipped = new_project.copy_kit(tmp_path)

    assert (tmp_path / "README.md").read_text() == "our project\n"
    assert (tmp_path / "CLAUDE.md").read_text() == "our rules\n"
    assert skipped == ["CLAUDE.md"]
    assert "docs/METHOD.md" in copied


def test_the_moved_readme_links_still_resolve(tmp_path):
    (tmp_path / "README.md").write_text("ours\n")
    new_project.copy_kit(tmp_path)
    method = tmp_path / "docs" / "METHOD.md"
    links = re.findall(r"\]\(([^)#]+)\)", method.read_text())
    assert links
    broken = [link for link in links if not (method.parent / link).resolve().exists()]
    assert not broken, broken
