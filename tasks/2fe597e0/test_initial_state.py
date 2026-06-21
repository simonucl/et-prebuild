# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system / filesystem
# state *before* the student performs any task-related actions.
#
# NOTE:
#   • We intentionally do *not* reference or test for any of the paths, files
#     or directories that the student is expected to create (e.g.
#     /home/user/obs_env or package_report.log).  This keeps the checks focused
#     solely on the baseline environment that must already be in place.
#   • Only Python’s standard library and pytest are used.

import os
import subprocess
import tempfile
from pathlib import Path

HOME = Path("/home/user")


def test_home_directory_exists():
    """Ensure that the canonical home directory is present and is a directory."""
    assert HOME.exists(), f"Expected home directory {HOME} to exist, but it is missing."
    assert HOME.is_dir(), f"Expected {HOME} to be a directory."


def test_home_directory_is_writable():
    """
    Verify that /home/user is writable by attempting to create and then delete
    a temporary file in that location.
    """
    try:
        with tempfile.NamedTemporaryFile(prefix="pytest_writecheck_", dir=HOME, delete=True) as tmp:
            tmp.write(b"ok")
            tmp.flush()
            tmp.seek(0)
            assert tmp.read() == b"ok", "Failed to write/read to a file within /home/user."
    except PermissionError as exc:
        pytest.fail(f"Write permission to {HOME} is required: {exc}")


def test_python3_executable_available():
    """python3 must be available on the PATH and callable."""
    result = subprocess.run(
        ["python3", "--version"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert result.returncode == 0, (
        "python3 executable not found or not callable. "
        f"stdout: {result.stdout!r} stderr: {result.stderr!r}"
    )
    # The version string is usually in stdout for newer Python releases, but may
    # appear in stderr on some systems; combine for robustness.
    combined = f"{result.stdout} {result.stderr}".lower()
    assert "python" in combined, (
        "Unexpected output from 'python3 --version'; could not detect a Python version."
    )


def test_venv_module_is_available():
    """The standard library 'venv' module must be importable for virtualenv creation."""
    try:
        import venv  # noqa: F401
    except ImportError as exc:
        pytest.fail(
            "The standard library 'venv' module is required to create a virtual "
            f"environment but could not be imported: {exc}"
        )


def test_pip_module_usable():
    """
    Ensure that the built-in `python3 -m pip` command is operational.
    We do not check any package versions here—only that pip itself starts.
    """
    result = subprocess.run(
        ["python3", "-m", "pip", "--version"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert result.returncode == 0, (
        "`python3 -m pip` failed. Make sure pip is installed and functional.\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )