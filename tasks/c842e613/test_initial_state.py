# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating system
# before the student starts working on the task.  It checks that the raw
# profile file exists with the exact expected content and that none of the
# output artefacts (profiling_reports directory, summary files, tarball, log,
# …) are present yet.
#
# Only stdlib + pytest are used.

import os
from pathlib import Path

RAW_PROFILE = Path("/home/user/raw_profiles/app_service.profile")
REPORT_DIR = Path("/home/user/profiling_reports")

EXPECTED_LINES = [
    "# Profile data for app_service",
    "# timestamp cpu_percent mem_mb",
    "2024-06-20T12:00:00Z 35.5 1530",
    "2024-06-20T12:00:05Z 42.0 1548",
    "2024-06-20T12:00:10Z 27.3 1522",
    "2024-06-20T12:00:15Z 55.1 1555",
    "2024-06-20T12:00:20Z 48.6 1540",
    "2024-06-20T12:00:25Z 31.2 1528",
]


def test_raw_profile_file_exists():
    """The raw profile file must exist before any transformation starts."""
    assert RAW_PROFILE.is_file(), (
        f"Expected raw trace file at '{RAW_PROFILE}', but it does not exist. "
        "Ensure the initial dataset is in place."
    )


def test_raw_profile_content_exact():
    """
    The raw profile file must contain exactly the eight expected lines,
    in order, with no extra or missing lines.
    """
    with RAW_PROFILE.open("r", encoding="utf-8") as fh:
        actual_lines = [ln.rstrip("\n") for ln in fh.readlines()]

    assert (
        actual_lines == EXPECTED_LINES
    ), (
        "The contents of the raw profile file do not match the expected "
        "initial dataset.\n"
        f"Expected lines ({len(EXPECTED_LINES)}):\n{EXPECTED_LINES}\n\n"
        f"Actual lines   ({len(actual_lines)}):\n{actual_lines}"
    )


def test_output_directory_absent_initially():
    """
    The /home/user/profiling_reports directory (and therefore any files that
    should be created by the student's solution) must NOT exist yet.
    """
    assert not REPORT_DIR.exists(), (
        f"Directory '{REPORT_DIR}' already exists before the transformation "
        "has been run. Make sure tests are executed on a clean initial state."
    )