# test_initial_state.py
#
# This pytest suite validates the *initial* state of the filesystem
# before the student performs any actions.  It checks only for the
# artefacts that must already exist; it intentionally does **not** look
# for the backup file, the change-records directory, or the log file,
# because those are created by the student as part of the assignment.

import os
import pytest

CONFIG_DIR = "/home/user/configs"
CONFIG_FILE = os.path.join(CONFIG_DIR, "app.cfg")

EXPECTED_CONFIG_CONTENT = (
    "# Application Configuration\n"
    "VERSION=1.4.2\n"
    "ENABLED=false\n"
    "LOG_LEVEL=info\n"
)


def test_config_directory_exists():
    """The directory /home/user/configs must exist."""
    assert os.path.isdir(
        CONFIG_DIR
    ), f"Required directory missing: {CONFIG_DIR!r}"


def test_config_file_exists():
    """The file /home/user/configs/app.cfg must exist."""
    assert os.path.isfile(
        CONFIG_FILE
    ), f"Required file missing: {CONFIG_FILE!r}"


def test_config_file_contents_exact_match():
    """
    The initial configuration file must contain the exact expected
    contents (including the trailing newline).
    """
    with open(CONFIG_FILE, "r", encoding="utf-8") as fh:
        actual = fh.read()

    assert (
        actual == EXPECTED_CONFIG_CONTENT
    ), (
        f"Contents of {CONFIG_FILE!r} are not as expected.\n\n"
        "Expected:\n"
        "---------\n"
        f"{EXPECTED_CONFIG_CONTENT!r}\n\n"
        "Actual:\n"
        "-------\n"
        f"{actual!r}"
    )