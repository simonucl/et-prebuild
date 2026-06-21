# test_initial_state.py
#
# Pytest suite that verifies the operating-system / filesystem state
# **before** the student starts working on the capacity-planning task.
#
# Rules enforced:
#   • The two input CSV files must already exist and contain the exact data
#     specified in the task description.
#   • The directories meant for outputs (/home/user/capacity/output/ and
#     /home/user/capacity/logs/) must NOT yet exist.
#
# Any deviation from these expectations will cause a clear, actionable test
# failure message.

import pathlib
import textwrap

import pytest

HOME = pathlib.Path("/home/user")
DATA_DIR = HOME / "capacity" / "data"
OUTPUT_DIR = HOME / "capacity" / "output"
LOGS_DIR = HOME / "capacity" / "logs"

WORKLOADS_CSV = DATA_DIR / "workloads.csv"
SERVERS_CSV = DATA_DIR / "servers.csv"


@pytest.fixture(scope="session")
def expected_workloads_content() -> str:
    """Return the exact multi-line string expected in workloads.csv."""
    return textwrap.dedent(
        """\
        workload,cpu,ram,storage
        Analytics,4,16,50
        Web,2,8,20
        Database,6,24,100
        Batch,3,12,40
        """
    ).strip()  # strip() removes the trailing newline for comparison


@pytest.fixture(scope="session")
def expected_servers_content() -> str:
    """Return the exact multi-line string expected in servers.csv."""
    return textwrap.dedent(
        """\
        server,cpu,ram,storage,cost
        alpha,8,32,200,50
        bravo,16,64,500,90
        charlie,4,16,100,30
        delta,6,24,120,40
        """
    ).strip()


def test_data_directory_exists():
    assert DATA_DIR.is_dir(), (
        f"Required data directory {DATA_DIR} is missing.\n"
        "Create it and make sure the CSV files are placed inside."
    )


def test_workloads_csv_presence_and_content(expected_workloads_content):
    assert WORKLOADS_CSV.is_file(), (
        f"Missing file: {WORKLOADS_CSV}\n"
        "Create this file with the exact workloads data provided in the task."
    )

    content = WORKLOADS_CSV.read_text(encoding="utf-8").strip()
    assert content == expected_workloads_content, (
        f"Content of {WORKLOADS_CSV} does not match the expected data.\n"
        "Verify that all rows and columns are exactly as specified."
    )


def test_servers_csv_presence_and_content(expected_servers_content):
    assert SERVERS_CSV.is_file(), (
        f"Missing file: {SERVERS_CSV}\n"
        "Create this file with the exact servers data provided in the task."
    )

    content = SERVERS_CSV.read_text(encoding="utf-8").strip()
    assert content == expected_servers_content, (
        f"Content of {SERVERS_CSV} does not match the expected data.\n"
        "Verify that all rows and columns are exactly as specified."
    )


@pytest.mark.parametrize("path", [OUTPUT_DIR, LOGS_DIR])
def test_output_and_logs_directories_do_not_exist_yet(path):
    assert not path.exists(), (
        f"The directory {path} should NOT exist before the solution runs.\n"
        "It must be created by the student's script at execution time."
    )