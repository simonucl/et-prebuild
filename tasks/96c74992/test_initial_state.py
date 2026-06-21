# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the operating system
# before the student starts working on the “profiling archive” task.
#
# The suite checks that:
#   1. /home/user/raw_runs/ exists and contains exactly the three expected
#      *.run files.
#   2. Each *.run file has the expected line-count (sampling ticks).
#   3. The workspace that the student is supposed to create later
#      (/home/user/profiler/ and its sub-folders /results and /summary) does
#      NOT exist yet.
#
# Only the Python standard library and pytest are used.

import os
import stat
import pytest

HOME = "/home/user"
RAW_DIR = os.path.join(HOME, "raw_runs")
PROFILER_DIR = os.path.join(HOME, "profiler")
RESULTS_DIR = os.path.join(PROFILER_DIR, "results")
SUMMARY_DIR = os.path.join(PROFILER_DIR, "summary")
SUMMARY_LOG = os.path.join(SUMMARY_DIR, "run_summary.log")

EXPECTED_FILES = {
    "app_alpha.run": 15,
    "app_beta.run": 22,
    "app_gamma.run": 9,
}


def _full(path):
    """Return the absolute path below RAW_DIR for a given filename."""
    return os.path.join(RAW_DIR, path)


def test_raw_runs_directory_exists_with_correct_permissions():
    assert os.path.isdir(RAW_DIR), (
        f"Required directory {RAW_DIR} is missing. "
        "The initial dataset must be present before you start."
    )

    mode = os.stat(RAW_DIR).st_mode
    # Check read & execute bits for the owner so tests can traverse it.
    assert mode & stat.S_IRUSR and mode & stat.S_IXUSR, (
        f"Directory {RAW_DIR} exists but lacks read/execute permissions "
        "required for the exercise."
    )


def test_expected_run_files_exist_and_have_correct_line_counts():
    found_files = set(os.listdir(RAW_DIR))
    expected_files_set = set(EXPECTED_FILES.keys())

    missing = expected_files_set - found_files
    extra   = found_files - expected_files_set

    assert not missing, (
        "The following expected *.run files are missing in "
        f"{RAW_DIR}: {', '.join(sorted(missing))}"
    )
    # We allow extra files but warn if they exist to keep the student honest.
    assert not extra, (
        "Unexpected files found in the raw data directory: "
        f"{', '.join(sorted(extra))}. The initial state should contain only "
        "the three specified .run files."
    )

    # Verify line counts
    for filename, expected_lines in EXPECTED_FILES.items():
        path = _full(filename)
        assert os.path.isfile(path), f"Expected file {path} is not present."

        with open(path, "r", encoding="ascii") as fh:
            line_count = sum(1 for _ in fh)

        assert line_count == expected_lines, (
            f"{path} should contain {expected_lines} lines, "
            f"but {line_count} lines were found."
        )


@pytest.mark.parametrize(
    "path",
    [
        PROFILER_DIR,
        RESULTS_DIR,
        SUMMARY_DIR,
        SUMMARY_LOG,
    ],
)
def test_profiler_workspace_not_present_yet(path):
    assert not os.path.exists(path), (
        f"{path} already exists, but the workspace should be created by the "
        "student during the task, not beforehand."
    )