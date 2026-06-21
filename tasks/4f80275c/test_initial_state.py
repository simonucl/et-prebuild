# test_initial_state.py
#
# Pytest suite that validates the starting state of the filesystem
# BEFORE the student performs the FinOps reporting task.

import os
from pathlib import Path

CLOUD_DIR = Path("/home/user/cloud_logs")
JAN_CSV = CLOUD_DIR / "usage_jan.csv"
FEB_CSV = CLOUD_DIR / "usage_feb.csv"

REPORT_DIR = Path("/home/user/finops_report")
SUMMARY_LOG = REPORT_DIR / "summary.log"

JAN_EXPECTED = (
    "date,service,resource,cost\n"
    "2023-01-05,Compute,vm-1,10.50\n"
    "2023-01-10,Storage,s3-bucket-1,2.75\n"
    "2023-01-15,Compute,vm-2,7.25\n"
)

FEB_EXPECTED = (
    "date,service,resource,cost\n"
    "2023-02-03,Compute,vm-1,9.00\n"
    "2023-02-08,Storage,s3-bucket-1,2.75\n"
)

def _read_text(path: Path) -> str:
    """Return the full text of a file using universal newlines."""
    with path.open("r", encoding="utf-8", newline=None) as fh:
        return fh.read()

def test_cloud_logs_directory_exists():
    assert CLOUD_DIR.is_dir(), f"Required directory {CLOUD_DIR} is missing."

def test_jan_csv_exists_and_contents():
    assert JAN_CSV.is_file(), f"CSV file {JAN_CSV} is missing."
    content = _read_text(JAN_CSV)
    assert content == JAN_EXPECTED, (
        f"Unexpected contents in {JAN_CSV}.\n"
        "Expected:\n"
        f"{JAN_EXPECTED!r}\nGot:\n{content!r}"
    )

def test_feb_csv_exists_and_contents():
    assert FEB_CSV.is_file(), f"CSV file {FEB_CSV} is missing."
    content = _read_text(FEB_CSV)
    assert content == FEB_EXPECTED, (
        f"Unexpected contents in {FEB_CSV}.\n"
        "Expected:\n"
        f"{FEB_EXPECTED!r}\nGot:\n{content!r}"
    )

def test_finops_report_not_present_yet():
    assert not REPORT_DIR.exists(), (
        f"Directory {REPORT_DIR} should NOT exist before the task is started."
    )
    # If for some reason the directory exists, also check the file.
    if REPORT_DIR.exists():
        assert not SUMMARY_LOG.exists(), (
            f"{SUMMARY_LOG} should NOT exist before the task is started."
        )