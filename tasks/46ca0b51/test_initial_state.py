# test_initial_state.py
#
# This test-suite verifies that the *initial* operating-system / filesystem
# state is exactly as expected **before** the student carries out any
# configuration steps.  It intentionally avoids checking for any files that
# must be created by the student later (e.g. backup files or audit logs).

import os
from pathlib import Path
import stat
import pytest

CONFIG_DIR = Path("/home/user/configs")
CONFIG_FILE = CONFIG_DIR / "dummy_service.conf"


@pytest.fixture(scope="module")
def expected_config_bytes() -> bytes:
    """
    The byte-for-byte contents that must be present in the original
    configuration file before the student script runs.
    """
    expected_lines = [
        "#-----------------------------------\n",
        "# Dummy Service configuration file\n",
        "# Maintainer: DevOps Team\n",
        "MAX_CLIENTS=50\n",
        "#-----------------------------------\n",
    ]
    # Join and encode once so every test uses the exact same bytes.
    return "".join(expected_lines).encode("utf-8")


def test_configs_directory_exists_and_is_writable():
    """
    /home/user/configs must already exist, be a directory, and be writable
    by the current user.  Without this the rest of the exercise cannot
    possibly succeed.
    """
    assert CONFIG_DIR.exists(), (
        f"Expected directory '{CONFIG_DIR}' is missing. "
        "Create it before running your automation."
    )
    assert CONFIG_DIR.is_dir(), (
        f"'{CONFIG_DIR}' exists but is not a directory."
    )
    # os.access uses the real UID/GID of the process, which is what we want.
    assert os.access(CONFIG_DIR, os.W_OK), (
        f"Directory '{CONFIG_DIR}' is not writable by the current user. "
        "Fix the permissions so your script can place files there."
    )


def test_original_config_file_present_and_correct(expected_config_bytes):
    """
    The original dummy_service.conf file must be present and match the exact
    canonical contents provided in the task description.  Any deviation here
    would invalidate subsequent grading that relies on a known starting
    point.
    """
    assert CONFIG_FILE.exists(), (
        f"Configuration file '{CONFIG_FILE}' is missing. "
        "It must be present before any changes are applied."
    )
    assert CONFIG_FILE.is_file(), (
        f"Expected a regular file at '{CONFIG_FILE}', but found something else."
    )

    actual_bytes = CONFIG_FILE.read_bytes()
    assert actual_bytes == expected_config_bytes, (
        "The contents of '{0}' do not match the expected initial state.\n\n"
        "Expected (hex):\n{1}\n\nActual (hex):\n{2}\n\n"
        "Ensure the file is identical to the exercise specification BEFORE "
        "you start modifying it.".format(
            CONFIG_FILE,
            expected_config_bytes.hex(),
            actual_bytes.hex(),
        )
    )

    # Optional sanity-check: file should be readable by owner and not be world-writable.
    mode = CONFIG_FILE.stat().st_mode
    assert mode & stat.S_IRUSR, f"Owner read permission is missing on '{CONFIG_FILE}'."
    assert not (mode & stat.S_IWOTH), (
        f"'{CONFIG_FILE}' is world-writable; tighten the permissions to at most 0644."
    )