# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression tests for the release tooling configuration (tbump.toml)."""

from __future__ import annotations

import shutil
import subprocess
import tomllib
from pathlib import Path

import pytest

TBUMP_TOML = Path(__file__).parent.parent / "tbump.toml"


def _renormalize_cmd() -> str:
    with open(TBUMP_TOML, "rb") as f:
        config = tomllib.load(f)
    cmds = [
        step["cmd"]
        for step in config["before_commit"]
        if "--renormalize" in step["cmd"]
    ]
    assert len(cmds) == 1
    return str(cmds[0])


def test_deletions_are_staged_before_renormalize() -> None:
    cmd = _renormalize_cmd()
    assert "git add --update" in cmd
    assert cmd.index("git add --update") < cmd.index("git add --renormalize")


@pytest.mark.skipif(shutil.which("git") is None, reason="git is required")
def test_renormalize_command_handles_deleted_tracked_file(tmp_path: Path) -> None:
    def git(*args: str) -> str:
        return subprocess.run(
            ["git", "-c", "user.name=t", "-c", "user.email=t@example.com", *args],
            cwd=tmp_path,
            check=True,
            capture_output=True,
            text=True,
        ).stdout

    git("init", "-q")
    expected = tmp_path / "expected.314.txt"
    expected.write_text("content\n", encoding="utf-8")
    git("add", ".")
    git("commit", "-q", "-m", "init")
    expected.unlink()

    result = subprocess.run(
        _renormalize_cmd(),
        shell=True,
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert git("diff", "--cached", "--name-status").split() == ["D", "expected.314.txt"]
