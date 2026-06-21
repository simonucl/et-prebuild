# test_initial_state.py
#
# This pytest file validates the *initial* state of the operating-system /
# filesystem *before* the student performs the assignment steps.  It checks
# that the project directory exists and that the tools required to complete
# the task are available.  It intentionally does NOT look for (or against)
# any of the output artefacts the student is expected to create
# (venv/, requirements.txt, setup.log, etc.).

import os
import shutil
import subprocess
import sys
import importlib.util
import pytest

WEBAPP_DIR = "/home/user/webapp"


def _run(cmd):
    """
    Helper to run a shell command and return (returncode, stdout, stderr).
    Raises AssertionError with a meaningful message if the command cannot be
    executed at all (e.g. binary not found).
    """
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        pytest.fail(f"Required executable '{cmd[0]}' not found in PATH: {exc}")
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def test_webapp_directory_exists():
    """
    The freshly-cloned project directory must already be present so the
    student can work inside it.
    """
    assert os.path.isdir(
        WEBAPP_DIR
    ), f"Expected project directory '{WEBAPP_DIR}' to exist and be a directory."


def test_python3_available():
    """
    python3 must exist in PATH; students will use it to create the venv.
    """
    python_path = shutil.which("python3")
    assert python_path is not None, "python3 executable not found in PATH."
    # Verify it actually runs.
    rc, out, err = _run(["python3", "--version"])
    assert rc == 0, f"'python3 --version' failed with rc={rc}: {err or out}"


def test_venv_module_available():
    """
    The stdlib module 'venv' must be importable; otherwise the
    student cannot create the virtual environment.
    """
    spec = importlib.util.find_spec("venv")
    assert spec is not None, "Python standard-library module 'venv' is missing."
    # A quick import to be extra sure.
    try:
        import venv  # noqa: F401
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Unable to import 'venv' module: {exc}")


def test_pip_available_through_python_m():
    """
    pip must be invocable via 'python3 -m pip'.  We rely on this form so we do
    not depend on a separate 'pip' binary being in PATH.
    """
    rc, out, err = _run(["python3", "-m", "pip", "--version"])
    assert rc == 0, (
        "Unable to run 'python3 -m pip --version'. "
        "Ensure that pip is installed for the system Python. "
        f"stderr: {err or '<empty>'}"
    )