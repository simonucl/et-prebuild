# test_initial_state.py
#
# This test-suite verifies that the machine is in the correct *initial*
# condition **before** the student executes any of the required backup /
# restore commands.  It intentionally does NOT look for the final artefacts
# that the student must create, only for resources that have to be present
# from the outset (e.g. writable directories and essential tooling).
#
# Requirements checked:
#   1. The directory /home/user/backups exists and is writable.
#   2. The venv module is available so a virtual environment can be created.
#   3. A working Python 3 interpreter is on PATH.
#   4. pip (via “python3 -m pip”) is operational.
#
# No third-party modules are used; only the Python standard library and
# pytest are required.

import os
import shutil
import subprocess
import sys

import pytest


BACKUP_DIR = "/home/user/backups"


def _run(cmd):
    """
    Helper that runs *cmd* (a list of str) and returns (rc, stdout, stderr).
    All streams are captured as text, **not** bytes.
    """
    completed = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )
    return completed.returncode, completed.stdout, completed.stderr


def test_backup_directory_exists():
    """
    The backup directory must already exist so the student can write the two
    required artefacts there.  We also check writability in case the test
    runner mounted the directory read-only by mistake.
    """
    assert os.path.isdir(
        BACKUP_DIR
    ), f"Expected directory '{BACKUP_DIR}' to exist, but it is missing."

    assert os.access(
        BACKUP_DIR, os.W_OK
    ), f"Directory '{BACKUP_DIR}' is not writable; please adjust permissions."


def test_venv_module_is_available():
    """
    A virtual environment is needed to perform the package backup and
    restoration.  The stdlib 'venv' module must therefore be importable.
    """
    try:
        import venv  # noqa: F401 (imported for its side-effect: validation)
    except ImportError:
        pytest.fail(
            "The standard library module 'venv' is missing. "
            "Python installation appears to be incomplete."
        )


def test_python3_on_path():
    """
    Ensure that a Python 3 interpreter is discoverable via PATH.  This is the
    interpreter that will ultimately run 'python3 -m venv' and 'python3 -m pip'.
    """
    python_exe = shutil.which("python3")
    assert python_exe is not None, (
        "No 'python3' executable found on PATH. "
        "A working Python 3 interpreter is required."
    )

    # Double-check we can execute it.
    rc, out, err = _run([python_exe, "--version"])
    assert rc == 0, (
        f"Executing '{python_exe} --version' failed with return code {rc}. "
        f"stderr was:\n{err}"
    )
    assert out.startswith("Python 3") or err.startswith(
        "Python 3"
    ), "The interpreter found is not Python 3."


def test_python3_pip_is_functional():
    """
    pip is required to install the exact package versions.  Invoke
    'python3 -m pip --version' to verify that pip is functional.
    """
    python_exe = shutil.which("python3")
    assert python_exe is not None, "Internal error: 'python3' disappeared from PATH."

    rc, out, err = _run([python_exe, "-m", "pip", "--version"])
    assert rc == 0, (
        f"'python3 -m pip --version' failed with return code {rc}. "
        f"stderr was:\n{err}\n"
        "pip must be available so packages can be installed."
    )

    assert "pip" in out.lower(), (
        "Output of 'python3 -m pip --version' did not mention 'pip'. "
        "pip does not appear to be installed correctly."
    )