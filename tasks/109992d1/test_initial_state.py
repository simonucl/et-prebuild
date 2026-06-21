# test_initial_state.py
#
# This pytest suite validates that the execution environment is ready
# for the student’s one-liner.  It checks:
#   1. The base home directory (/home/user) exists.
#   2. The report directory (/home/user/observability/reports) already exists.
#   3. The Python package “prometheus-client” is installed at version 0.19.0
#      and is discoverable through both importlib.metadata and
#      `python3 -m pip show`.
#
# NOTE:  The tests purposely DO NOT look for the log file that the student
#        must create; they only verify the initial, pre-exercise state.
#
# The tests rely *only* on the Python standard library and pytest.

import subprocess
import sys
from pathlib import Path

import pytest

HOME_DIR = Path("/home/user")
REPORT_DIR = HOME_DIR / "observability" / "reports"
EXPECTED_VERSION = "0.19.0"
PACKAGE_NAME = "prometheus-client"


def test_home_directory_exists():
    """Ensure the /home/user directory exists."""
    assert HOME_DIR.is_dir(), (
        f"Expected home directory {HOME_DIR} to exist as a directory, "
        "but it is missing."
    )


def test_report_directory_exists():
    """Ensure /home/user/observability/reports exists prior to the exercise."""
    assert REPORT_DIR.is_dir(), (
        "The directory expected to hold the log file is missing:\n"
        f"  {REPORT_DIR}\n"
        "The grader guarantees this directory should already exist. "
        "Create it before running the exercise setup."
    )


def _get_version_via_importlib():
    """Return the package version using importlib.metadata (Python ≥3.8)."""
    try:
        # Python 3.8+
        from importlib import metadata as importlib_metadata  # type: ignore
    except ImportError:  # pragma: no cover
        # Very old Python; fall back to pkg_resources
        import pkg_resources  # type: ignore

        return pkg_resources.get_distribution(PACKAGE_NAME).version

    return importlib_metadata.version(PACKAGE_NAME)


def test_prometheus_client_installed_correct_version_importlib():
    """Verify the installed version via importlib.metadata."""
    version = _get_version_via_importlib()
    assert (
        version == EXPECTED_VERSION
    ), f"prometheus-client version mismatch (importlib): expected {EXPECTED_VERSION}, found {version!r}"


def test_prometheus_client_installed_correct_version_pip_show():
    """
    Verify pip reports the correct version.
    This mirrors the exact command the student will run.
    """
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", PACKAGE_NAME],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as exc:  # pragma: no cover
        pytest.fail(
            f"Failed to execute 'python3 -m pip show {PACKAGE_NAME}'. "
            f"Exit code: {exc.returncode}\nstdout:\n{exc.stdout}\nstderr:\n{exc.stderr}"
        )

    stdout_lines = result.stdout.splitlines()

    # Build a dict of key/value pairs from pip show output
    info = {}
    for line in stdout_lines:
        if ":" in line:
            key, value = [part.strip() for part in line.split(":", 1)]
            info[key] = value

    missing_keys = {"Name", "Version"} - info.keys()
    assert not missing_keys, (
        "The following expected fields are missing from "
        f"'pip show {PACKAGE_NAME}' output: {', '.join(sorted(missing_keys))}\n"
        "Full output:\n" + result.stdout
    )

    assert (
        info["Name"] == PACKAGE_NAME
    ), f"Expected package name 'prometheus-client' but got '{info['Name']}'"
    assert (
        info["Version"] == EXPECTED_VERSION
    ), f"prometheus-client version mismatch (pip show): expected {EXPECTED_VERSION}, found {info['Version']}"