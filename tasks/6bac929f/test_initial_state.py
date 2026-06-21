# test_initial_state.py
"""
Pytest suite to validate the _initial_ workstation state **before** the learner
performs any actions for the “manpreview” setup task.

This file purposely avoids checking for the *output* artefacts the learner is
expected to create (`~/.config/manpreview/config.ini`, the log file, etc.),
because those should be absent at this stage.  Instead, it verifies that the
baseline filesystem environment is sane and ready for the task.

Rules adhered to:
* Uses only the Python standard library + pytest.
* Provides clear failure messages.
* Does **not** reference the eventual output files or directories.
"""

from pathlib import Path
import os
import tempfile
import pytest


HOME = Path("/home/user")


def test_home_directory_exists_and_is_directory():
    """Ensure /home/user exists and is a directory."""
    assert HOME.exists(), "Expected /home/user to exist."
    assert HOME.is_dir(), "/home/user exists but is not a directory."


def test_home_directory_writable():
    """
    Confirm the user has write permissions to /home/user by attempting to
    create and immediately delete a temporary file there.
    """
    try:
        with tempfile.NamedTemporaryFile(dir=HOME, delete=True) as tmp:
            tmp.write(b"probe")  # noqa: WPS110 – simple probe write
    except PermissionError as exc:
        pytest.fail(f"Cannot write to /home/user: {exc}")


def test_config_folder_not_prepopulated():
    """
    Verify that the specific application folder ~/.config/manpreview
    is not already populated with a config.ini file before the task starts.

    NOTE: We deliberately avoid failing if the folder itself exists because
    many environments already have a ~/.config directory.  We merely ensure
    the target configuration file is not in place yet.
    """
    target_file = HOME / ".config" / "manpreview" / "config.ini"
    assert not target_file.exists(), (
        "The configuration file "
        f"{target_file} already exists, but it should be created by the learner."
    )


def test_setup_log_not_prepopulated():
    """
    Confirm that the final log file is not present yet; it must be produced
    by the learner as part of the exercise.
    """
    log_path = HOME / "setup_summary.log"
    assert not log_path.exists(), (
        "The log file /home/user/setup_summary.log already exists; "
        "it should be generated during the learner's setup steps."
    )