# test_initial_state.py
#
# This pytest suite validates the _initial_ operating-system / filesystem
# state for the “Network Diagnostics Bundle” exercise **before** the student
# performs any actions.  The checks here must all pass _as delivered_ by the
# exercise author; if any fail, the environment itself is broken, not the
# student’s solution.
#
# Requirements verified:
#   • /home/user/repositories   — directory, mode 755
#   • /home/user/repositories/targets.list
#       – regular file, mode 644
#       – exactly three non-blank, non-comment lines
#       – lines (in order):  repo-alpha, repo-beta, repo-gamma — all 127.0.0.1
#       – file ends with a newline
#   • /home/user/artifacts      — directory, mode 755 and EMPTY
#   • No diagnostic-output files are present yet
#
# Only the Python stdlib and pytest are used, per specification.

import os
import stat
from pathlib import Path

import pytest

HOME = Path("/home/user")
REPO_DIR = HOME / "repositories"
TARGETS_FILE = REPO_DIR / "targets.list"
ARTIFACTS_DIR = HOME / "artifacts"
EXPECTED_LINES = [
    "repo-alpha 127.0.0.1",
    "repo-beta 127.0.0.1",
    "repo-gamma 127.0.0.1",
]


def _assert_mode(path: Path, expected_octal: int):
    """
    Assert that the filesystem object's permission bits (not including
    the file-type bits) exactly match expected_octal.
    """
    st_mode = path.stat().st_mode
    actual_perms = stat.S_IMODE(st_mode)
    assert actual_perms == expected_octal, (
        f"{path} has mode {oct(actual_perms)}; expected {oct(expected_octal)}"
    )


def test_repository_directory_exists_and_mode():
    assert REPO_DIR.exists(), f"Required directory {REPO_DIR} is missing."
    assert REPO_DIR.is_dir(), f"{REPO_DIR} exists but is not a directory."
    _assert_mode(REPO_DIR, 0o755)


def test_targets_list_exists_and_mode():
    assert TARGETS_FILE.exists(), f"Required file {TARGETS_FILE} is missing."
    assert TARGETS_FILE.is_file(), f"{TARGETS_FILE} exists but is not a regular file."
    _assert_mode(TARGETS_FILE, 0o644)


def test_targets_list_content_exact():
    content = TARGETS_FILE.read_text(encoding="utf-8")
    assert content.endswith(
        "\n"
    ), f"{TARGETS_FILE} must terminate with a newline character."

    # Collect non-blank, non-comment lines
    usable_lines = [
        line.strip() for line in content.splitlines() if line.strip() and not line.lstrip().startswith("#")
    ]

    assert (
        usable_lines == EXPECTED_LINES
    ), (
        f"{TARGETS_FILE} content mismatch.\n"
        f"Expected lines:\n  {EXPECTED_LINES}\n"
        f"Actual lines:\n  {usable_lines}"
    )


def test_artifacts_directory_exists_and_empty():
    assert ARTIFACTS_DIR.exists(), f"Required directory {ARTIFACTS_DIR} is missing."
    assert ARTIFACTS_DIR.is_dir(), f"{ARTIFACTS_DIR} exists but is not a directory."
    _assert_mode(ARTIFACTS_DIR, 0o755)

    entries = [p for p in ARTIFACTS_DIR.iterdir()]
    assert (
        not entries
    ), f"{ARTIFACTS_DIR} is expected to be empty initially, but contains: {[e.name for e in entries]}"


@pytest.mark.parametrize(
    "unexpected_path",
    [
        ARTIFACTS_DIR / "net_diagnostics_aggregated.log",
        ARTIFACTS_DIR / "README.md",
    ],
)
def test_no_output_files_yet(unexpected_path: Path):
    assert (
        not unexpected_path.exists()
    ), f"Output file {unexpected_path} should not exist before the student runs their solution."