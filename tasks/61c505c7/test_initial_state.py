# test_initial_state.py
#
# This test-suite verifies the *initial* state of the filesystem for the
# “Nginx access-log reporting” kata **before** the student starts working.
#
# Expectations
# ------------
# 1. The raw access log is present and readable at
#        /home/user/projects/website/logs/access.log
# 2. Every log entry is for the date “15/Aug/2023”.
# 3. The reports output files *do not* exist yet:
#        /home/user/projects/website/reports/status_per_hour.csv
#        /home/user/projects/website/reports/top5_endpoints.txt
#        /home/user/projects/website/reports/aug15_summary.tar.gz
#    (The directory /home/user/projects/website/reports itself may or may not
#     exist – both situations are acceptable as long as the files above are
#     absent.)
#
# Only stdlib + pytest are used.

import os
import re
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Helpers & constants
# --------------------------------------------------------------------------- #
PROJECT_ROOT = Path("/home/user/projects/website")
LOG_FILE     = PROJECT_ROOT / "logs" / "access.log"
REPORT_DIR   = PROJECT_ROOT / "reports"

STATUS_CSV   = REPORT_DIR / "status_per_hour.csv"
TOP5_TXT     = REPORT_DIR / "top5_endpoints.txt"
TARBALL      = REPORT_DIR / "aug15_summary.tar.gz"

_DATE_RE = re.compile(r"\[15/Aug/2023:")

# Very light Nginx log line structure (remote_ip … "METHOD PATH HTTP" status …)
_LOG_RE = re.compile(
    r"""
    ^\d{1,3}(?:\.\d{1,3}){3}\s+-\s+-\s+          # remote address + - -
    \[15/Aug/2023:\d{2}:\d{2}:\d{2}\s+[+\-]\d{4}] # timestamp (fixed date)
    \s+"[A-Z]+\s+\S+\s+HTTP/[\d.]+"\s+            # request line
    \d{3}\s+\d+\s+"[^"]*"\s+"[^"]*"$              # status, size, ref, agent
    """,
    re.VERBOSE,
)

# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_access_log_exists_and_readable():
    """The raw access log must exist, be a regular file and not be empty."""
    assert LOG_FILE.exists(), (
        f"Expected log file '{LOG_FILE}' to exist but it is missing."
    )
    assert LOG_FILE.is_file(), (
        f"'{LOG_FILE}' exists but is not a regular file."
    )
    size = LOG_FILE.stat().st_size
    assert size > 0, f"Log file '{LOG_FILE}' is empty (size == 0)."


def test_access_log_only_contains_15_aug_2023_lines():
    """
    Every line in the log must
      1. Contain the literal '[15/Aug/2023:' (date check)
      2. Match a minimal Nginx combined-log regex (format sanity)
    """
    bad_date_lines   = []
    bad_format_lines = []

    with LOG_FILE.open("rt", encoding="utf-8", errors="replace") as fh:
        for lineno, line in enumerate(fh, 1):
            stripped = line.rstrip("\n")
            if not _DATE_RE.search(stripped):
                bad_date_lines.append((lineno, stripped))
            elif not _LOG_RE.match(stripped):
                bad_format_lines.append((lineno, stripped))

    assert not bad_date_lines, (
        "The following lines are *not* dated 15/Aug/2023:\n"
        + "\n".join(f"  line {n}: {txt}" for n, txt in bad_date_lines)
    )
    assert not bad_format_lines, (
        "The following lines do not match the expected Nginx log format:\n"
        + "\n".join(f"  line {n}: {txt}" for n, txt in bad_format_lines)
    )


@pytest.mark.parametrize(
    "path",
    [STATUS_CSV, TOP5_TXT, TARBALL],
    ids=["status_per_hour.csv", "top5_endpoints.txt", "aug15_summary.tar.gz"],
)
def test_output_files_do_not_exist_yet(path: Path):
    """
    None of the expected result artefacts should be present before the student
    starts working.
    """
    assert not path.exists(), (
        f"Output file '{path}' already exists – the workspace is not in the "
        f"required clean initial state."
    )


def test_report_directory_state():
    """
    The reports/ directory may or may not exist yet.
    • If it does *not* exist – that is acceptable (creation is part of the task).
    • If it *does* exist, it must *not* already contain any of the output
      artefacts. Other unrelated files are disallowed as they could interfere
      with grading.
    """
    if not REPORT_DIR.exists():
        # Directory absent – nothing more to check.
        return

    assert REPORT_DIR.is_dir(), (
        f"'{REPORT_DIR}' exists but is not a directory."
    )

    # Collect all entries except the three artefacts we explicitly allow to be
    # absent (they were checked above).
    unexpected_entries = [
        p.name for p in REPORT_DIR.iterdir()
        if p.name not in {STATUS_CSV.name, TOP5_TXT.name, TARBALL.name}
    ]

    assert not unexpected_entries, (
        "The reports directory contains unexpected pre-existing files or "
        "sub-directories:\n  "
        + "\n  ".join(unexpected_entries)
    )