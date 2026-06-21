# test_initial_state.py
"""
Pytest suite that verifies the machine’s *initial* state before the
student script runs.

RULES FOR THESE TESTS
---------------------
1. Only validate resources that **must already exist**.
2. NEVER look for, or refer to, any artefacts that the student is
   supposed to create later (reports, summaries, etc.).
3. Failures must provide a clear, actionable explanation so the student
   immediately knows what prerequisite is missing or malformed.
"""

import os
import stat
import re
from pathlib import Path

# ---------------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------------

HOME = Path("/home/user")
LOG_DIR = HOME / "logs"
WEBSERVER_DIR = LOG_DIR / "webserver"
ACCESS_LOG = WEBSERVER_DIR / "access.log"

# Reference patterns we expect to find at least once in the log.  These help
# guarantee the data is sufficiently rich for later tasks while keeping the
# tests robust.
ADMIN_PATH_REGEX = re.compile(r'"\w+\s+/admin[^"]*\s+HTTP/', re.IGNORECASE)
STATUS_5XX_REGEX = re.compile(r'"\s5\d{2}\s')  # space 5xx space


# ---------------------------------------------------------------------------
# TESTS
# ---------------------------------------------------------------------------

def test_log_directories_exist_with_correct_permissions():
    """Both /home/user/logs and /home/user/logs/webserver must exist (mode 755)."""
    for directory in (LOG_DIR, WEBSERVER_DIR):
        assert directory.is_dir(), (
            f"Required directory '{directory}' is missing. "
            "Create it with mode 755."
        )
        mode = stat.S_IMODE(directory.stat().st_mode)
        assert mode == 0o755, (
            f"Directory '{directory}' must have permissions 755 "
            f"(currently {oct(mode)})."
        )


def test_access_log_exists_and_is_readable():
    """The raw web-server access log must be present and world-readable (mode 644)."""
    assert ACCESS_LOG.is_file(), (
        f"Expected log file '{ACCESS_LOG}' does not exist."
    )
    mode = stat.S_IMODE(ACCESS_LOG.stat().st_mode)
    assert mode == 0o644, (
        f"Log file '{ACCESS_LOG}' must have permissions 644 "
        f"(currently {oct(mode)})."
    )


def test_access_log_contains_expected_number_of_entries():
    """
    The log must contain exactly 10 lines as per the specification so the
    subsequent policy checks have deterministic data to process.
    """
    with ACCESS_LOG.open("r", encoding="utf-8") as fh:
        lines = fh.readlines()

    assert len(lines) == 10, (
        f"Access log is expected to have 10 entries, found {len(lines)}."
    )


def test_access_log_has_admin_and_5xx_samples():
    """
    For the assignment to be meaningful, the log must include:
    * at least one request to an /admin* path
    * at least one request whose HTTP status is in the 5xx range
    """
    with ACCESS_LOG.open("r", encoding="utf-8") as fh:
        content = fh.read()

    assert ADMIN_PATH_REGEX.search(content), (
        "The access log must contain at least one request whose path starts "
        "with '/admin' so Policy P-2 can be exercised."
    )

    assert STATUS_5XX_REGEX.search(content), (
        "The access log must contain at least one request returning an HTTP "
        "status in the 5xx range so Policy P-1 can be exercised."
    )