# test_initial_state.py
#
# This pytest suite validates the **initial** filesystem state *before*
# the student script runs.  It checks that:
#   1. The observability directory exists.
#   2. The two raw log files exist *and* contain the exact expected
#      pipe-delimited content (6 lines each, header + 5 data rows).
#   3. The target output files **do not** exist yet.
#
# If any assertion fails, the error message will clearly indicate what
# is missing or incorrect.
#
# NOTE: No checks are performed for the files that the student must
# eventually create (dashboard_source.csv and verification.log) other
# than ensuring they are currently absent.

import os
import pathlib
import pytest

OBS_DIR = pathlib.Path("/home/user/observability")
CPU_LOG = OBS_DIR / "metrics_cpu.log"
MEM_LOG = OBS_DIR / "metrics_mem.log"
DASHBOARD_CSV = OBS_DIR / "dashboard_source.csv"
VERIFICATION_LOG = OBS_DIR / "verification.log"

# ----------------------------------------------------------------------
# Expected contents of the raw log files (each line must end with '\n')
# ----------------------------------------------------------------------

CPU_EXPECTED_LINES = [
    "timestamp|host|cpu_usage_percent|load_average|context_switches\n",
    "2024-12-01T12:00:00Z|server-a|37.5|0.89|2312\n",
    "2024-12-01T12:05:00Z|server-a|42.1|0.92|2478\n",
    "2024-12-01T12:10:00Z|server-a|45.0|0.95|2560\n",
    "2024-12-01T12:15:00Z|server-a|39.2|0.90|2401\n",
    "2024-12-01T12:20:00Z|server-a|41.8|0.93|2505\n",
]

MEM_EXPECTED_LINES = [
    "timestamp|host|mem_used_mb|mem_free_mb|swap_used_mb\n",
    "2024-12-01T12:00:00Z|server-a|5678|1024|256\n",
    "2024-12-01T12:05:00Z|server-a|5690|1012|256\n",
    "2024-12-01T12:10:00Z|server-a|5705|997|256\n",
    "2024-12-01T12:15:00Z|server-a|5710|992|256\n",
    "2024-12-01T12:20:00Z|server-a|5725|977|256\n",
]

# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------

def read_file_lines(path: pathlib.Path):
    """Return list of lines from a text file, preserving newline chars."""
    with path.open("r", encoding="utf-8") as fh:
        return fh.readlines()


# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------

def test_observability_directory_exists():
    assert OBS_DIR.is_dir(), f"Required directory missing: {OBS_DIR}"


@pytest.mark.parametrize(
    "path, expected_lines",
    [
        (CPU_LOG, CPU_EXPECTED_LINES),
        (MEM_LOG, MEM_EXPECTED_LINES),
    ],
)
def test_source_log_files_exist_and_match_expected_content(path, expected_lines):
    assert path.is_file(), f"Source log file missing: {path}"
    actual_lines = read_file_lines(path)

    # Ensure exact number of lines
    assert len(actual_lines) == len(
        expected_lines
    ), f"{path} should contain {len(expected_lines)} lines " \
       f"(header + 5 rows). Found {len(actual_lines)}."

    # Compare line-by-line to help students identify mismatches easily
    for idx, (actual, expected) in enumerate(zip(actual_lines, expected_lines), start=1):
        assert (
            actual == expected
        ), f"Line {idx} in {path} mismatch:\n" \
           f"  expected: {expected!r}\n" \
           f"  found   : {actual!r}"


@pytest.mark.parametrize("path", [DASHBOARD_CSV, VERIFICATION_LOG])
def test_output_files_do_not_yet_exist(path):
    assert not path.exists(), (
        f"Output file {path} should NOT exist before the student script runs."
    )