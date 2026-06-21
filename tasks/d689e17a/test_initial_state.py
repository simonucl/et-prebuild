# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the filesystem and
# environment before the student begins working on the task described in
# the prompt.  These tests are intentionally strict so that any deviation
# from the expected starting point is caught early and reported with a
# clear, actionable message.
#
# The checks performed are:
#   1. Required source artefacts (metrics.csv, mock_ps.txt) are present
#      at their exact absolute paths and contain the expected content.
#   2. None of the deliverable files/directories that the student is
#      supposed to create exist yet (they either do not exist at all, or
#      exist but are empty placeholders without the final content).
#
# Only the Python standard library and pytest are used.

import os
import stat
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constants — absolute paths and expected contents of *pre-seeded* artefacts.
# --------------------------------------------------------------------------- #
HOME = Path("/home/user").resolve()

METRICS_CSV = HOME / "experiments/run_01/metrics.csv"
MOCK_PS_TXT = HOME / "mock_ps.txt"

EXP_REPORTS_DIR = HOME / "exp_reports"
SNAPSHOT_LOG = EXP_REPORTS_DIR / "system_snapshot.log"
SUMMARY_JSON = EXP_REPORTS_DIR / "experiment_summary.json"
TOP_PROCS_CSV = EXP_REPORTS_DIR / "top_memory_processes.csv"

EXPECTED_METRICS_CONTENT = [
    "epoch,loss,accuracy",
    "1,0.80,0.71",
    "2,0.60,0.78",
    "3,0.45,0.82",
    "4,0.40,0.84",
    "5,0.38,0.85",
]

EXPECTED_MOCK_PS_CONTENT = [
    "PID USER %CPU %MEM COMMAND",
    "1234 user 12.3 1.1 python",
    "2345 user 2.1 15.2 chrome",
    "3456 user 0.5 10.0 java",
    "4567 user 50.0 0.3 gcc",
    "5678 user 0.7 5.5 node",
]


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def read_file_lines(path: Path):
    """Return a list of lines stripped of newlines from *path*."""
    with path.open("rt", encoding="utf-8") as fp:
        return [line.rstrip("\n") for line in fp.readlines()]


def assert_file_permissions(path: Path, expected_mode: int):
    """Assert that *path* has the given octal permissions (e.g. 0o644)."""
    st_mode = path.stat().st_mode & 0o777
    assert (
        st_mode == expected_mode
    ), f"{path} exists but has permissions {oct(st_mode)}, expected {oct(expected_mode)}."


# --------------------------------------------------------------------------- #
# Tests for presence and integrity of pre-seeded files.
# --------------------------------------------------------------------------- #
def test_metrics_csv_exists_and_is_correct():
    assert METRICS_CSV.is_file(), (
        "The expected metrics file is missing at "
        f"{METRICS_CSV}. This file must be present before the task begins."
    )

    lines = read_file_lines(METRICS_CSV)
    assert (
        lines == EXPECTED_METRICS_CONTENT
    ), (
        f"{METRICS_CSV} contents differ from the expected starting point.\n"
        "If you changed this file, please restore it to the original state."
    )

    # The file should be world-readable.
    assert_file_permissions(METRICS_CSV, 0o644)


def test_mock_ps_txt_exists_and_is_correct():
    assert MOCK_PS_TXT.is_file(), (
        "The expected mock process list is missing at "
        f"{MOCK_PS_TXT}. This file must be present before the task begins."
    )

    lines = read_file_lines(MOCK_PS_TXT)
    assert (
        lines == EXPECTED_MOCK_PS_CONTENT
    ), (
        f"{MOCK_PS_TXT} contents differ from the expected starting point.\n"
        "If you changed this file, please restore it to the original state."
    )

    assert_file_permissions(MOCK_PS_TXT, 0o644)


# --------------------------------------------------------------------------- #
# Tests ensuring that deliverable artefacts are *not* present yet.
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "path",
    [
        SNAPSHOT_LOG,
        SUMMARY_JSON,
        TOP_PROCS_CSV,
    ],
)
def test_output_files_do_not_exist_yet(path: Path):
    assert not path.exists(), (
        f"{path} already exists, but it should be created by the student as "
        "part of the exercise.  Remove or rename this file before starting."
    )


def test_exp_reports_dir_initial_state():
    """
    The /home/user/exp_reports directory may or may not already exist, but
    if it does, it must not contain any of the final artefacts and must not
    carry incorrect permissions that could mask later failures.
    """
    if EXP_REPORTS_DIR.exists():
        assert EXP_REPORTS_DIR.is_dir(), (
            f"{EXP_REPORTS_DIR} exists but is not a directory."
        )

        # Directory exists — ensure it does *not* yet contain the required files.
        present = [p.name for p in EXP_REPORTS_DIR.iterdir()]
        forbidden = {
            SNAPSHOT_LOG.name,
            SUMMARY_JSON.name,
            TOP_PROCS_CSV.name,
        }.intersection(present)

        assert (
            not forbidden
        ), (
            f"The following deliverable files are already present in "
            f"{EXP_REPORTS_DIR}: {', '.join(sorted(forbidden))}. "
            "They must not exist before the student runs their solution."
        )

        # If directory already exists, check its permissions are not overly lax.
        mode = EXP_REPORTS_DIR.stat().st_mode & 0o777
        assert (
            mode in {0o700, 0o755}
        ), (
            f"{EXP_REPORTS_DIR} has permissions {oct(mode)}. "
            "They should be 755 after task completion, but at this stage "
            "the directory must *at least* not be world-writable."
        )