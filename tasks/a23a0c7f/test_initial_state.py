# test_initial_state.py
#
# This test-suite verifies that the *initial* operating–system state
# has everything a student needs **before** carrying out the assignment.
#
# IMPORTANT:  These tests deliberately avoid touching any of the *output*
# targets mentioned in the instructions (/home/user/siteadmin/…).
# They only check that prerequisite tools and data are available.

import os
import pwd
import shutil
import subprocess

import pytest


@pytest.fixture(scope="session")
def dpkg_query_path():
    """
    Locate the `dpkg-query` binary.

    Returns
    -------
    str
        Absolute path to the binary.

    Raises
    ------
    pytest.SkipTest
        If the command is not present on the system.
    """
    path = shutil.which("dpkg-query")
    if not path:
        pytest.fail(
            "Required command `dpkg-query` not found in $PATH. "
            "The container must provide the Debian/Ubuntu package manager "
            "tools so the student can obtain package information."
        )
    return path


def test_bash_package_installed(dpkg_query_path):
    """
    Confirm that the `bash` package is installed and a version string
    can be retrieved with `dpkg-query -W`.
    """
    try:
        result = subprocess.run(
            [dpkg_query_path, "-W", "-f=${Status} ${Version}\\n", "bash"],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        pytest.fail(
            f"`dpkg-query` reported an error when asked about the `bash` "
            f"package:\n{exc.stderr}"
        )

    output = result.stdout.strip()
    # Expected output example: "install ok installed 5.0-6ubuntu1.2"
    parts = output.split()
    assert (
        len(parts) >= 4
    ), f"Unexpected dpkg-query output format: {output!r}"

    status_triplet = " ".join(parts[:3])
    assert (
        status_triplet == "install ok installed"
    ), f"`bash` package does not appear to be installed (status: {status_triplet!r})."

    version_str = " ".join(parts[3:])
    assert version_str, "Version string for `bash` is empty."


def test_passwd_file_exists_and_readable():
    """
    Make sure /etc/passwd exists, is a regular file, and is readable.
    """
    passwd_path = "/etc/passwd"
    assert os.path.exists(
        passwd_path
    ), "/etc/passwd is missing—cannot enumerate system users."
    assert os.path.isfile(
        passwd_path
    ), f"{passwd_path} exists but is not a regular file."
    assert os.access(
        passwd_path, os.R_OK
    ), f"File {passwd_path} is not readable."


def test_at_least_one_human_user():
    """
    Ensure that there is at least one account with UID ≥ 1000.
    The assignment requires the student to enumerate these users; if
    none exist, the task would be impossible.
    """
    human_users = [
        p.pw_name for p in pwd.getpwall() if p.pw_uid >= 1000 and p.pw_uid != 65534
    ]  # exclude the usual 'nobody' UID on Debian/Ubuntu (65534)

    assert (
        human_users
    ), "No user accounts with UID ≥ 1000 found. "
    # Provide a helpful diagnostic listing existing UIDs (if any)
    all_uids = sorted({p.pw_uid for p in pwd.getpwall()})
    assert human_users, (
        "Expected at least one non-system account (UID ≥ 1000) in /etc/passwd, "
        f"but found none. UID list present on system: {all_uids}"
    )


def test_bash_binary_available():
    """
    Verify that the `bash` executable itself is available in PATH.  Although
    the package may be installed, a missing or moved binary would break the
    student's workflow.
    """
    bash_path = shutil.which("bash")
    assert bash_path, "`bash` executable not found in $PATH."
    assert os.access(
        bash_path, os.X_OK
    ), f"`bash` binary at {bash_path} is not executable."