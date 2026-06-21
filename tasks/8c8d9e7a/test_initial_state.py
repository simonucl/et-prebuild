# test_initial_state.py
#
# This test-suite verifies the *initial* state of the operating system /
# filesystem **before** the student starts working.
#
# What we check:
#   1. The three expected log-files are present under /home/user/backup_logs/.
#   2. Their content conforms to the required “START … / END …” specification.
#   3. The destination directory /home/user/restore_reports/ and its expected
#      artefacts do *not* exist yet.
#
# If any of these assertions fails the accompanying error-message will point
# precisely at what is missing or malformed so that the student can fix the
# environment before implementing the actual task.
#
# Only Python’s stdlib and pytest are used, as required.

import re
from pathlib import Path

import pytest

HOME = Path("/home/user")
BACKUP_DIR = HOME / "backup_logs"
RESTORE_DIR = HOME / "restore_reports"

LOG_FILES = [
    BACKUP_DIR / "restore_20240601.log",
    BACKUP_DIR / "restore_20240602.log",
    BACKUP_DIR / "restore_20240603.log",
]

# ---------------------------------------------------------------------------
# Generic, compiled regular expressions for line validation
# ---------------------------------------------------------------------------

# Example:
# 2024-06-01 00:00:01 START /srv/data size=15728640
START_RE = re.compile(
    r"""
    ^
    (?P<ts>\d{4}-\d{2}-\d{2}\ \d{2}:\d{2}:\d{2})   # timestamp
    \s+
    START
    \s+
    (?P<path>/\S+)
    \s+
    size=(?P<size>\d+)
    $
    """,
    re.VERBOSE,
)

# Example:
# 2024-06-01 00:05:02 END   /srv/data duration=301s status=SUCCESS
# 2024-06-01 01:30:31 END   /srv/media duration=1231s status=FAILURE code=E42
END_RE = re.compile(
    r"""
    ^
    (?P<ts>\d{4}-\d{2}-\d{2}\ \d{2}:\d{2}:\d{2})   # timestamp
    \s+
    END
    \s+
    (?P<path>/\S+)
    \s+
    duration=(?P<duration>\d+)s
    \s+
    status=(?P<status>SUCCESS|FAILURE)
    (?:
        \s+
        code=(?P<code>\w+)
    )?
    $
    """,
    re.VERBOSE,
)


# ---------------------------------------------------------------------------
# Tests regarding the presence / absence of directories and files
# ---------------------------------------------------------------------------


def test_backup_logs_directory_exists():
    assert BACKUP_DIR.is_dir(), (
        f"Required directory {BACKUP_DIR} is missing. "
        "The three log files must live here."
    )


@pytest.mark.parametrize("log_path", LOG_FILES, ids=[p.name for p in LOG_FILES])
def test_each_log_file_exists(log_path: Path):
    assert log_path.is_file(), f"Expected log file {log_path} is missing."


def test_no_restore_reports_directory_yet():
    assert not RESTORE_DIR.exists(), (
        f"{RESTORE_DIR} should NOT exist before the student runs the solution."
    )
    # Even if the directory is absent, double-check the individual files
    summary = RESTORE_DIR / "restore_summary.csv"
    failed  = RESTORE_DIR / "failed_restore_log.txt"
    assert not summary.exists(), f"{summary} should not be present yet."
    assert not failed.exists(), f"{failed} should not be present yet."


# ---------------------------------------------------------------------------
# Tests validating the *content* of each log file
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("log_path", LOG_FILES, ids=[p.name for p in LOG_FILES])
def test_log_file_format_is_valid(log_path: Path):
    """
    Validates that every log file

      * has an even number of lines,
      * alternates strictly START / END,
      * each START / END line follows the documented pattern,
      * each START has a matching END with the **same path**,
      * END lines with status=FAILURE always have a code=… field,
        and those with status=SUCCESS never have one.
    """

    lines = [ln.rstrip("\n") for ln in log_path.read_text().splitlines() if ln.strip()]

    assert lines, f"{log_path} is empty."
    assert len(lines) % 2 == 0, (
        f"{log_path} must contain an even number of lines: "
        "one START line + one END line per transaction."
    )

    for idx in range(0, len(lines), 2):
        start_line = lines[idx]
        end_line = lines[idx + 1]

        # Validate START line
        m_start = START_RE.match(start_line)
        assert m_start, (
            f"Malformed START line in {log_path} (line {idx + 1}):\n{start_line}"
        )
        start_path = m_start.group("path")

        # Validate END line
        m_end = END_RE.match(end_line)
        assert m_end, (
            f"Malformed END line in {log_path} (line {idx + 2}):\n{end_line}"
        )
        end_path = m_end.group("path")
        status = m_end.group("status")
        code   = m_end.group("code")

        # START and END must reference the same path
        assert (
            start_path == end_path
        ), f"START/END path mismatch in {log_path}: {start_path!r} vs {end_path!r}"

        # If status is FAILURE, an error code *must* be present; otherwise must be absent
        if status == "FAILURE":
            assert code, (
                f"END line in {log_path} (line {idx + 2}) has status=FAILURE "
                "but no error code."
            )
        else:  # SUCCESS
            assert code is None, (
                f"END line in {log_path} (line {idx + 2}) has status=SUCCESS "
                "but unexpectedly contains an error code."
            )