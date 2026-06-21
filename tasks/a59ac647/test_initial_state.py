# test_initial_state.py
#
# This pytest module validates the *initial* operating-system / filesystem
# state **before** the student performs any actions for the “release-manager”
# task.  It asserts the presence and behaviour of the pre-existing legacy
# deployment script and does **not** look for any artefacts the student is
# expected to create later.

import os
import subprocess
import stat
import pytest

HOME = "/home/user"
LEGACY_DIR = os.path.join(HOME, "old_code")
LEGACY_SCRIPT = os.path.join(LEGACY_DIR, "release.sh")
EXPECTED_VERSION_OUTPUT = "old_code release v0.9.8\n"


def test_legacy_directory_exists():
    assert os.path.isdir(LEGACY_DIR), (
        f"Expected legacy directory '{LEGACY_DIR}' is missing."
    )


def test_release_script_exists_and_is_file():
    assert os.path.isfile(LEGACY_SCRIPT), (
        f"Expected script '{LEGACY_SCRIPT}' does not exist or is not a regular file."
    )


def test_release_script_is_executable():
    st = os.stat(LEGACY_SCRIPT)
    is_executable = bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert is_executable, (
        f"Script '{LEGACY_SCRIPT}' exists but is not marked as executable."
    )


def test_release_script_version_output_matches_exactly():
    try:
        completed = subprocess.run(
            [LEGACY_SCRIPT, "--version"],
            check=True,
            text=True,
            capture_output=True,
        )
    except FileNotFoundError:
        pytest.fail(f"Could not execute '{LEGACY_SCRIPT}' – file not found.")
    except PermissionError:
        pytest.fail(f"Could not execute '{LEGACY_SCRIPT}' – permission denied.")
    except subprocess.CalledProcessError as exc:
        pytest.fail(
            f"Execution of '{LEGACY_SCRIPT} --version' failed with exit status "
            f"{exc.returncode}. Stderr:\n{exc.stderr}"
        )

    stdout = completed.stdout
    assert stdout == EXPECTED_VERSION_OUTPUT, (
        "Version string mismatch.\n"
        f"Expected: {EXPECTED_VERSION_OUTPUT!r}\n"
        f"Received: {stdout!r}"
    )