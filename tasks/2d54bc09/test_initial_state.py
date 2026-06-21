# test_initial_state.py
#
# This test-suite validates that the expected **initial** filesystem state
# is present before the student runs any commands or creates output files.
#
# It checks:
#   1. The /home/user/logs directory exists.
#   2. The three required log files exist.
#   3. Each log file’s contents exactly match the canonical “ground-truth”
#      provided in the task description.
#
# NOTE:  • We purposefully do *not* test for /home/user/debug or any files
#          the student is asked to create later.
#        • Only the Python standard library + pytest are used.

from pathlib import Path
import pytest

HOME = Path("/home/user")
LOG_DIR = HOME / "logs"

# Ground-truth file contents including the terminating newline character
EXPECTED_CONTENTS = {
    "auth.log": (
        "2023-08-01 12:00:00 INFO  Starting service\n"
        "2023-08-01 12:01:00 ERROR Failed to connect to DB\n"
        "2023-08-01 12:02:00 INFO  Retrying\n"
        "2023-08-01 12:03:00 ERROR Timeout reached\n"
    ),
    "billing.log": (
        "2023-08-01 12:00:00 INFO  Starting service\n"
        "2023-08-01 12:05:00 ERROR Payment gateway unreachable\n"
        "2023-08-01 12:06:00 INFO  Circuit breaker open\n"
    ),
    "inventory.log": (
        "2023-08-01 12:00:00 INFO  Starting service\n"
        "2023-08-01 12:04:00 INFO  Inventory synced\n"
    ),
}


def _read_file(path: Path) -> str:
    """Helper that returns the full text of a file or raises a detailed error."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        pytest.fail(f"Expected file is missing: {path}")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read file {path}: {exc}")


def test_log_directory_exists():
    assert LOG_DIR.is_dir(), f"Required directory is missing: {LOG_DIR}"


@pytest.mark.parametrize("filename", sorted(EXPECTED_CONTENTS))
def test_log_file_exists(filename):
    path = LOG_DIR / filename
    assert path.is_file(), f"Required log file is missing: {path}"


@pytest.mark.parametrize("filename, expected", EXPECTED_CONTENTS.items())
def test_log_file_contents_exact_match(filename, expected):
    """
    Ensure every log file contains *exactly* the expected text, including
    newlines, spacing, and order.  Any deviation indicates the initial
    environment is not as described in the task.
    """
    path = LOG_DIR / filename
    actual = _read_file(path)

    assert (  # explain differences clearly if they exist
        actual == expected
    ), (
        f"Contents of {path} do not match the expected ground-truth.\n"
        "---- Expected ----\n"
        f"{expected}\n"
        "---- Actual ----\n"
        f"{actual}"
    )