# test_initial_state.py

"""
Pytest suite that validates the initial repository state *before* the student
runs any commands.

Checked items (pre-conditions):
1. /home/user/project/scripts/md_lint
   • Exists, is a regular file, is executable.
   • Has permission bits 0o755.
   • Contains the exact, line-by-line Bash script provided in the task
     description (including the trailing newline on the last line).

2. /home/user/project/README.md and /home/user/project/CHANGELOG.md
   • Both files must already exist (contents are irrelevant).

Nothing related to the build output directory or the future log file is
validated here, in accordance with the grading-suite rules.
"""

import os
import stat
from pathlib import Path

PROJECT_ROOT = Path("/home/user/project")
SCRIPT_PATH = PROJECT_ROOT / "scripts" / "md_lint"


def test_md_lint_file_exists_and_is_executable():
    """
    The linter script must exist, be a regular file, and be executable.
    """
    assert SCRIPT_PATH.exists(), f"Expected {SCRIPT_PATH} to exist, but it is missing."
    assert SCRIPT_PATH.is_file(), f"Expected {SCRIPT_PATH} to be a file, but it is not."
    assert os.access(SCRIPT_PATH, os.X_OK), (
        f"{SCRIPT_PATH} must be executable (chmod +x). "
        "Make sure it has at least one executable bit set."
    )


def test_md_lint_has_correct_permissions():
    """
    The linter script must have permission mode 0o755.
    """
    mode = SCRIPT_PATH.stat().st_mode & 0o777
    expected_mode = 0o755
    assert mode == expected_mode, (
        f"{SCRIPT_PATH} should have permissions 755 (rwxr-xr-x), "
        f"but has {oct(mode)} instead."
    )


def test_md_lint_contents_are_exact():
    """
    The linter script content must exactly match the specification,
    down to the final newline.
    """
    expected_content = (
        "#!/usr/bin/env bash\n"
        'echo "README.md:1 MD001/heading-increment Header levels should only increment by one level at a time"\n'
        'echo "CHANGELOG.md:5 MD012/no-multiple-blanks Multiple consecutive blank lines"\n'
    )

    actual_content = SCRIPT_PATH.read_text(encoding="utf-8")

    assert (
        actual_content == expected_content
    ), (
        f"Contents of {SCRIPT_PATH} do not match the expected template.\n"
        "----- EXPECTED -----\n"
        f"{expected_content!r}\n"
        "----- FOUND -----\n"
        f"{actual_content!r}\n"
        "--------------------"
    )


def test_markdown_source_files_exist():
    """
    README.md and CHANGELOG.md should already be present in /home/user/project.
    Only their existence is verified; actual contents do not matter for this test.
    """
    for filename in ("README.md", "CHANGELOG.md"):
        path = PROJECT_ROOT / filename
        assert path.exists(), f"Expected {path} to exist, but it is missing."
        assert path.is_file(), f"Expected {path} to be a file, but it is not."