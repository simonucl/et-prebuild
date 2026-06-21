# test_initial_state.py
#
# This pytest suite verifies that the repository is in its EXPECTED **initial**
# state _before_ the student starts working on the task.  It checks
#
# 1. The dev-utils directory exists.
# 2. The two required input files are present and contain the exact, canonical
#    content that the exercise specifies.
# 3. None of the four output / artefact files is present yet.
#
# If any of these assertions fails the test output will point out precisely
# what is wrong so the learner (or the exercise author) can fix the setup
# before going on.

import os
import textwrap
import pytest

BASE_DIR = "/home/user/dev-utils"

# --------------------------------------------------------------------------- #
# Canonical file contents as given in the task description
# (All files are expected to have a single trailing LF '\n'.)
# --------------------------------------------------------------------------- #

RAW_IPS_CONTENT = textwrap.dedent("""\
    2024-02-09 12:01:11 Connection from 192.168.1.10: accepted
    2024-02-09 12:01:12 8.8.8.8 requested /favicon.ico
    WARN: suspicious activity from 10.0.0.5
    Client at 172.16.0.3 disconnected
    192.168.1.12 - - [09/Feb/2024:12:01:13] "GET /index.html"
    203.0.113.25 - possible abuse report
    INFO [client 10.1.2.3] request processed
    192.168.1.10 - - [09/Feb/2024:12:01:15] "GET /dashboard"
    ERROR - invalid credentials from 10.0.0.5
    Ping from 192.168.1.100 successful
    Session start for 100.64.0.1
    198.51.100.42 contacted support endpoint
    Heartbeat ok from 172.20.14.2
    Random noise without address
    Client 192.0.2.123 disconnected
    Another line with IP 192.168.1.12
""")

USERS_CSV_CONTENT = textwrap.dedent("""\
    id,name,department,status
    1,Alice Smith,Engineering,active
    2,Bob Jones,Engineering,active
    3,Carol White,Engineering,inactive
    4,David Black,HR,active
    5,Eva Green,Marketing,active
    6,Frank Brown,Sales,active
    7,Grace Miller,Sales,active
    8,Hank Wilson,Sales,active
    9,Ian Clark,Marketing,inactive
    10,Judy Adams,Engineering,active
    11,Kate Lewis,Engineering,active
    12,Larry Young,Engineering,active
    13,Mona Hall,HR,inactive
    14,Nick King,Marketing,active
""")

INPUT_FILES = {
    "raw_ips.log": RAW_IPS_CONTENT,
    "users.csv": USERS_CSV_CONTENT,
}

# Output files that must NOT exist yet
OUTPUT_FILES = [
    "sanitized_ips.txt",
    "dept_summary.tsv",
    "daily_report_2024-02-10.txt",
    "process.log",
]

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #


def read_file(path: str) -> str:
    """Read a text file using utf-8 encoding and return its full content."""
    with open(path, encoding="utf-8") as f:
        return f.read()


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #


def test_base_directory_exists():
    assert os.path.isdir(
        BASE_DIR
    ), f"Required directory {BASE_DIR!r} does not exist."


@pytest.mark.parametrize("filename,expected_content", INPUT_FILES.items())
def test_input_file_exists_and_is_correct(filename, expected_content):
    full_path = os.path.join(BASE_DIR, filename)
    assert os.path.isfile(
        full_path
    ), f"Input file {full_path!r} is missing."

    actual = read_file(full_path)

    # Normalise line endings to LF only for comparison, then make sure the file
    # ends with exactly one LF to catch accidental blank lines.
    expected = expected_content.replace("\r\n", "\n")
    if not expected.endswith("\n"):
        pytest.fail(
            f"Internal test error: canonical content for {filename} must end with a single LF."
        )
    assert (
        actual == expected
    ), f"Content of {full_path!r} does not match the canonical specification."


@pytest.mark.parametrize("filename", OUTPUT_FILES)
def test_output_files_do_not_exist_yet(filename):
    full_path = os.path.join(BASE_DIR, filename)
    assert not os.path.exists(
        full_path
    ), (
        f"Output file {full_path!r} should NOT exist before the student runs "
        "their solution, but it is already present."
    )