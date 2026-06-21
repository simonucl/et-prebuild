# test_initial_state.py
#
# Pytest suite that verifies the initial operating-system state
# BEFORE the student attempts the exercise.  These tests make sure
# that the provided INI file exists exactly as specified so the
# subsequent solution can rely on it.
#
# NOTE:  As required, we do NOT test for the presence of the
#        output file (/home/user/service_report.log).

from pathlib import Path
import pytest

HOME = Path("/home/user")
INI_DIR = HOME / "server_configs"
INI_FILE = INI_DIR / "appserver.ini"


@pytest.fixture(scope="module")
def ini_contents():
    """
    Read the contents of the INI file once for all tests.
    """
    if not INI_FILE.exists():
        pytest.fail(
            f"Required file {INI_FILE} is missing. "
            "It must be present before the task begins."
        )
    try:
        return INI_FILE.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {INI_FILE}: {exc}")


def test_server_configs_directory_exists():
    """
    Verify that /home/user/server_configs exists and is a directory.
    """
    assert INI_DIR.exists(), (
        f"Directory {INI_DIR} is missing. "
        "Create it or place the INI file elsewhere."
    )
    assert INI_DIR.is_dir(), f"{INI_DIR} exists but is not a directory."


def test_appserver_ini_exists():
    """
    Verify that /home/user/server_configs/appserver.ini exists and is a file.
    """
    assert INI_FILE.exists(), f"Expected file {INI_FILE} to exist."
    assert INI_FILE.is_file(), f"{INI_FILE} exists but is not a regular file."


def test_appserver_ini_contents_exact(ini_contents):
    """
    Ensure the INI file content EXACTLY matches what the specification states
    (ignoring the presence or absence of a final trailing newline).
    """
    expected_content = (
        "[web]\n"
        "enabled = true\n"
        "port = 8080\n"
        "\n"
        "[db]\n"
        "enabled = false\n"
        "port = 5432\n"
        "\n"
        "[cache]\n"
        "enabled = true\n"
        "port = 6379\n"
    )

    # Strip exactly one optional trailing newline from both
    actual = ini_contents.rstrip("\n")
    expected = expected_content.rstrip("\n")

    assert (
        actual == expected
    ), (
        "The content of /home/user/server_configs/appserver.ini does not match "
        "the expected initial state.\n\n"
        "----- Expected -----\n"
        f"{expected_content}"
        "--------------------\n\n"
        "----- Actual -----\n"
        f"{ini_contents}"
        "------------------"
    )