# test_initial_state.py
"""
Pytest suite that verifies the expected *initial* state of the execution
environment **before** the learner runs their solution.

What we check (and why):
1. The canonical home directory (/home/user) exists – this is the base
   location for all subsequent work.
2. NumPy is already importable and reports version 1.24.2 – this is the
   version that must be captured later by the learner.
3. `python -m pip show numpy` also reports the exact same version – this
   mimics how the learner will query the version from the CLI.

We intentionally do *not* touch /home/user/training_env or any file
inside it, because those are artifacts the learner is expected to create.
"""

import os
import subprocess
import sys

import pytest


HOME_DIR = "/home/user"
EXPECTED_NUMPY_VERSION = "1.24.2"


def test_home_directory_exists():
    """
    Ensure the canonical home directory is present.  This is a basic sanity
    check so that later instructions referring to /home/user make sense.
    """
    assert os.path.isdir(
        HOME_DIR
    ), f"Expected the home directory {HOME_DIR!r} to exist, but it is missing."


def test_numpy_import_version():
    """
    Verify that NumPy can be imported and that its __version__ attribute
    matches the expected version (1.24.2).
    """
    try:
        import numpy as np  # type: ignore
    except ImportError as exc:
        pytest.fail(f"NumPy should be pre-installed, but 'import numpy' failed: {exc}")

    actual_version = getattr(np, "__version__", None)
    assert (
        actual_version == EXPECTED_NUMPY_VERSION
    ), f"Imported NumPy reports version {actual_version!r}, expected {EXPECTED_NUMPY_VERSION!r}."


def test_pip_show_numpy_version():
    """
    Confirm that `python -m pip show numpy` reports the same version.
    This aligns with how the learner will query the version in their shell
    command.
    """
    cmd = [sys.executable, "-m", "pip", "show", "numpy"]
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
    except FileNotFoundError as exc:
        pytest.fail(f"pip is not available via 'python -m pip': {exc}")
    except subprocess.CalledProcessError as exc:
        pytest.fail(
            f"Running {' '.join(cmd)!r} failed with exit code {exc.returncode}:\n"
            f"stdout:\n{exc.stdout}\n"
            f"stderr:\n{exc.stderr}"
        )

    version_line = next(
        (line for line in result.stdout.splitlines() if line.startswith("Version:")), None
    )
    assert (
        version_line is not None
    ), "'pip show numpy' did not contain a 'Version:' line. Full output:\n" + result.stdout

    _, _, reported_version = version_line.partition(":")
    reported_version = reported_version.strip()

    assert (
        reported_version == EXPECTED_NUMPY_VERSION
    ), f"'pip show numpy' reports version {reported_version!r}, expected {EXPECTED_NUMPY_VERSION!r}."