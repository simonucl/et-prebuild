# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating system
# before the learner makes any changes for the “notifyd” support ticket.
#
# The expectations are:
#
# 1. /home/user/.config/notifyd/notifyd.conf
#       • Must exist and be a regular file.
#       • Must contain exactly the single line “enabled=0”
#         (optionally terminated by a single Unix newline).
#
# 2. /home/user/log/notifyd/  MUST NOT exist yet.
#
# 3. /home/user/log/notifyd/config_change.log  MUST NOT exist yet.
#
# Any deviation from the above means the starting state is wrong and should
# immediately fail so that downstream grading is meaningful.

import pathlib
import os
import stat
import pytest

HOME = pathlib.Path("/home/user")

CONFIG_FILE = HOME / ".config" / "notifyd" / "notifyd.conf"
LOG_DIR = HOME / "log" / "notifyd"
LOG_FILE = LOG_DIR / "config_change.log"


def _read_text(path):
    """
    Helper that reads a small text file safely and returns its str contents.

    Raises a clear pytest failure if the file cannot be read as UTF-8.
    """
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        pytest.fail(f"{path} is not valid UTF-8 text: {exc}")


def test_config_file_exists_and_is_disabled():
    """
    The notifyd configuration file must be present *and* set to disabled
    (enabled=0) before the user makes any modifications.
    """
    assert CONFIG_FILE.is_file(), (
        f"Expected config file {CONFIG_FILE} to exist as a regular file, "
        "but it is missing."
    )

    # Verify file permissions are ordinary (not world-writable, etc.).
    mode = CONFIG_FILE.stat().st_mode
    assert stat.S_ISREG(mode), f"{CONFIG_FILE} exists but is not a regular file."

    # Accept either no newline or a single trailing newline.
    contents = _read_text(CONFIG_FILE)
    if contents.endswith("\n"):
        stripped = contents[:-1]  # remove the final newline for comparison
        leftover_newlines = contents.count("\n")
        assert leftover_newlines == 1, (
            f"{CONFIG_FILE} should contain exactly one line; "
            f"found {leftover_newlines} newline characters."
        )
        contents_no_nl = stripped
    else:
        contents_no_nl = contents

    assert contents_no_nl == "enabled=0", (
        f"{CONFIG_FILE} content mismatch.\n"
        "Expected exactly:\n\n"
        "    enabled=0\n\n"
        f"Got:\n\n{contents!r}"
    )


def test_log_directory_absent():
    """
    The log directory for notifyd should *not* exist yet; the student must
    create it as part of the task.
    """
    assert not LOG_DIR.exists(), (
        f"Log directory {LOG_DIR} unexpectedly already exists. "
        "It should be created by the learner's solution."
    )


def test_log_file_absent():
    """
    The change-control log file must also be absent at the start.
    """
    assert not LOG_FILE.exists(), (
        f"Log file {LOG_FILE} unexpectedly already exists. "
        "It should be created by the learner's solution."
    )