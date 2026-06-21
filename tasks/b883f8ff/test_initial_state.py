# test_initial_state.py
#
# This test-suite validates the baseline environment *before* the student
# begins work on the ETL automation exercise.  It deliberately avoids any
# reference to the files or directories the student is expected to create
# (see developer instructions).  Instead, it checks that the underlying
# operating-system prerequisites are in place so the student can complete
# the task without hindrance.

import os
import json
import subprocess


def test_python3_binary_exists_and_is_executable():
    """
    The task’s cron entry explicitly calls `/usr/bin/python3`, so that exact
    path must exist *and* be executable.
    """
    python_path = "/usr/bin/python3"

    assert os.path.isfile(
        python_path
    ), (
        f"Expected a Python interpreter at {python_path}, "
        "but no file exists there."
    )

    assert os.access(
        python_path, os.X_OK
    ), (
        f"{python_path} exists but is not marked executable. "
        "It must have its executable bit set."
    )


def test_python3_is_version_3():
    """
    Guard against misconfigured symlinks that might point `/usr/bin/python3`
    at a non-Python-3 interpreter.
    """
    completed = subprocess.run(
        ["/usr/bin/python3", "-c", "import sys, json; print(json.dumps(sys.version_info[:3]))"],
        capture_output=True,
        text=True,
        timeout=10,
    )

    assert completed.returncode == 0, (
        "Failed to execute /usr/bin/python3 to determine its version."
    )

    try:
        major, minor, micro = json.loads(completed.stdout.strip())
    except Exception as exc:  # pragma: no cover
        raise AssertionError(
            "Could not parse the version information emitted by /usr/bin/python3."
        ) from exc

    assert major == 3, (
        f"/usr/bin/python3 must be a Python 3 interpreter; found major version {major}."
    )


def test_home_directory_exists_and_is_writable():
    """
    The student needs a writable home directory (/home/user) in order to
    create the ETL artefacts.  We therefore check that it both exists and is
    writable by the current user.
    """
    home_path = "/home/user"

    assert os.path.isdir(
        home_path
    ), f"The home directory {home_path} does not exist."

    assert os.access(
        home_path, os.W_OK
    ), (
        f"The home directory {home_path} is not writable. "
        "Write permission is required for the student to create files there."
    )