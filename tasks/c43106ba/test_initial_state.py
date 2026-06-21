# test_initial_state.py
#
# This test-suite verifies that the filesystem is exactly in the expected
# *initial* state before the student runs the required single-line shell
# command.  Any failure here means the starting point is wrong, so the
# subsequent exercise cannot be graded reliably.

import os
import pytest

# --------------------------------------------------------------------------- #
# Constants                                                                   #
# --------------------------------------------------------------------------- #
BASE_DIR = "/home/user/project/config"
MODEL_CFG = os.path.join(BASE_DIR, "model_config.yaml")
RUN_CFG = os.path.join(BASE_DIR, "run_settings.toml")
LOG_FILE = os.path.join(BASE_DIR, "update_log.txt")


# --------------------------------------------------------------------------- #
# Helpers                                                                     #
# --------------------------------------------------------------------------- #
def read_file(path: str) -> str:
    """Read *binary* then decode as UTF-8 to avoid newline translation issues."""
    with open(path, "rb") as fh:
        return fh.read().decode("utf-8")


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
def test_config_directory_exists():
    assert os.path.isdir(
        BASE_DIR
    ), f"Expected directory '{BASE_DIR}' to exist, but it is missing."


def test_model_config_initial_contents():
    assert os.path.isfile(
        MODEL_CFG
    ), f"Expected file '{MODEL_CFG}' to exist, but it is missing."

    expected = (
        "dataset:\n"
        '  path: "/data/train.csv"\n'
        "  batch_size: 32\n"
        "  shuffle: true\n"
    )
    actual = read_file(MODEL_CFG)
    assert (
        actual == expected
    ), (
        f"'{MODEL_CFG}' does not contain the expected initial content.\n"
        "Expected:\n"
        "----------\n"
        f"{expected!r}\n"
        "Got:\n"
        "-----\n"
        f"{actual!r}"
    )


def test_run_settings_initial_contents():
    assert os.path.isfile(
        RUN_CFG
    ), f"Expected file '{RUN_CFG}' to exist, but it is missing."

    expected = "[run]\nepochs = 10\nlearning_rate = 0.001\n"
    actual = read_file(RUN_CFG)
    assert (
        actual == expected
    ), (
        f"'{RUN_CFG}' does not contain the expected initial content.\n"
        "Expected:\n"
        "----------\n"
        f"{expected!r}\n"
        "Got:\n"
        "-----\n"
        f"{actual!r}"
    )


def test_update_log_does_not_exist_yet():
    assert not os.path.exists(
        LOG_FILE
    ), f"Log file '{LOG_FILE}' should NOT exist before the student's command is run."