# test_initial_state.py
#
# Pytest suite that validates the *starting* filesystem/OS state
# for the “AWS month-end FinOps” shell assignment.
#
# The checks purposely assert ONLY the things that must already be
# present **before** the student runs any commands.  Conversely,
# it also confirms that none of the expected output artefacts have
# been created yet.
#
# If any check fails the accompanying message explains exactly
# what is missing or unexpectedly present.
#
# NOTE:  Uses only the Python standard library + pytest.

import os
import pathlib
import pytest

HOME = pathlib.Path("/home/user")

RAW_DIR = HOME / "raw_reports"
RAW_FILES = {
    "aws_costs_2023-08.csv": 8,  # header + 7 data lines
    "aws_costs_2023-09.csv": 9,  # header + 8 data lines
}

# Paths that should *not* exist yet
PIPE_DIR = HOME / "pipe_stage"
PIPE_FILES = {
    PIPE_DIR / "aws_costs_2023-08.pipe",
    PIPE_DIR / "aws_costs_2023-09.pipe",
}
FINOPS_DIR = HOME / "finops_logs"
FINOPS_FILES = {
    FINOPS_DIR / "q3_2023_service_costs.log",
    FINOPS_DIR / "q3_2023_daily_trend.log",
}

HEADER = "Date,Account,Service,Region,CostUSD"


def test_raw_reports_directory_exists_and_is_clean():
    """Verify /home/user/raw_reports exists and contains ONLY the two expected CSVs."""
    assert RAW_DIR.is_dir(), f"Required directory {RAW_DIR} is missing."
    found = {p.name for p in RAW_DIR.iterdir() if p.is_file()}
    expected = set(RAW_FILES)
    missing = expected - found
    unexpected = found - expected
    assert not missing, (
        "The following required raw report file(s) are missing:\n"
        + "\n".join(f"- {m}" for m in sorted(missing))
    )
    assert not unexpected, (
        "Found unexpected file(s) in /home/user/raw_reports (should contain ONLY the two raw CSVs):\n"
        + "\n".join(f"- {u}" for u in sorted(unexpected))
    )


@pytest.mark.parametrize("filename,total_lines", RAW_FILES.items())
def test_each_raw_csv_has_correct_header_and_line_count(filename, total_lines):
    """Confirm the header row is correct and the file has the expected number of lines."""
    path = RAW_DIR / filename
    assert path.is_file(), f"Expected file {path} is missing."

    with path.open("r", encoding="utf-8") as fh:
        first_line = fh.readline().rstrip("\n")
        assert first_line == HEADER, (
            f"Header mismatch in {filename}.\n"
            f" Expected: {HEADER}\n"
            f" Found   : {first_line}"
        )

        # Count total lines (including header)
        line_count = 1 + sum(1 for _ in fh)
        assert (
            line_count == total_lines
        ), f"{filename} should contain {total_lines} total lines (header included) but has {line_count}."


def test_no_output_directories_or_files_exist_yet():
    """
    Ensure that none of the deliverables/directories exist before the student
    starts working.  Their presence would indicate the grading environment is
    already ‘dirty’.
    """
    assert not PIPE_DIR.exists(), f"Directory {PIPE_DIR} should NOT exist yet."
    assert not FINOPS_DIR.exists(), f"Directory {FINOPS_DIR} should NOT exist yet."

    for path in PIPE_FILES | FINOPS_FILES:
        assert not path.exists(), f"Output file {path} should NOT exist before student action."