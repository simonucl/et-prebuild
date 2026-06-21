# test_initial_state.py
#
# This pytest suite validates the initial state of the filesystem
# before the learner performs any actions.  It checks only the items
# that are supposed to be pre-existing; it deliberately ignores any
# artefacts that the learner is expected to create (e.g.,
# /home/user/security/rotation_report.txt).

import os
from pathlib import Path

SECURITY_DIR = Path("/home/user/security")
ROTATION_LOG = SECURITY_DIR / "rotation.log"


def test_security_directory_exists():
    """
    Verify that /home/user/security exists and is a directory.
    """
    assert SECURITY_DIR.exists(), (
        f"Required directory {SECURITY_DIR} is missing."
    )
    assert SECURITY_DIR.is_dir(), (
        f"{SECURITY_DIR} exists but is not a directory."
    )


def test_rotation_log_exists_and_is_readable():
    """
    Verify that /home/user/security/rotation.log exists, is a file,
    and is readable.
    """
    assert ROTATION_LOG.exists(), (
        f"Required file {ROTATION_LOG} is missing."
    )
    assert ROTATION_LOG.is_file(), (
        f"{ROTATION_LOG} exists but is not a regular file."
    )
    # Check read permission by attempting to open the file.
    try:
        with ROTATION_LOG.open("r", encoding="utf-8") as _:
            pass
    except Exception as exc:  # pragma: no cover
        raise AssertionError(
            f"Cannot read {ROTATION_LOG}: {exc}"
        ) from exc


def test_rotation_log_contents_exact():
    """
    Verify that rotation.log contains exactly the expected six lines
    with no extra or missing entries.
    """
    expected_lines = [
        "2024-05-21T09:14:03Z INFO User john rotated credential AKIAOLD123 to AKIANEW321 from IP 10.0.0.12",
        "2024-05-21T10:22:17Z WARN Rotation failed for credential AKIAOLD456 from IP 10.0.0.7",
        "2024-05-21T11:33:01Z INFO User alice rotated credential AKIAOLD789 to AKIANEW654 from IP 10.0.0.23",
        "2024-05-22T12:01:55Z INFO User bob rotated credential AKIAOLD000 to AKIANEW999 from IP 10.0.0.5",
        "2024-05-22T13:09:42Z WARN Rotation failed for credential AKIAOLD888 from IP 10.0.0.29",
        "2024-05-22T14:45:17Z INFO User carol rotated credential AKIAOLD222 to AKIANEW333 from IP 10.0.0.44",
    ]

    with ROTATION_LOG.open("r", encoding="utf-8") as fh:
        actual_lines = fh.read().splitlines()

    assert actual_lines == expected_lines, (
        "Contents of rotation.log do not match the expected initial "
        "state.\n\nExpected:\n"
        + "\n".join(expected_lines)
        + "\n\nFound:\n"
        + "\n".join(actual_lines)
    )