# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state for the “quick static security sweep” exercise.
#
# IMPORTANT:  These tests assert that the environment exactly matches the
#             description given in the task **before** the student runs
#             any commands.  If any assertion here fails, the exercise
#             itself is improperly staged.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user").resolve()
WEBAPP_DIR = HOME / "webapp"
SCAN_DIR = HOME / "web_security_scan"
SCAN_LOG = SCAN_DIR / "quick_scan.log"


def _collect_php_occurrences(root: Path):
    """
    Walk ``root`` recursively and yield tuples of
        (relative_path, line_number, matched_literal)
    whenever a line contains the *case-sensitive* string
    'eval(' or 'exec('.
    """
    dangerous = ("eval(", "exec(")
    for path in root.rglob("*.php"):
        rel_path = path.relative_to(root).as_posix()
        with path.open("r", encoding="utf-8", errors="ignore") as fh:
            for ln, line in enumerate(fh, 1):
                for needle in dangerous:
                    if needle in line:
                        yield (rel_path, ln, needle)


def test_webapp_directory_exists():
    assert WEBAPP_DIR.is_dir(), (
        f"Expected directory {WEBAPP_DIR} to exist, "
        "but it is missing."
    )


@pytest.mark.parametrize(
    "relative_path, expected_min_lines",
    [
        ("index.php", 14),
        ("admin/tools.php", 60),
    ],
)
def test_key_php_files_exist_with_minimum_length(relative_path, expected_min_lines):
    target = WEBAPP_DIR / relative_path
    assert target.is_file(), f"Required file {target} is missing."
    # Make sure the file is long enough so that the line numbers tested later
    # are meaningful.
    num_lines = sum(1 for _ in target.open("r", encoding="utf-8", errors="ignore"))
    assert (
        num_lines >= expected_min_lines
    ), f"{target} is expected to have at least {expected_min_lines} lines, but has only {num_lines}."


def test_exact_dangerous_occurrences():
    """
    Verify that the *only* occurrences of the dangerous literals are

        admin/tools.php:45:exec(
        admin/tools.php:60:eval(
        index.php:14:eval(
    """
    found = sorted(_collect_php_occurrences(WEBAPP_DIR))
    expected = sorted(
        [
            ("admin/tools.php", 45, "exec("),
            ("admin/tools.php", 60, "eval("),
            ("index.php", 14, "eval("),
        ]
    )

    assert found == expected, (
        "The set of dangerous occurrences inside /home/user/webapp does "
        "not match the expected ground-truth.\n\n"
        f"Expected ({len(expected)} entries):\n{expected}\n\n"
        f"Found ({len(found)} entries):\n{found}"
    )


def test_scan_artifacts_do_not_exist_yet():
    """
    Before the student performs any action, no scan directory / log must exist.
    """
    assert not SCAN_DIR.exists(), (
        f"{SCAN_DIR} should *not* exist before the student runs the task, "
        "but it is already present."
    )
    assert not SCAN_LOG.exists(), (
        f"{SCAN_LOG} should *not* exist before the student runs the task, "
        "but it is already present."
    )