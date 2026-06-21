# test_initial_state.py
"""
Pytest suite to validate the operating-system / filesystem state
BEFORE the learner performs any actions.

This file checks ONLY the pre-condition items supplied in the task
description.  It purposefully avoids checking for any output files or
directories that the learner is expected to create.

Rules honoured:
  • Full absolute paths are used.
  • Only stdlib + pytest are imported.
"""

import os
import stat
import pytest

# ----------  CONSTANTS  ------------------------------------------------------

HOME_DIR = "/home/user"
IOT_ROOT = os.path.join(HOME_DIR, "iot_device")
CONFIG_DIR = os.path.join(IOT_ROOT, "config")
DEVICE_CONF = os.path.join(CONFIG_DIR, "device.conf")

EXPECTED_CONF_BYTES = b"# Device Configuration\nMAX_THREADS=1\n"


# ----------  HELPERS  --------------------------------------------------------


def _assert_is_directory(path: str) -> None:
    """
    Assert that `path` exists and is a directory.
    """
    assert os.path.exists(path), f"Expected directory '{path}' to exist, but it does not."
    assert os.path.isdir(path), f"'{path}' exists but is not a directory."


def _assert_is_regular_file(path: str) -> None:
    """
    Assert that `path` exists and is a regular file.
    """
    assert os.path.exists(path), f"Expected file '{path}' to exist, but it does not."
    st = os.stat(path)
    assert stat.S_ISREG(st.st_mode), f"'{path}' exists but is not a regular file."


# ----------  TESTS  ----------------------------------------------------------


def test_required_directories_exist():
    """
    The directories /home/user/iot_device/ and /home/user/iot_device/config/
    must already exist.
    """
    _assert_is_directory(IOT_ROOT)
    _assert_is_directory(CONFIG_DIR)


def test_device_conf_file_exists_and_is_regular():
    """
    The configuration file must be present as a regular file.
    """
    _assert_is_regular_file(DEVICE_CONF)


def test_device_conf_content_is_exact_two_line_template():
    """
    The file must contain exactly the two expected lines and end with a single
    newline character.  No other text (including blank lines) is allowed.
    """
    with open(DEVICE_CONF, "rb") as fp:
        content = fp.read()

    assert (
        content == EXPECTED_CONF_BYTES
    ), (
        "The file '{0}' does not contain the expected two-line template.\n\n"
        "Expected (repr):\n{1!r}\n\n"
        "Actual (repr):\n{2!r}".format(DEVICE_CONF, EXPECTED_CONF_BYTES, content)
    )