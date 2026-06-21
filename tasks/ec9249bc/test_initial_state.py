# test_initial_state.py
# Pytest suite to verify the filesystem is in the expected **initial** state
# before the student generates /home/user/perf_summary.log.

import os
import pytest

HOME = "/home/user"
AUTH_LOG = os.path.join(HOME, "services", "auth", "logs", "request.log")
INVENTORY_LOG = os.path.join(HOME, "services", "inventory", "logs", "request.log")

EXPECTED_AUTH_LINES = [
    "1609459201000 15",
    "1609459202000 10",
    "1609459203000 20",
    "1609459204000 5",
    "1609459205000 15",
]

EXPECTED_INVENTORY_LINES = [
    "1609459201100 30",
    "1609459202100 25",
    "1609459203100 35",
    "1609459204100 40",
]


@pytest.mark.parametrize(
    "path, description",
    [
        (os.path.join(HOME, "services", "auth", "logs"), "auth log directory"),
        (os.path.join(HOME, "services", "inventory", "logs"), "inventory log directory"),
    ],
)
def test_directories_exist(path, description):
    assert os.path.isdir(
        path
    ), f"Expected {description} to exist at absolute path {path}, but it was not found."


@pytest.mark.parametrize(
    "path, description",
    [
        (AUTH_LOG, "auth request.log"),
        (INVENTORY_LOG, "inventory request.log"),
    ],
)
def test_files_exist(path, description):
    assert os.path.isfile(
        path
    ), f"Expected {description} to exist at absolute path {path}, but it was not found."


@pytest.mark.parametrize(
    "path, expected_lines, service_name",
    [
        (AUTH_LOG, EXPECTED_AUTH_LINES, "auth"),
        (INVENTORY_LOG, EXPECTED_INVENTORY_LINES, "inventory"),
    ],
)
def test_log_contents_exact(path, expected_lines, service_name):
    """
    Verify that each log file contains exactly the expected lines, no more, no less,
    and in the correct order.
    """
    with open(path, encoding="utf-8") as f:
        actual_lines = [line.rstrip("\n") for line in f]

    assert (
        actual_lines == expected_lines
    ), (
        f"{service_name} log at {path} does not match the expected contents.\n"
        f"Expected lines:\n{expected_lines}\n\nActual lines:\n{actual_lines}"
    )