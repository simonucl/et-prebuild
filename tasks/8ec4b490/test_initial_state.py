# test_initial_state.py
#
# Pytest suite that validates the initial state of the operating system /
# filesystem before the student starts working on ticket DNS-0001.

import os
import stat
import pytest

HOME_DIR = "/home/user"
NETWORK_DATA_DIR = os.path.join(HOME_DIR, "network_data")
HOSTS_SAMPLE = os.path.join(NETWORK_DATA_DIR, "hosts_sample")
VERIFICATION_DIR = os.path.join(NETWORK_DATA_DIR, "verification")
VERIFICATION_LOG = os.path.join(VERIFICATION_DIR, "localhost_resolution.log")

EXPECTED_HOSTS_CONTENT = [
    "127.0.0.1 localhost\n",
    "::1 localhost ip6-localhost ip6-loopback\n",
]


def test_network_data_directory_exists_and_writable():
    assert os.path.isdir(
        NETWORK_DATA_DIR
    ), f"Required directory {NETWORK_DATA_DIR} is missing."
    mode = os.stat(NETWORK_DATA_DIR).st_mode
    is_writable = bool(mode & stat.S_IWUSR)
    assert is_writable, f"Directory {NETWORK_DATA_DIR} is not writable by the current user."


def test_hosts_sample_file_exists_with_expected_content():
    assert os.path.isfile(
        HOSTS_SAMPLE
    ), f"Required file {HOSTS_SAMPLE} is missing."

    with open(HOSTS_SAMPLE, "r", encoding="utf-8") as fh:
        content = fh.readlines()

    assert (
        content == EXPECTED_HOSTS_CONTENT
    ), (
        f"{HOSTS_SAMPLE} does not contain the expected lines.\n"
        f"Expected ({len(EXPECTED_HOSTS_CONTENT)} lines):\n{''.join(EXPECTED_HOSTS_CONTENT)}\n"
        f"Found ({len(content)} lines):\n{''.join(content)}"
    )


def test_verification_directory_does_not_exist_yet():
    assert not os.path.exists(
        VERIFICATION_DIR
    ), f"Directory {VERIFICATION_DIR} should not exist before the task is started."


def test_verification_log_file_does_not_exist_yet():
    assert not os.path.exists(
        VERIFICATION_LOG
    ), f"File {VERIFICATION_LOG} should not exist before the task is started."