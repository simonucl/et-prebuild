# test_initial_state.py
#
# This pytest suite verifies that the execution environment is ready
# for the student to implement the health-check task.  It makes **no**
# assertions about the artefacts that the student is expected to
# create later (e.g., /home/user/uptime or any log files); those paths
# are deliberately *not* referenced here, in accordance with the task
# authoring guidelines.

import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pytest

HOME = Path("/home/user")
CURL_BIN_CANDIDATES = (
    "/usr/bin/curl",
    "/bin/curl",
    shutil.which("curl") or "",
)


def _first_existing_executable(paths):
    """Return the first path that exists and is executable, else None."""
    for p in paths:
        if p and os.path.isfile(p) and os.access(p, os.X_OK):
            return p
    return None


@pytest.fixture(scope="session")
def curl_path():
    """
    Locate the curl binary that should be used for subsequent tests.

    Fails early with a clear message if curl is not available or not
    executable.
    """
    path = _first_existing_executable(CURL_BIN_CANDIDATES)
    assert path is not None, (
        "curl was not found in any of the expected locations. "
        "Ensure that curl is installed and accessible."
    )
    return path


def test_home_directory_exists_and_is_writable():
    """
    Validate that the base home directory exists, is a directory, and
    is writable by the current user.  This is a pre-requisite for
    creating the /home/user/uptime directory later.
    """
    assert HOME.exists(), f"Expected home directory {HOME} does not exist."
    assert HOME.is_dir(), f"{HOME} exists but is not a directory."
    # Attempt to create and delete a temporary file to verify write perms.
    temp_file = HOME / f".pytest_tmp_{int(time.time() * 1000)}"
    try:
        with open(temp_file, "w") as fh:
            fh.write("touch")
    except PermissionError as exc:
        pytest.fail(
            f"Home directory {HOME} is not writable by the current user: {exc}"
        )
    finally:
        temp_file.unlink(missing_ok=True)


def test_curl_is_installed_and_executable(curl_path):
    """Simple sanity check that we can run `curl --version`."""
    proc = subprocess.run(
        [curl_path, "--version"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=10,
    )
    assert proc.returncode == 0, (
        f"curl exists at {curl_path} but could not be executed. "
        f"stderr: {proc.stderr}"
    )
    assert "curl" in proc.stdout.lower(), "Unexpected output from curl --version."


def test_example_dot_com_is_reachable_with_curl(curl_path):
    """
    The assignment relies on example.com returning HTTP 200.
    Perform a lightweight HEAD request and confirm the HTTP status.
    """
    # Use --head to avoid downloading the entire body.
    proc = subprocess.run(
        [curl_path, "--head", "-s", "-o", "/dev/null", "-w", "%{http_code}", "https://example.com/"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=20,
    )
    assert proc.returncode == 0, (
        "curl could not complete the request to https://example.com/.\n"
        f"stderr: {proc.stderr}"
    )
    status_code_str = proc.stdout.strip()
    assert status_code_str.isdigit(), (
        "Did not receive a numeric HTTP status code from curl when probing "
        "https://example.com/."
    )
    status_code = int(status_code_str)
    assert status_code == 200, (
        f"Expected HTTP 200 from https://example.com/ but got {status_code}."
    )