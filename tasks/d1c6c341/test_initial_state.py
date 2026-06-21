# test_initial_state.py
#
# This pytest suite validates that the *initial* execution environment is sane
# and ready for the student to carry out the workflow-automation task.
#
# IMPORTANT:  We deliberately do **not** look for any of the artefacts the
#             student must create later (/home/user/workflows, the virtual
#             environment, log files, etc.).  These would be “output”
#             objects and are therefore excluded from the initial-state
#             checks according to the grading rubric.
#
# The tests below confine themselves to things that *must already be true*:
# • the basic /home/user directory is present and writable
# • a usable python3 interpreter is on PATH
# • the stdlib “venv” module can be imported (needed for virtual-env creation)
#
# Any failure message should give a clear hint about what prerequisite is
# missing or mis-configured.

import os
import shutil
import tempfile
import subprocess
import sys
import importlib.util
import pytest


HOME_DIR = "/home/user"


def _assert(condition: bool, message: str) -> None:
    """
    Helper that wraps a bare assert with a more descriptive failure message.
    """
    assert condition, message


def test_home_directory_exists_and_is_dir():
    """
    The canonical home directory (/home/user) must exist and be a directory.
    """
    _assert(
        os.path.exists(HOME_DIR),
        f"Expected {HOME_DIR} to exist, but it was not found."
    )
    _assert(
        os.path.isdir(HOME_DIR),
        f"{HOME_DIR} exists but is not a directory."
    )


def test_home_directory_is_writable():
    """
    The student will need to create sub-directories and files; make sure /home/user is writable.
    """
    try:
        tmp_path = tempfile.mkdtemp(dir=HOME_DIR)
    except PermissionError as exc:
        pytest.fail(f"{HOME_DIR} is not writable: {exc}")
    finally:
        # Clean up only if creation succeeded.
        if 'tmp_path' in locals() and os.path.isdir(tmp_path):
            shutil.rmtree(tmp_path, ignore_errors=True)


def test_python3_on_path_and_executable():
    """
    A 'python3' executable must be discoverable via PATH and invokable.
    """
    python_exe = shutil.which("python3")
    _assert(
        python_exe is not None,
        "'python3' was not found on PATH; ensure Python ≥3.6 is installed."
    )

    # Try `python3 -V` to confirm it runs.
    try:
        completed = subprocess.run(
            [python_exe, "-V"],
            capture_output=True,
            check=True,
            text=True
        )
    except (OSError, subprocess.SubprocessError) as exc:
        pytest.fail(f"Invoking '{python_exe} -V' failed: {exc}")

    _assert(
        completed.returncode == 0,
        f"'python3 -V' returned non-zero exit code: {completed.returncode}"
    )


def test_venv_module_is_available():
    """
    The stdlib 'venv' module must be importable so the student can create
    the required virtual environment.
    """
    spec = importlib.util.find_spec("venv")
    _assert(
        spec is not None,
        "Cannot import the stdlib 'venv' module; it is required for this task."
    )