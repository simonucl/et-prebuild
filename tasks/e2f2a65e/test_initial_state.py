# test_initial_state.py
#
# This pytest suite verifies the *initial* state of the operating system
# before the student carries out the task described in the assignment.
#
# The student has been asked to create
#   /home/user/alerts/container_cpu_alert.json
# with specific contents.  At this point in time that file must *not* yet
# exist.  If it already exists (with any content), the exercise has been
# prematurely completed or the environment is not clean, so the tests must
# fail and clearly explain why.

import os
import json
import hashlib
import pytest

ALERTS_DIR = "/home/user/alerts"
ALERT_FILE = os.path.join(ALERTS_DIR, "container_cpu_alert.json")

# The exact contents that will eventually be required.  We keep it here
# only so we can compare if the file happens to exist already (which should
# fail the test).
EXPECTED_JSON = """{
  "alert": "container_cpu_usage",
  "threshold_percent": 80,
  "action": "email",
  "recipients": [
    "ops-team@example.com"
  ]
}
"""


def sha256_of_bytes(data: bytes) -> str:
    """Return the SHA-256 hex digest for the given byte sequence."""
    return hashlib.sha256(data).hexdigest()


EXPECTED_SHA256 = sha256_of_bytes(EXPECTED_JSON.encode("utf-8"))


def test_alert_json_must_not_exist_yet():
    """
    The target JSON file should NOT exist before the student performs the task.

    We also verify that, in the unlikely event the file *does* exist, its
    contents are not already the exact desired contents.  Either situation
    would indicate the starting environment is incorrect.
    """
    if not os.path.exists(ALERT_FILE):
        # Ideal situation: the file truly doesn't exist yet.
        assert True
        return

    # If the file path exists, we need to explain why this is a failure.
    if os.path.isdir(ALERT_FILE):
        pytest.fail(
            f"Expected a clean state but found a *directory* at "
            f"'{ALERT_FILE}'. Remove it so the exercise can create the "
            f"required JSON file."
        )

    # The path exists and is a file.  Read its contents and compare hashes.
    with open(ALERT_FILE, "rb") as fh:
        current_contents = fh.read()
    current_hash = sha256_of_bytes(current_contents)

    if current_hash == EXPECTED_SHA256:
        pytest.fail(
            f"The file '{ALERT_FILE}' already exists with the exact desired "
            f"contents. The initial state must be empty to properly test the "
            f"student's work."
        )
    else:
        pytest.fail(
            f"The file '{ALERT_FILE}' already exists but has *different* "
            f"contents. Remove or rename it before beginning the exercise."
        )


def test_alerts_directory_state_is_not_blocking():
    """
    The parent directory (/home/user/alerts) may or may not exist.

    If it exists, it must be a directory that the user can write to
    (standard permissions).  If it doesn't exist, that's fine—the student
    will create it during the exercise.
    """
    if not os.path.exists(ALERTS_DIR):
        # Directory doesn't exist yet.  That's acceptable.
        assert True
        return

    # It exists; confirm it is a directory.
    if not os.path.isdir(ALERTS_DIR):
        pytest.fail(
            f"A non-directory item exists at '{ALERTS_DIR}'. "
            f"Remove or rename it so the student can create the required "
            f"directory."
        )

    # Optionally, check basic write permissions (user has write bit).
    if not os.access(ALERTS_DIR, os.W_OK):
        pytest.fail(
            f"The directory '{ALERTS_DIR}' is not writable by the current "
            f"user. Adjust permissions so the exercise can proceed."
        )