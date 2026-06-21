# test_initial_state.py
#
# Pytest suite that verifies the initial, pre-task filesystem state for the
# “experiment log consolidation” assignment.  It checks that the expected
# experiment directories and their artifact files exist *and* contain the
# exact data specified in the task description.
#
# These tests purposefully DO NOT touch or mention any output locations
# such as /home/user/experiments/summary/ or
# /home/user/experiments/summary/experiment_overview.log.

import pathlib
import re
import pytest

BASE_DIR = pathlib.Path("/home/user/experiments")

# (experiment_name, final_accuracy, final_loss, learning_rate)
EXPERIMENTS = [
    ("exp_alpha", "0.9234", "0.1123", "0.001"),
    ("exp_beta",  "0.9111", "0.1278", "0.0005"),
    ("exp_gamma", "0.9570", "0.0931", "0.002"),
]

def test_experiments_base_dir_exists():
    """/home/user/experiments must exist and be a directory."""
    assert BASE_DIR.exists(), f"Expected directory {BASE_DIR} to exist."
    assert BASE_DIR.is_dir(), f"{BASE_DIR} exists but is not a directory."


@pytest.mark.parametrize("exp_name,exp_acc,exp_loss,exp_lr", EXPERIMENTS)
def test_experiment_files_and_contents(exp_name, exp_acc, exp_loss, exp_lr):
    """
    For each experiment directory:
      1. metrics.csv and config.yaml must exist.
      2. metrics.csv must have the correct header and at least two data rows.
      3. The LAST data row in metrics.csv must match the expected accuracy
         and loss values.
      4. config.yaml must contain a 'learning_rate:' line whose value matches
         the expected learning-rate.
    """
    exp_dir = BASE_DIR / exp_name
    metrics_file = exp_dir / "metrics.csv"
    config_file  = exp_dir / "config.yaml"

    # ---------- Structure checks ----------
    assert exp_dir.exists(), f"Missing experiment directory: {exp_dir}"
    assert exp_dir.is_dir(), f"{exp_dir} exists but is not a directory."

    assert metrics_file.exists(), f"Missing metrics file: {metrics_file}"
    assert metrics_file.is_file(), f"{metrics_file} exists but is not a file."

    assert config_file.exists(), f"Missing config file: {config_file}"
    assert config_file.is_file(), f"{config_file} exists but is not a file."

    # ---------- metrics.csv content checks ----------
    lines = [ln.rstrip("\n") for ln in metrics_file.read_text().splitlines()]

    assert lines, f"{metrics_file} is empty."
    header = lines[0]
    assert header == "epoch,accuracy,loss", (
        f"{metrics_file} header mismatch.\n"
        f"Expected: 'epoch,accuracy,loss'\n"
        f"Found:    '{header}'"
    )
    assert len(lines) >= 3, (
        f"{metrics_file} should contain at least two data rows "
        f"(found only {len(lines)-1})."
    )

    last_row = lines[-1]
    parts = last_row.split(",")
    assert len(parts) == 3, (
        f"Expected 3 comma-separated columns in last row of {metrics_file}, "
        f"found {len(parts)}: {last_row!r}"
    )

    epoch_str, acc_str, loss_str = parts
    # Validate that accuracy and loss are floats and match expected strings
    for label, value in [("accuracy", acc_str), ("loss", loss_str)]:
        try:
            float(value)
        except ValueError:
            pytest.fail(
                f"Column '{label}' in last row of {metrics_file} should be "
                f"a valid float, got {value!r}"
            )

    assert acc_str == exp_acc, (
        f"Accuracy mismatch in {metrics_file}.\n"
        f"Expected: {exp_acc}\n"
        f"Found:    {acc_str}"
    )
    assert loss_str == exp_loss, (
        f"Loss mismatch in {metrics_file}.\n"
        f"Expected: {exp_loss}\n"
        f"Found:    {loss_str}"
    )

    # ---------- config.yaml content checks ----------
    lr_pattern = re.compile(r"^\s*learning_rate:\s+([0-9.]+)\s*$")
    lr_value = None
    for line in config_file.read_text().splitlines():
        match = lr_pattern.match(line)
        if match:
            lr_value = match.group(1)
            break

    assert lr_value is not None, (
        f"{config_file} does not contain a line of the form "
        f"'learning_rate: <float>'."
    )

    try:
        float(lr_value)
    except ValueError:
        pytest.fail(
            f"Learning rate value in {config_file} should be a valid float, "
            f"got {lr_value!r}."
        )

    assert lr_value == exp_lr, (
        f"Learning rate mismatch in {config_file}.\n"
        f"Expected: {exp_lr}\n"
        f"Found:    {lr_value}"
    )