# test_initial_state.py
#
# This pytest suite verifies the initial operating-system / filesystem
# state *before* the student performs any action for the “best-run”
# extraction task.

import os
import textwrap
import pytest


EXP_DIR = "/home/user/experiments"
METRICS_CSV = os.path.join(EXP_DIR, "metrics.csv")


def test_experiments_directory_exists():
    assert os.path.isdir(EXP_DIR), (
        f"Required directory missing: {EXP_DIR!r}. "
        "The task expects the experiments workspace to exist."
    )


def test_metrics_csv_exists():
    assert os.path.isfile(METRICS_CSV), (
        f"Required file missing: {METRICS_CSV!r}. "
        "The task cannot proceed without the metrics.csv file."
    )


def test_metrics_csv_content_is_exact():
    """The CSV must match the specification exactly."""
    expected_content = textwrap.dedent(
        """\
        run_id,accuracy,loss
        run_001,0.87,0.34
        run_002,0.91,0.29
        run_003,0.89,0.31
        """
    )
    # The spec states “terminating newlines”; each of the four lines,
    # including the last one, ends with '\n'.
    expected_content = expected_content  # already ends with '\n' after last line

    with open(METRICS_CSV, "r", encoding="utf-8") as fh:
        actual_content = fh.read()

    # Helpful diff style message on mismatch
    assert actual_content == expected_content, (
        "The contents of metrics.csv do not match the expected initial state.\n"
        "Expected:\n"
        f"{expected_content!r}\n\n"
        "Found:\n"
        f"{actual_content!r}"
    )