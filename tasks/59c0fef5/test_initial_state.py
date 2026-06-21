# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating-system
# before the student performs any of the required steps described in the
# assignment.
#
# The checks deliberately assert that none of the **target** artefacts
# (.env, print_env.sh, env_output.log) are present yet.  If any of them
# already exist, or already contain the final-expected content, the
# student would not be starting from a clean slate and the test must fail
# with a clear explanation.
#
# Only the presence of the base directory /home/user/app is required at
# this stage.

import os
import stat
import textwrap
import pytest


APP_DIR = "/home/user/app"
ENV_FILE = os.path.join(APP_DIR, ".env")
SCRIPT_FILE = os.path.join(APP_DIR, "print_env.sh")
LOG_FILE = os.path.join(APP_DIR, "env_output.log")

# Expected final contents (should *not* exist yet).
EXPECTED_LINES = textwrap.dedent(
    """\
    APP_ENV=production
    DB_HOST=127.0.0.1
    DB_PORT=5432
    SECRET_KEY=supersecret
    """
).splitlines(keepends=True)


def _has_expected_content(path: str) -> bool:
    """
    Helper: return True if the file at *path* exists and its entire
    contents byte-for-byte match the final expected lines (including the
    terminating newline).
    """
    if not os.path.isfile(path):
        return False

    try:
        with open(path, "rb") as fp:
            data = fp.read()
    except (OSError, IOError):
        return False

    return data == "".join(EXPECTED_LINES).encode()


def test_app_directory_exists():
    assert os.path.isdir(
        APP_DIR
    ), f"Expected base directory {APP_DIR!r} to exist before starting."


@pytest.mark.parametrize(
    "path,description",
    [
        (ENV_FILE, "configuration file '.env'"),
        (SCRIPT_FILE, "helper script 'print_env.sh'"),
        (LOG_FILE, "log file 'env_output.log'"),
    ],
)
def test_target_files_absent(path, description):
    """
    None of the artefacts required for the *final* state should be present
    yet.  If they already exist, the student is not starting from a clean
    environment.
    """
    assert not os.path.exists(
        path
    ), f"The {description} ({path}) already exists; start with a clean slate."


def test_script_not_executable_if_accidentally_present():
    """
    Defensive check: if for some reason the helper script exists,
    ensure it is *not* already executable and does *not* match the
    expected final content.  This gives an explanatory failure instead of
    silently passing the previous parametrised test (which only checks
    for existence).
    """
    if not os.path.exists(SCRIPT_FILE):
        pytest.skip("Script file does not exist (as expected).")

    # File exists: make sure it's not yet executable.
    is_executable = os.stat(SCRIPT_FILE).st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    assert (
        not is_executable
    ), f"{SCRIPT_FILE} is already executable; this should happen only after the student completes the task."

    # Also ensure it does not already contain the final expected lines.
    assert not _has_expected_content(
        SCRIPT_FILE
    ), f"{SCRIPT_FILE} already contains the expected final output; please start from a clean state."


def test_env_file_not_prepopulated():
    """
    If a .env file exists for other reasons, verify that it does *not*
    already contain the final-expected four lines.  The student must be
    the one who creates/populates it.
    """
    if not os.path.exists(ENV_FILE):
        pytest.skip(".env file does not exist (as expected).")

    assert not _has_expected_content(
        ENV_FILE
    ), f"{ENV_FILE} already contains the final-expected variables; it should start empty or absent."