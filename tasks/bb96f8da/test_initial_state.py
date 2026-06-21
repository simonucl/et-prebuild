# test_initial_state.py
#
# Pytest suite that verifies the initial filesystem state **before** the
# student tackles the task.  It checks that all prerequisite files and
# directories are present and correct, and that no result file exists yet.

import os
import stat
import textwrap
import pytest

HOME = "/home/user"
NT_DIR = os.path.join(HOME, "network_targets")
SR_DIR = os.path.join(HOME, "scan_reports")
SAMPLE_FILE = os.path.join(NT_DIR, "sample_nmap_output.txt")
OUTPUT_FILE = os.path.join(SR_DIR, "open_ports.csv")


@pytest.fixture(scope="session")
def sample_file_expected_content():
    # The exact content that must be present in the sample Nmap output file.
    # A final newline *is* part of the expected content.
    return textwrap.dedent(
        """\
        Starting Nmap 7.93 ( https://nmap.org ) at 2023-06-15 12:34 UTC
        Nmap scan report for localhost (127.0.0.1)
        Host is up (0.000093s latency).
        Not shown: 995 closed tcp ports (reset)
        PORT     STATE SERVICE
        22/tcp   open  ssh
        25/tcp   filtered smtp
        80/tcp   open  http
        111/tcp  open  rpcbind
        139/tcp  closed netbios-ssn
        443/tcp  open  https
        3306/tcp open  mysql

        Nmap done: 1 IP address (1 host up) scanned in 0.19 seconds
        """
    )


def _mode(path):
    """Return the permission bits (e.g. 0o644) of a filesystem entry."""
    return stat.S_IMODE(os.stat(path).st_mode)


def test_directories_exist_with_correct_permissions():
    # 1. /home/user/network_targets
    assert os.path.isdir(
        NT_DIR
    ), f"Required directory missing: {NT_DIR!r}"

    dir_mode = _mode(NT_DIR)
    assert (
        dir_mode == 0o755
    ), f"Directory {NT_DIR!r} should have permissions 755, found {oct(dir_mode)}."

    # 2. /home/user/scan_reports
    assert os.path.isdir(
        SR_DIR
    ), f"Required directory missing: {SR_DIR!r}"

    dir_mode = _mode(SR_DIR)
    assert (
        dir_mode == 0o755
    ), f"Directory {SR_DIR!r} should have permissions 755, found {oct(dir_mode)}."


def test_sample_nmap_output_file_exists_and_is_correct(sample_file_expected_content):
    assert os.path.isfile(
        SAMPLE_FILE
    ), f"Sample Nmap output file missing: {SAMPLE_FILE!r}"

    file_mode = _mode(SAMPLE_FILE)
    assert (
        file_mode == 0o644
    ), f"File {SAMPLE_FILE!r} should have permissions 644, found {oct(file_mode)}."

    with open(SAMPLE_FILE, "r", encoding="utf-8") as fh:
        actual_content = fh.read()

    expected_content = sample_file_expected_content
    # Ensure the file ends with a single trailing newline.
    assert actual_content.endswith(
        "\n"
    ), f"File {SAMPLE_FILE!r} must end with a single trailing newline."

    assert (
        actual_content == expected_content
    ), f"Content of {SAMPLE_FILE!r} does not match the expected Nmap output."


def test_output_file_does_not_exist_yet():
    assert not os.path.exists(
        OUTPUT_FILE
    ), f"Output CSV file {OUTPUT_FILE!r} should NOT exist before the student runs their solution."