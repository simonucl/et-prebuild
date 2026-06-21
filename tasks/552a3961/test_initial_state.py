# test_initial_state.py
#
# This pytest suite validates that the _input_ artifacts required by the
# student task are present and correct **before** the student performs any
# action.  It intentionally makes no assertions about the output directory
# /home/user/experiments/summary or any files that will be generated there.

import csv
import os
from pathlib import Path

import pytest

BASE_DIR = Path("/home/user/experiments")

# Mapping: experiment_id -> (relative metrics.csv path, expected final accuracy string)
EXPERIMENTS = {
    "exp_alpha": ("exp_alpha/metrics.csv", "0.78"),
    "exp_beta": ("exp_beta/metrics.csv", "0.84"),
    "exp_gamma": ("exp_gamma/metrics.csv", "0.74"),
}


def _read_csv_lines(csv_path):
    """Return header line (str) and list of data rows (List[List[str]])."""
    with csv_path.open(newline="") as fh:
        reader = csv.reader(fh)
        rows = list(reader)
        assert rows, f"{csv_path} is empty."
        header, data_rows = rows[0], rows[1:]
    return header, data_rows


@pytest.mark.parametrize("experiment_id", sorted(EXPERIMENTS))
def test_metrics_csv_exists_and_has_correct_header(experiment_id):
    rel_path, _ = EXPERIMENTS[experiment_id]
    csv_path = BASE_DIR / rel_path

    assert csv_path.exists(), f"Required file missing: {csv_path}"
    assert csv_path.is_file(), f"Expected a file at {csv_path}, but found something else."

    header, _ = _read_csv_lines(csv_path)

    expected_header = ["epoch", "loss", "accuracy"]
    assert header == expected_header, (
        f"{csv_path} header mismatch.\n"
        f"Expected: {','.join(expected_header)}\n"
        f"Found:    {','.join(header)}"
    )


@pytest.mark.parametrize("experiment_id", sorted(EXPERIMENTS))
def test_metrics_csv_has_at_least_one_data_row(experiment_id):
    rel_path, _ = EXPERIMENTS[experiment_id]
    csv_path = BASE_DIR / rel_path

    _, data_rows = _read_csv_lines(csv_path)
    assert data_rows, f"{csv_path} contains no data rows beneath the header."


@pytest.mark.parametrize("experiment_id", sorted(EXPERIMENTS))
def test_last_row_accuracy_matches_expectation(experiment_id):
    """
    The 'final accuracy' is defined as the accuracy value of the last
    data row (i.e., row with the highest epoch number).  This test ensures
    that value matches the ground-truth seeded in the container.
    """
    rel_path, expected_accuracy = EXPERIMENTS[experiment_id]
    csv_path = BASE_DIR / rel_path

    _, data_rows = _read_csv_lines(csv_path)

    # Validate column count and simple typing while we're here.
    for line_number, row in enumerate(data_rows, start=2):  # header is line 1
        assert len(row) == 3, (
            f"{csv_path} line {line_number} expected 3 comma-separated values "
            f"but found {len(row)}."
        )
        epoch_str = row[0]
        assert epoch_str.isdigit(), (
            f"{csv_path} line {line_number} first column should be an integer "
            f"epoch but found '{epoch_str}'."
        )

    final_accuracy = data_rows[-1][2]  # third column of the last row

    assert (
        final_accuracy == expected_accuracy
    ), f"{csv_path} expected final accuracy {expected_accuracy} but found {final_accuracy}."


def test_experiments_directory_presence():
    """
    A sanity check that the /home/user/experiments directory itself exists
    and is a directory.  This guards against catastrophic mounting issues.
    """
    assert BASE_DIR.exists(), f"Base directory {BASE_DIR} is missing."
    assert BASE_DIR.is_dir(), f"{BASE_DIR} exists but is not a directory."


def test_no_extra_missing_experiments():
    """
    Ensures that all declared experiment sub-directories exist.  Having them
    missing would indicate a corrupted initial state.
    """
    missing = [
        exp_id
        for exp_id, (rel_path, _) in EXPERIMENTS.items()
        if not (BASE_DIR / rel_path).parent.exists()
    ]
    assert not missing, (
        "The following experiment directories are missing under "
        f"{BASE_DIR}: {', '.join(missing)}"
    )