# test_initial_state.py
#
# Pytest suite that verifies the operating-system / filesystem **before**
# the student performs the requested maintenance work.
#
# What we assert:
# 1. The CSV data file exists at the exact path given.
# 2. Its contents are **exactly** the ten lines specified in the task
#    (including the presence of a single trailing "\n" on every line).
# 3. The reports directory either does not exist or, if it does, it
#    contains none of the two report files that the student is supposed
#    to create.  This guarantees that the student really has to perform
#    the work and that no leftover artefacts are present.

import os
from pathlib import Path

CSV_PATH = Path("/home/user/projects/mobile-ci/pipeline_runs.csv")
REPORTS_DIR = Path("/home/user/projects/mobile-ci/reports")

EXPECTED_CSV_LINES = [
    "20231015-001;android;main;SUCCESS",
    "20231015-002;android;main;FAILURE",
    "20231015-003;ios;main;SUCCESS",
    "20231015-004;ios;develop;FAILURE",
    "20231015-005;ios;develop;SUCCESS",
    "20231015-006;android;develop;SUCCESS",
    "20231015-007;ios;develop;FAILURE",
    "20231015-008;android;main;SUCCESS",
    "20231015-009;android;main;SUCCESS",
    "20231015-010;ios;develop;FAILURE",
]

EXPECTED_REPORT_FILES = [
    REPORTS_DIR / "android_main_pass.txt",
    REPORTS_DIR / "ios_dev_fail.txt",
]


def test_csv_file_exists():
    assert CSV_PATH.is_file(), (
        f"The source CSV file must exist at {CSV_PATH} but was not found."
    )


def test_csv_file_content_matches_exactly():
    """
    The CSV must contain *exactly* the ten lines defined in
    EXPECTED_CSV_LINES, in the same order, each terminated with a single
    UNIX newline.  No extra whitespace or blank lines are allowed.
    """
    with CSV_PATH.open("r", encoding="utf-8") as fh:
        actual_lines = fh.readlines()

    expected_with_newlines = [f"{line}\n" for line in EXPECTED_CSV_LINES]

    assert (
        actual_lines == expected_with_newlines
    ), (
        "The contents of the CSV file do not match the expected initial "
        "state.  Please ensure the file has exactly the ten lines provided in "
        "the task description, each terminated with a single '\\n'."
    )


def test_each_csv_line_has_four_semicolon_separated_fields():
    """
    Guard-rail: every line must contain exactly four semicolon-separated
    fields (run_id;platform;branch;result).  This protects against
    accidental corruption of the input data.
    """
    with CSV_PATH.open("r", encoding="utf-8") as fh:
        for idx, line in enumerate(fh, start=1):
            num_fields = len(line.rstrip("\n").split(";"))
            assert num_fields == 4, (
                f"Line {idx} of the CSV file should have exactly 4 "
                f"semicolon-separated fields, but {num_fields} were found."
            )


def test_reports_directory_and_files_not_present_yet():
    """
    Prior to the student's action, the reports directory should *not*
    contain the two report files—or it may not exist at all.
    """
    if REPORTS_DIR.exists():
        assert REPORTS_DIR.is_dir(), (
            f"{REPORTS_DIR} exists but is not a directory."
        )

        unexpected = [
            str(path)
            for path in EXPECTED_REPORT_FILES
            if path.exists()
        ]
        assert not unexpected, (
            "The following report file(s) already exist but should be created "
            "by the student as part of the task:\n"
            + "\n".join(unexpected)
        )