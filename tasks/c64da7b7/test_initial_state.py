# test_initial_state.py
#
# This pytest file checks that the raw performance logs expected by the
# assignment are present and well-formed *before* the student starts writing
# code that consumes them.  Only the input directory (/home/user/cluster_logs)
# and its contents are verified—nothing related to the required output is
# inspected, per the grading rules.

import os
import csv
import pytest
from pathlib import Path

# ---------------------------------------------------------------------------#
# Constants describing the expected initial state
# ---------------------------------------------------------------------------#
HOME = Path("/home/user")
LOG_DIR = HOME / "cluster_logs"
EXPECTED_FILES = {
    "nodeA.log",
    "nodeB.log",
    "nodeC.log",
}
CSV_HEADER = (
    "timestamp",
    "cpu_percent",
    "mem_mb",
    "net_in_mb",
    "net_out_mb",
)
DATA_LINES_PER_FILE = 5  # exactly 5 data rows in every *.log file


# ---------------------------------------------------------------------------#
# Helper functions
# ---------------------------------------------------------------------------#
def read_csv_rows(path: Path):
    """Yield each row of the CSV file located at *path* as a tuple."""
    with path.open(newline="", encoding="utf-8") as fp:
        reader = csv.reader(fp)
        for row in reader:
            yield tuple(row)


def assert_numeric(value, line_no, file_path):
    """Helper—fail with a clear message if *value* cannot be parsed as int."""
    try:
        int(value)
    except ValueError:  # pragma: no cover
        pytest.fail(
            f"Non-integer value '{value}' found in {file_path} "
            f"(line {line_no}); every numeric field must be an integer."
        )


# ---------------------------------------------------------------------------#
# Tests
# ---------------------------------------------------------------------------#
def test_log_directory_present_and_correct():
    """The /home/user/cluster_logs directory must exist and contain the three log files."""
    assert LOG_DIR.exists(), (
        f"Required directory {LOG_DIR} is missing. It must already exist and "
        f"contain the raw performance logs."
    )
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."

    # Gather actual *.log files
    actual_files = {p.name for p in LOG_DIR.iterdir() if p.is_file()}
    missing = EXPECTED_FILES - actual_files
    unexpected = actual_files - EXPECTED_FILES

    assert not missing, (
        f"The following expected log files are missing from {LOG_DIR}: "
        f"{', '.join(sorted(missing))}"
    )
    # If the instructor accidentally left extra files, that's fine, but warn
    # the student so they know the checker will ignore them.
    if unexpected:
        pytest.skip(
            f"Extra files present in {LOG_DIR} that will be ignored: "
            f"{', '.join(sorted(unexpected))}"
        )


@pytest.mark.parametrize("filename", sorted(EXPECTED_FILES))
def test_each_log_file_has_correct_header_and_row_count(filename):
    """Every log file must begin with the exact CSV header and contain exactly 5 data lines."""
    file_path = LOG_DIR / filename
    rows = list(read_csv_rows(file_path))

    # --- Header ------------------------------------------------------------#
    assert rows, f"{file_path} is empty; must contain header and data lines."
    header = rows[0]
    assert header == CSV_HEADER, (
        f"Header mismatch in {file_path}.\n"
        f"Expected: {', '.join(CSV_HEADER)}\n"
        f"Actual:   {', '.join(header)}"
    )

    # --- Row count ---------------------------------------------------------#
    data_rows = rows[1:]
    assert len(data_rows) == DATA_LINES_PER_FILE, (
        f"{file_path} should contain exactly {DATA_LINES_PER_FILE} data "
        f"lines after the header, found {len(data_rows)}."
    )

    # --- Column count & types ---------------------------------------------#
    for idx, row in enumerate(data_rows, start=2):  # start=2 includes header
        assert len(row) == 5, (
            f"Wrong column count in {file_path} line {idx}. "
            f"Expected 5 values, found {len(row)}."
        )
        ts, cpu, mem, net_in, net_out = row

        # Basic timestamp sanity: ISO-8601 strings contain 'T' and 'Z'
        assert "T" in ts and ts.endswith("Z"), (
            f"Timestamp '{ts}' in {file_path} line {idx} is not ISO-8601 "
            f"(YYYY-MM-DDTHH:MM:SSZ)."
        )

        for value in (cpu, mem, net_in, net_out):
            assert_numeric(value, idx, file_path)