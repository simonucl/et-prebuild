# test_initial_state.py
#
# Pytest suite that verifies the **initial** state of the filesystem
# before the learner performs any actions.  It checks that the sandbox
# experiments directory exists, that each expected sub-directory and
# file is present, and that the contents of the log and CSV files match
# the specification given in the task description.
#
# NOTE:  This file intentionally does *not* test for any artefacts that
# the learner is supposed to create later (e.g. /home/user/experiment_summary).

import os
import re
import csv
import pytest
from pathlib import Path

HOME = Path("/home/user")
EXP_ROOT = HOME / "experiments"
EXPERIMENTS = ["exp1", "exp2", "exp3"]


@pytest.mark.parametrize("exp", EXPERIMENTS)
def test_experiment_directory_exists(exp):
    """
    Each experiment directory (exp1, exp2, exp3) must exist under
    /home/user/experiments and be a directory.
    """
    path = EXP_ROOT / exp
    assert path.exists(), f"Missing directory: {path}"
    assert path.is_dir(), f"Expected directory at {path}, but found something else."


@pytest.mark.parametrize("exp", EXPERIMENTS)
def test_log_file_exists_and_has_final_lines(exp):
    """
    log.txt must exist inside each experiment directory and must end with:
        Final accuracy: <float with 2 decimals>
        Final loss: <float with 2 decimals>
    """
    log_path = EXP_ROOT / exp / "log.txt"
    assert log_path.exists(), f"Missing log file: {log_path}"
    assert log_path.is_file(), f"Expected regular file at {log_path}"

    with log_path.open("r", encoding="utf-8") as fh:
        lines = [ln.rstrip("\n") for ln in fh.readlines()]

    # Strip possible empty lines at the end
    while lines and lines[-1] == "":
        lines.pop()

    assert len(lines) >= 2, (
        f"{log_path} should have at least two lines (final accuracy/loss), "
        f"found only {len(lines)}."
    )

    final_accuracy_line, final_loss_line = lines[-2], lines[-1]

    acc_pattern = re.compile(r"^Final accuracy: \d+\.\d{2}$")
    loss_pattern = re.compile(r"^Final loss: \d+\.\d{2}$")

    assert acc_pattern.match(final_accuracy_line), (
        f"{log_path} last-but-one line is malformed:\n"
        f"Expected format 'Final accuracy: <float with 2 decimals>'\n"
        f"Got: {final_accuracy_line!r}"
    )
    assert loss_pattern.match(final_loss_line), (
        f"{log_path} last line is malformed:\n"
        f"Expected format 'Final loss: <float with 2 decimals>'\n"
        f"Got: {final_loss_line!r}"
    )


@pytest.mark.parametrize("exp", EXPERIMENTS)
def test_metrics_csv_exists_and_has_header(exp):
    """
    metrics.csv must exist, be a CSV file with header:
        epoch,accuracy,loss
    and contain at least one data row.
    """
    csv_path = EXP_ROOT / exp / "metrics.csv"
    assert csv_path.exists(), f"Missing metrics file: {csv_path}"
    assert csv_path.is_file(), f"Expected regular file at {csv_path}"

    with csv_path.open("r", newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail(f"{csv_path} is empty, expected at least a header line.")

        expected_header = ["epoch", "accuracy", "loss"]
        assert header == expected_header, (
            f"{csv_path} header mismatch:\n"
            f"Expected: {','.join(expected_header)}\n"
            f"Got:      {','.join(header)}"
        )

        # Ensure there is at least one data row
        try:
            next(reader)
        except StopIteration:
            pytest.fail(f"{csv_path} contains header only; expected at least one data row.")