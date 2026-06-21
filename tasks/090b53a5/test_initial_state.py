# test_initial_state.py
#
# Pytest suite that verifies the *starting* state of the operating-system
# filesystem for the “legacy uptime” exercise _before_ the student does any work.
#
# The checks ensure that:
#   • All required legacy assets are present and in the right state.
#   • No deliverable artifacts (logs, summaries) exist yet.
#
# Only Python’s standard library and pytest are used.

import os
import stat
import subprocess
from pathlib import Path
import pytest

HOME = Path("/home/user")
LEGACY_DIR = HOME / "legacy_tools"
LOGS_DIR = HOME / "logs"

LEGACY_SCRIPT = LEGACY_DIR / "legacy_uptime_checker.sh"
MOCK_DATA = LEGACY_DIR / "mock_ping_results.dat"
HOSTS_TXT = LEGACY_DIR / "hosts.txt"

EXPECTED_RAW_LINES = [
    "web01: UP",
    "web02: DOWN",
    "db01: UP",
    "cache01: DOWN",
]


def _is_executable(path: Path) -> bool:
    """Return True if 'path' exists, is a file and is executable by the owner."""
    if not path.is_file():
        return False
    st_mode = path.stat().st_mode
    return bool(st_mode & stat.S_IXUSR)


def test_legacy_directory_exists():
    assert LEGACY_DIR.is_dir(), (
        f"Required directory {LEGACY_DIR} is missing.\n"
        "It should have been pre-provisioned with legacy tools."
    )


@pytest.mark.parametrize(
    "file_path",
    [
        pytest.param(LEGACY_SCRIPT, id="legacy_uptime_checker.sh"),
        pytest.param(MOCK_DATA, id="mock_ping_results.dat"),
        pytest.param(HOSTS_TXT, id="hosts.txt"),
    ],
)
def test_legacy_files_exist(file_path: Path):
    assert file_path.is_file(), f"Expected file {file_path} does not exist."


def test_legacy_script_is_executable():
    assert _is_executable(LEGACY_SCRIPT), (
        f"{LEGACY_SCRIPT} must be executable (mode +x) but is not."
    )


def test_legacy_script_output_is_as_expected():
    """
    Run the legacy script and make sure the raw console output is _exactly_
    the four lines that later have to be archived.  This protects against
    accidental edits to the script or its data file.
    """
    completed = subprocess.run(
        [str(LEGACY_SCRIPT)],
        cwd=str(LEGACY_DIR),
        text=True,
        capture_output=True,
        check=True,
    )

    # Strip the trailing newline to get clean line splitting.
    actual_lines = completed.stdout.rstrip("\n").split("\n")
    assert actual_lines == EXPECTED_RAW_LINES, (
        "The legacy script’s current output differs from what the exercise "
        "expects.\n"
        f"Expected lines:\n{EXPECTED_RAW_LINES}\n"
        f"Actual lines:\n{actual_lines}"
    )
    # The script should *not* emit anything on stderr.
    assert completed.stderr == "", (
        "The legacy script unexpectedly wrote to stderr:\n" + completed.stderr
    )


def test_logs_directory_does_not_yet_exist():
    """
    Students are told the /home/user/logs directory should _not_ exist before
    they run their solution.  Make sure that is indeed the case so the test
    suite confirms the starting state.
    """
    assert not LOGS_DIR.exists(), (
        f"{LOGS_DIR} already exists, but it should be created by the student’s "
        "solution, not beforehand."
    )


def test_no_deliverable_log_files_yet():
    """Ensure that the two deliverable files are absent at the start."""
    for fname in ("uptime_latest.log", "summary_latest.log"):
        target = LOGS_DIR / fname
        assert not target.exists(), (
            f"Found {target} already present. It must not exist before the "
            "student runs their commands."
        )