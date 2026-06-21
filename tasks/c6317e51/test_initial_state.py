# test_initial_state.py
#
# This pytest suite validates the *initial* state of the CI runner
# before the student performs any action.  It checks that:
#
# 1. The `curl` package is installed.
# 2. The installed version is exactly `7.74.0-1ubuntu2.18`.
# 3. The status in `dpkg -s curl` reports “install ok installed”.
# 4. The output file the student is expected to create
#    (/home/user/curl_version.log) does NOT exist yet.
#
# Any deviation from these expectations will surface as a clear,
# informative assertion failure.

import subprocess
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def curl_version_from_dpkg_query():
    """
    Returns the version string reported by
        dpkg-query -W -f=${Version}\n curl
    """
    try:
        output = subprocess.check_output(
            ["dpkg-query", "-W", "-f=${Version}\n", "curl"],
            text=True,
            stderr=subprocess.STDOUT,
        ).strip()
    except FileNotFoundError as exc:  # dpkg-query not present
        pytest.fail(
            "The command `dpkg-query` is not available on this system. "
            "Cannot verify initial package state."
        )
    except subprocess.CalledProcessError as exc:
        pytest.fail(
            "Failed to run `dpkg-query` for curl. Output was:\n"
            f"{exc.output}"
        )

    return output


def test_curl_package_status_is_installed():
    """dpkg -s curl reports 'install ok installed'."""
    completed = subprocess.run(
        ["dpkg", "-s", "curl"],
        capture_output=True,
        text=True,
    )

    assert (
        completed.returncode == 0
    ), "The `curl` package is not registered in dpkg."

    assert (
        "Status: install ok installed" in completed.stdout
    ), (
        "Expected `curl` to be in state 'install ok installed', "
        "but dpkg -s output was:\n"
        f"{completed.stdout}"
    )


def test_curl_version_matches_expected(curl_version_from_dpkg_query):
    """curl is at the exact expected version."""
    expected_version = "7.74.0-1ubuntu2.18"
    assert (
        curl_version_from_dpkg_query == expected_version
    ), (
        "The installed curl version is different from the expected one.\n"
        f"Expected: {expected_version}\n"
        f"Found   : {curl_version_from_dpkg_query}"
    )


def test_log_file_does_not_exist_yet():
    """The output file should not exist before the student creates it."""
    log_path = Path("/home/user/curl_version.log")

    assert not log_path.exists(), (
        "The file /home/user/curl_version.log already exists. "
        "The initial state should contain *no* such file."
    )