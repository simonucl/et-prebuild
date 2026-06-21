# test_initial_state.py
#
# Pytest suite that verifies the pristine filesystem / OS state **before**
# the student generates any reports.  The checks cover:
#   • existence of the expected source directories and log files
#   • absence of the yet-to-be-produced report files
#   • basic sanity of every supplied *.log file so that the student
#     can safely parse them later on
#
# Only the Python standard library and pytest are used.

import re
from pathlib import Path

import pytest

# Absolute base paths (as per task description)
LOG_DIR = Path("/home/user/mobile_ci/logs")
REPORT_DIR = Path("/home/user/mobile_ci/reports")

# The four log files that must already be present
EXPECTED_LOG_FILES = {
    LOG_DIR / "build_2023-08-01_c1345.log",
    LOG_DIR / "build_2023-08-02_c1346.log",
    LOG_DIR / "build_2023-08-03_c1347.log",
    LOG_DIR / "build_2023-08-04_c1348.log",
}

# Report files that must **not** exist yet
SUMMARY_FILE = (
    REPORT_DIR / "weekly_summary_2023-08-01_to_2023-08-07.log"
)
PARSE_DETAIL_FILE = REPORT_DIR / "parse_detail.log"


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
START_BUILD_RE = re.compile(r"^\[INFO] Start build: (?P<id>\S+)")
FINAL_STATUS_RE = re.compile(
    r"^\[INFO] Build finished with status: (?P<status>SUCCESS|FAILURE)"
)
DURATION_RE = re.compile(r"^Duration:\s*(?P<ms>\d+)ms")


def _read_lines(path: Path):
    """Return the stripped lines of a text file."""
    return [ln.rstrip("\n") for ln in path.read_text(encoding="utf-8").splitlines()]


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_logs_directory_exists():
    assert LOG_DIR.is_dir(), (
        f"Required directory {LOG_DIR} is missing or not a directory."
    )


def test_reports_directory_exists_and_empty():
    assert REPORT_DIR.is_dir(), (
        f"Required directory {REPORT_DIR} is missing or not a directory."
    )
    # It should be completely empty before the student runs any commands.
    # (Hidden OS files starting with '.' are ignored.)
    existing = [p for p in REPORT_DIR.iterdir() if not p.name.startswith(".")]
    assert (
        not existing
    ), f"{REPORT_DIR} should be empty initially, but contains: {', '.join(p.name for p in existing)}"


def test_expected_log_files_present():
    missing = [str(p) for p in EXPECTED_LOG_FILES if not p.is_file()]
    assert not missing, (
        "These expected log files are missing:\n  " + "\n  ".join(missing)
    )


def test_no_extra_log_files_present():
    present_logs = {p for p in LOG_DIR.glob("*.log")}
    extras = present_logs - EXPECTED_LOG_FILES
    assert (
        not extras
    ), f"Unexpected *.log files found in {LOG_DIR}: {', '.join(p.name for p in extras)}"


@pytest.mark.parametrize("log_path", sorted(EXPECTED_LOG_FILES))
def test_each_log_file_has_required_structure(log_path: Path):
    """
    Every supplied build log must contain the key lines needed
    for later parsing:
      • Start build: <id>
      • Build finished with status: SUCCESS|FAILURE
      • Duration: <number>ms
    """
    lines = _read_lines(log_path)

    # Check 'Start build'
    assert any(START_BUILD_RE.match(ln) for ln in lines), (
        f"{log_path} lacks a valid 'Start build:' line."
    )

    # Check 'Build finished with status'
    assert any(FINAL_STATUS_RE.match(ln) for ln in lines), (
        f"{log_path} lacks a valid 'Build finished with status:' line."
    )

    # Check 'Duration'
    assert any(DURATION_RE.match(ln) for ln in lines), (
        f"{log_path} lacks a valid 'Duration:' line."
    )


def test_report_files_do_not_exist_yet():
    for path in (SUMMARY_FILE, PARSE_DETAIL_FILE):
        assert not path.exists(), (
            f"Report file {path} should NOT exist before the student runs the solution."
        )