# test_initial_state.py
#
# This test-suite validates the filesystem **before** the student’s
# solution runs.  It confirms that the source data are present and
# correct, and that no deliverables have been created yet.

import pathlib
import stat
import pytest

# ---------------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------------

HOME            = pathlib.Path("/home/user")
DATA_DIR        = HOME / "data"
OUTPUT_DIR      = HOME / "output"
CSV_PATH        = DATA_DIR / "service_incidents.log"

INCIDENT_HEADER = "id,timestamp,service,host,severity,message"

EXPECTED_LINES = [
    "id,timestamp,service,host,severity,message",
    "1001,2023-08-14T10:15:32Z,auth-api,auth01,CRITICAL,Authentication failure rate above threshold",
    "1002,2023-08-14T10:17:05Z,billing-api,billing02,WARNING,Slow response time detected",
    "1003,2023-08-14T10:18:44Z,auth-api,auth02,CRITICAL,Multiple 5xx errors observed",
    "1004,2023-08-14T10:22:11Z,search-api,search01,INFO,Zero-downtime deployment completed",
    "1005,2023-08-14T10:25:53Z,billing-api,billing01,CRITICAL,Database connection pool exhausted",
    "1006,2023-08-14T10:27:19Z,auth-api,auth03,WARNING,Increased latency",
    "1007,2023-08-14T10:30:07Z,search-api,search02,CRITICAL,Out of memory killed process",
    "1008,2023-08-14T10:35:41Z,user-service,user01,INFO,Refresh tokens rotated",
    "1009,2023-08-14T10:38:00Z,billing-api,billing03,CRITICAL,Payment gateway timeout",
    "1010,2023-08-14T10:40:24Z,user-service,user02,WARNING,Cache miss rate increased",
]

# ---------------------------------------------------------------------------
# TESTS
# ---------------------------------------------------------------------------

def test_data_directory_exists_and_has_correct_permissions():
    assert DATA_DIR.exists(), f"Required directory {DATA_DIR} is missing."
    assert DATA_DIR.is_dir(), f"{DATA_DIR} exists but is not a directory."
    mode = DATA_DIR.stat().st_mode
    # directory bit and 0755 perms
    assert stat.S_IMODE(mode) & 0o777 == 0o755, (
        f"{DATA_DIR} should have permissions 0755, "
        f"found {oct(stat.S_IMODE(mode))}"
    )

def test_csv_file_exists_and_content_exact():
    assert CSV_PATH.exists(), f"Required file {CSV_PATH} is missing."
    assert CSV_PATH.is_file(), f"{CSV_PATH} exists but is not a regular file."

    with CSV_PATH.open("r", encoding="utf-8") as fh:
        lines = [ln.rstrip("\n") for ln in fh]

    assert len(lines) == 11, (
        f"{CSV_PATH} should have exactly 11 lines "
        f"(1 header + 10 data), found {len(lines)}."
    )

    for idx, (got, expected) in enumerate(zip(lines, EXPECTED_LINES), start=1):
        assert got == expected, (
            f"Line {idx} of {CSV_PATH!s} is incorrect.\n"
            f"Expected: {expected}\n"
            f"Got     : {got}"
        )

    # Validate column count (6 columns, comma-separated) for every line
    for idx, line in enumerate(lines, start=1):
        cols = line.split(",")
        assert len(cols) == 6, (
            f"Line {idx} of {CSV_PATH} does not have 6 comma-separated columns "
            f"(found {len(cols)}). Line content: {line}"
        )

def test_output_directory_does_not_yet_exist():
    assert not OUTPUT_DIR.exists(), (
        f"The output directory {OUTPUT_DIR} should NOT exist before the "
        "student runs their solution, but it does."
    )

def test_no_deliverable_files_exist():
    summary_tsv   = OUTPUT_DIR / "incident_summary.tsv"
    critical_txt  = OUTPUT_DIR / "critical_services.txt"
    audit_log     = OUTPUT_DIR / "triage_audit.log"

    for path in (summary_tsv, critical_txt, audit_log):
        assert not path.exists(), (
            f"Deliverable file {path} should NOT exist before the student "
            "executes their commands."
        )