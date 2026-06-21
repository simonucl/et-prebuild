# test_initial_state.py
#
# Pytest suite that validates the filesystem state *before* the student
# performs any actions for the “web-analytics” task.  It confirms that the
# expected raw CSV file exists with the exact contents specified, and **does
# not** inspect or mention any of the files or directories the student is
# supposed to create later.

import os
import pytest

RAW_DIR = "/home/user/projects/web_analytics/raw"
RAW_CSV = os.path.join(RAW_DIR, "analytics_2023-10-15.csv")

EXPECTED_CSV_CONTENT = (
    "Date,PageViews,UniqueVisitors,BounceRate,AvgTimeOnPage\n"
    "2023-10-10,1450,675,0.42,00:03:21\n"
    "2023-10-11,1320,598,0.38,00:03:10\n"
    "2023-10-12,1703,840,0.41,00:03:45\n"
    "2023-10-13,1250,560,0.40,00:03:05\n"
    "2023-10-14,1800,910,0.39,00:03:50\n"
)


def test_raw_directory_exists():
    """
    The raw data directory must already exist.
    """
    assert os.path.isdir(
        RAW_DIR
    ), f"Required directory missing: {RAW_DIR!r}"


def test_raw_csv_exists():
    """
    The initial CSV report must already be present at the exact location.
    """
    assert os.path.isfile(
        RAW_CSV
    ), f"Required file missing: {RAW_CSV!r}"


def test_raw_csv_contents_are_exact():
    """
    The contents of the initial CSV must match exactly, including newlines.
    """
    with open(RAW_CSV, encoding="utf-8") as fp:
        actual = fp.read()

    assert (
        actual == EXPECTED_CSV_CONTENT
    ), (
        "Contents of the initial CSV file do not match the expected "
        "template.\n\nExpected:\n"
        f"{EXPECTED_CSV_CONTENT!r}\n\nGot:\n{actual!r}"
    )