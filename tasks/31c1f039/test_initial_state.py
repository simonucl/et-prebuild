# test_initial_state.py
# ============================================================
# Pytest suite to validate the *initial* state of the sandbox
# before the student performs any actions.
#
# Validates that the pre-existing runtime log is present with
# the exact expected permissions and contents.
#
# IMPORTANT:  Per the grading harness requirements we DO NOT
#             check for the presence (or absence) of any of
#             the output artefacts the student is expected to
#             create (e.g. /home/user/support or anything
#             within it).
# ============================================================

import os
import stat
import pytest

# Constants describing the canonical initial state
LOG_PATH = "/home/user/app/logs/runtime.log"
EXPECTED_LINES = [
    "System initialized successfully\n",
    "Connection pool ready\n",
    "Listening on port 8080\n",
]
EXPECTED_PERMS = 0o644  # rw-r--r--

@pytest.fixture(scope="module")
def log_stat():
    """
    Fixture that returns os.stat_result for the runtime log.
    Fails early if the file does not exist.
    """
    if not os.path.isfile(LOG_PATH):
        pytest.fail(
            f"Required log file missing: {LOG_PATH!r}. "
            "It must exist before the student begins the task."
        )
    return os.stat(LOG_PATH, follow_symlinks=True)


def test_log_path_is_file(log_stat):
    """Verify that the runtime log exists and is a regular file."""
    assert stat.S_ISREG(log_stat.st_mode), (
        f"{LOG_PATH!r} exists but is not a regular file."
    )


def test_log_permissions(log_stat):
    """Verify the runtime log has the expected 0644 permissions."""
    perms = stat.S_IMODE(log_stat.st_mode)
    assert perms == EXPECTED_PERMS, (
        f"{LOG_PATH!r} has permissions {oct(perms)}, "
        f"expected {oct(EXPECTED_PERMS)} (rw-r--r--)."
    )


def test_log_contents_exact():
    """Verify that the runtime log has exactly the expected three lines."""
    try:
        with open(LOG_PATH, "r", encoding="utf-8") as fh:
            contents = fh.readlines()
    except Exception as exc:
        pytest.fail(f"Could not read {LOG_PATH!r}: {exc}")

    assert contents == EXPECTED_LINES, (
        f"{LOG_PATH!r} does not contain the expected lines.\n"
        "Expected:\n"
        + "".join(EXPECTED_LINES)
        + "Found:\n"
        + "".join(contents)
    )