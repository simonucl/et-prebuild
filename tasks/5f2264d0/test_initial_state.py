# test_initial_state.py
#
# This pytest file verifies the **initial** state of the operating system
# before the student performs any actions for the compliance-report task.
#
# It asserts that the source configuration file exists at the expected
# absolute path and that its contents exactly match what the exercise
# description specifies.  Nothing is tested about the output directory
# (/home/user/compliance) or the report file because those are products
# the student is expected to create later.

import difflib
from pathlib import Path

import pytest

CFG_PATH = Path("/home/user/config/system.cfg")

# The canonical contents of /home/user/config/system.cfg as provided
# in the task description.
EXPECTED_CFG_CONTENT = """[General]
hostname=server01
os=ubuntu
version=20.04

[Security]
firewall=enabled
selinux=disabled
password_policy=weak

[Compliance]
data_encryption=aes256
logging=disabled
"""


def _normalized_contents(text: str) -> str:
    """
    Return text with a single trailing newline and no leading/trailing
    blank lines so that we can compare files robustly while still
    catching meaningful differences.
    """
    # Strip leading/trailing whitespace/newlines, then ensure exactly one '\n'
    # at the end so that a missing or extra final newline does not trigger
    # a failure.
    return text.strip() + "\n"


def test_config_file_exists_and_is_regular_file():
    """
    The configuration file must exist and be a regular, readable file.
    """
    assert CFG_PATH.exists(), (
        f"Required configuration file not found: {CFG_PATH}"
    )
    assert CFG_PATH.is_file(), (
        f"Expected {CFG_PATH} to be a regular file but it's not."
    )


def test_config_file_contents_match_expected():
    """
    The contents of the configuration file must match the exact text
    supplied in the exercise description.  A helpful unified diff is
    shown if they differ.
    """
    actual_text = CFG_PATH.read_text(encoding="utf-8")
    expected_normalized = _normalized_contents(EXPECTED_CFG_CONTENT)
    actual_normalized = _normalized_contents(actual_text)

    if actual_normalized != expected_normalized:
        diff = "\n".join(
            difflib.unified_diff(
                expected_normalized.splitlines(),
                actual_normalized.splitlines(),
                fromfile="expected",
                tofile="actual",
                lineterm="",
            )
        )
        pytest.fail(
            "The contents of /home/user/config/system.cfg do not match the "
            "expected initial state:\n\n" + diff
        )