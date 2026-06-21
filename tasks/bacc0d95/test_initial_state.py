# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the filesystem
# before the student performs any action.  It guarantees that only the
# two source CSV files are present and that they contain the exact
# contents described in the task.  It also confirms that none of the
# expected output artefacts (release_matrix.json, build_summary.csv,
# process.log) exist yet.
#
# The home directory is assumed to be /home/user.

import os
from pathlib import Path

import pytest


CI_DIR = Path("/home/user/ci_data")

# Full paths to the files we need to check
BUILD_RESULTS = CI_DIR / "build_results.csv"
DEPLOYMENT_TARGETS = CI_DIR / "deployment_targets.csv"
RELEASE_MATRIX = CI_DIR / "release_matrix.json"
BUILD_SUMMARY = CI_DIR / "build_summary.csv"
PROCESS_LOG = CI_DIR / "process.log"


@pytest.fixture(scope="module")
def ci_dir_contents():
    """
    Return a sorted list of file names currently present in /home/user/ci_data.
    """
    if not CI_DIR.exists():
        pytest.fail(f"Required directory {CI_DIR} is missing")
    if not CI_DIR.is_dir():
        pytest.fail(f"{CI_DIR} exists but is not a directory")

    return sorted(os.listdir(CI_DIR))


def test_no_extra_files(ci_dir_contents):
    """
    The directory must contain **only** the two source CSV files:
    build_results.csv and deployment_targets.csv.
    """
    expected_files = sorted(
        [
            BUILD_RESULTS.name,
            DEPLOYMENT_TARGETS.name,
        ]
    )

    assert (
        ci_dir_contents == expected_files
    ), (
        f"{CI_DIR} should contain only {expected_files}, "
        f"but currently contains {ci_dir_contents}"
    )


def test_build_results_csv_exists_and_exact_content():
    """
    Validate that build_results.csv exists and matches the exact
    expected content, including line order.
    """
    assert BUILD_RESULTS.exists(), f"Missing required file: {BUILD_RESULTS}"

    expected_lines = [
        "build_id,artifact,status\n",
        "1001,service-api,success\n",
        "1002,service-auth,failure\n",
        "1003,website,success\n",
        "1004,worker,success\n",
    ]

    with BUILD_RESULTS.open("r", encoding="utf-8") as fh:
        actual_lines = fh.readlines()

    assert (
        actual_lines == expected_lines
    ), (
        f"Contents of {BUILD_RESULTS} differ from expected.\n"
        f"Expected:\n{''.join(expected_lines)}\n"
        f"Actual:\n{''.join(actual_lines)}"
    )


def test_deployment_targets_csv_exists_and_exact_content():
    """
    Validate that deployment_targets.csv exists and matches the exact
    expected content, including line order.
    """
    assert (
        DEPLOYMENT_TARGETS.exists()
    ), f"Missing required file: {DEPLOYMENT_TARGETS}"

    expected_lines = [
        "build_id,target_env\n",
        "1001,prod\n",
        "1003,staging\n",
        "1004,prod\n",
    ]

    with DEPLOYMENT_TARGETS.open("r", encoding="utf-8") as fh:
        actual_lines = fh.readlines()

    assert (
        actual_lines == expected_lines
    ), (
        f"Contents of {DEPLOYMENT_TARGETS} differ from expected.\n"
        f"Expected:\n{''.join(expected_lines)}\n"
        f"Actual:\n{''.join(actual_lines)}"
    )


@pytest.mark.parametrize(
    "path",
    [
        RELEASE_MATRIX,
        BUILD_SUMMARY,
        PROCESS_LOG,
    ],
)
def test_output_artefacts_do_not_exist_yet(path: Path):
    """
    None of the artefacts that the student is supposed to create should
    exist before the task is started.
    """
    assert not path.exists(), f"Artefact {path} should NOT exist yet"