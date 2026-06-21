# test_initial_state.py
#
# Pytest suite for validating the expected filesystem state **after**
# the student has completed the monitoring-prototype task.
#
# NOTE:
# • Uses only stdlib + pytest.
# • Fails with clear, targeted messages so the student knows exactly
#   what is missing or incorrect.
# • All paths are absolute and must match the specification exactly.

import os
import stat
import pytest

# ---------------------------------------------------------------------------
# Constants 
# ---------------------------------------------------------------------------

HOME = "/home/user"
MONITORING_DIR = os.path.join(HOME, "monitoring")
CONFIG_DIR = os.path.join(MONITORING_DIR, "config")
LOGS_DIR = os.path.join(MONITORING_DIR, "logs")

THRESHOLD_CONF = os.path.join(CONFIG_DIR, "threshold.conf")
CHECK_MEMORY_SH = os.path.join(MONITORING_DIR, "check_memory.sh")
MEMORY_ALERT_LOG = os.path.join(LOGS_DIR, "memory_alert.log")

TEST_ALERT_LINE = (
    "[TEST] [ALERT] Memory usage is 90% (Used: 900MB / Total: 1000MB)"
)

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------


def _is_executable(path: str) -> bool:
    """Return True if the current user can execute `path`."""
    return os.path.isfile(path) and os.access(path, os.X_OK)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_directories_exist():
    """Required directories must exist."""
    for d in (MONITORING_DIR, CONFIG_DIR, LOGS_DIR):
        assert os.path.isdir(
            d
        ), f"Directory {d!r} is missing. Create it exactly as specified."


def test_threshold_conf_content():
    """threshold.conf must exist and contain exactly 'THRESHOLD=75' (with an optional trailing newline)."""
    assert os.path.isfile(
        THRESHOLD_CONF
    ), f"File {THRESHOLD_CONF!r} is missing."

    with open(THRESHOLD_CONF, "r", encoding="utf-8") as fh:
        contents = fh.read()

    # Strip a single trailing newline for comparison, but keep everything else
    stripped = contents.rstrip("\n")

    assert (
        stripped == "THRESHOLD=75"
    ), (
        f"File {THRESHOLD_CONF!r} must contain exactly the single line "
        f'`THRESHOLD=75` (no spaces). Current content: {contents!r}'
    )


def test_check_memory_sh_executable_and_shebang():
    """check_memory.sh must exist, be executable, and have a valid bash shebang."""
    assert os.path.isfile(
        CHECK_MEMORY_SH
    ), f"Script {CHECK_MEMORY_SH!r} is missing."

    assert _is_executable(
        CHECK_MEMORY_SH
    ), f"Script {CHECK_MEMORY_SH!r} is not executable by the current user."

    with open(CHECK_MEMORY_SH, "r", encoding="utf-8") as fh:
        first_line = fh.readline().rstrip("\n")

    assert first_line.startswith("#!"), (
        f"Script {CHECK_MEMORY_SH!r} must start with a shebang line; "
        f"found: {first_line!r}"
    )

    assert "bash" in first_line, (
        f"Shebang of {CHECK_MEMORY_SH!r} must reference bash. "
        f"Found: {first_line!r}"
    )


def test_memory_alert_log_contains_test_line():
    """memory_alert.log must exist and contain at least one exact test alert line."""
    assert os.path.isfile(
        MEMORY_ALERT_LOG
    ), f"Log file {MEMORY_ALERT_LOG!r} is missing."

    with open(MEMORY_ALERT_LOG, "r", encoding="utf-8") as fh:
        lines = [ln.rstrip("\n") for ln in fh]

    assert TEST_ALERT_LINE in lines, (
        f"Log file {MEMORY_ALERT_LOG!r} does not contain the required test "
        f"alert line:\n{TEST_ALERT_LINE}"
    )