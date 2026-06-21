# test_initial_state.py
#
# This test-suite asserts the **initial** filesystem state that must be
# present before the student’s solution runs.  It deliberately makes no
# reference to any files or directories that the student is expected to
# create (e.g. /home/user/experiment_runs/distributed_status.txt).

import os
from pathlib import Path

import pytest

BASE_DIR = Path("/home/user/experiments")
RUNS = {
    "run_alpha": {
        "node1.log": {"training_expected": True, "error_expected": False},
        "node2.log": {"training_expected": True, "error_expected": False},
    },
    "run_beta": {
        "node1.log": {"training_expected": True, "error_expected": False},
        "node2.log": {"training_expected": False, "error_expected": True},
    },
    "run_gamma": {
        "node1.log": {"training_expected": True, "error_expected": False},
        "node2.log": {"training_expected": True, "error_expected": False},
    },
}


@pytest.mark.parametrize("run_id", RUNS.keys())
def test_run_log_directory_exists(run_id):
    """
    Each training run must have a logs/ directory that already exists.
    """
    dir_path = BASE_DIR / run_id / "logs"
    assert dir_path.is_dir(), f"Expected directory {dir_path} to exist."


@pytest.mark.parametrize(
    "run_id,log_name",
    [
        (run_id, log_name)
        for run_id, logs in RUNS.items()
        for log_name in logs.keys()
    ],
)
def test_node_log_files_exist(run_id, log_name):
    """
    Each expected node log file must already be present.
    """
    file_path = BASE_DIR / run_id / "logs" / log_name
    assert file_path.is_file(), f"Expected log file {file_path} to exist."


@pytest.mark.parametrize(
    "run_id,log_name,training_expected,error_expected",
    [
        (run_id, log_name, meta["training_expected"], meta["error_expected"])
        for run_id, logs in RUNS.items()
        for log_name, meta in logs.items()
    ],
)
def test_node_log_contents(run_id, log_name, training_expected, error_expected):
    """
    Validate that each node log advertises its health status via
    the presence of 'TRAINING_COMPLETE' and/or 'ERROR'.
    """
    file_path = BASE_DIR / run_id / "logs" / log_name
    content = file_path.read_text(errors="ignore")

    if training_expected:
        assert "TRAINING_COMPLETE" in content, (
            f"{file_path} should contain 'TRAINING_COMPLETE' but it does not."
        )
    else:
        assert "TRAINING_COMPLETE" not in content, (
            f"{file_path} should NOT contain 'TRAINING_COMPLETE' but it does."
        )

    if error_expected:
        assert "ERROR" in content, (
            f"{file_path} should contain 'ERROR' but it does not."
        )
    else:
        # Note: we check the substring 'ERROR' rather than 'ERROR:' to keep
        # the assertion agnostic to formatting details.
        assert "ERROR" not in content, (
            f"{file_path} should NOT contain 'ERROR' but it does."
        )