# test_initial_state.py
#
# This pytest file validates the starting environment **before** the student
# runs any solution code.  It checks that the datasets/logs directory and the
# master acquisition file exist with the correct permissions and exact
# contents.  It deliberately avoids looking for (or at) the eventual output
# file `success_2023.log`, so as not to interfere with the assessment of the
# student’s work.

import os
import stat
import pytest

LOGS_DIR = "/home/user/datasets/logs"
COLLECTION_FILE = os.path.join(LOGS_DIR, "collection.log")

EXPECTED_DIR_MODE = 0o755
EXPECTED_FILE_MODE = 0o644

# Expected exact contents (each line must be terminated by a single LF '\n')
EXPECTED_LINES = [
    "[2023-02-14 10:12:03] SUCCESS BirdID: BD1001 URL: https://example.com/birds/BD1001.wav\n",
    "[2023-03-01 07:45:56] SUCCESS BirdID: BD1042 URL: https://example.com/birds/BD1042.wav\n",
    "[2023-04-22 19:10:11] SUCCESS BirdID: BD1100 URL: https://example.com/birds/BD1100.wav\n",
    "[2023-06-30 22:51:42] SUCCESS BirdID: BD1155 URL: https://example.com/birds/BD1155.wav\n",
    "[2023-12-01 05:02:29] SUCCESS BirdID: BD1300 URL: https://example.com/birds/BD1300.wav\n",
    "[2022-11-20 08:00:00] SUCCESS BirdID: BD0900 URL: https://example.com/birds/BD0900.wav\n",
    "[2023-01-02 12:00:07] FAIL    BirdID: BD1002 URL: https://example.com/birds/BD1002.wav\n",
    "[2023-05-15 15:30:22] FAIL    BirdID: BD1120 URL: https://example.com/birds/BD1120.wav\n",
    "[2021-07-14 03:03:03] SUCCESS BirdID: BD0500 URL: https://example.com/birds/BD0500.wav\n",
]


def _mode(path):
    """Return the permission bits (e.g., 0o755) for the given file/directory."""
    return stat.S_IMODE(os.stat(path).st_mode)


def test_logs_directory_exists_and_has_correct_permissions():
    assert os.path.isdir(LOGS_DIR), (
        f"Required directory '{LOGS_DIR}' does not exist or is not a directory."
    )
    mode = _mode(LOGS_DIR)
    assert mode == EXPECTED_DIR_MODE, (
        f"Directory '{LOGS_DIR}' has permissions {oct(mode)}, "
        f"but expected {oct(EXPECTED_DIR_MODE)}."
    )


def test_collection_file_exists_and_has_correct_permissions():
    assert os.path.isfile(COLLECTION_FILE), (
        f"Required file '{COLLECTION_FILE}' does not exist."
    )
    mode = _mode(COLLECTION_FILE)
    assert mode == EXPECTED_FILE_MODE, (
        f"File '{COLLECTION_FILE}' has permissions {oct(mode)}, "
        f"but expected {oct(EXPECTED_FILE_MODE)}."
    )


def test_collection_file_exact_contents():
    # Read in binary first to make sure there are no CR characters.
    with open(COLLECTION_FILE, "rb") as bf:
        raw = bf.read()
    assert b"\r" not in raw, (
        f"File '{COLLECTION_FILE}' must use Unix LF line endings only, "
        "but CR characters were found."
    )

    # Decode safely now that we know line endings are clean.
    text = raw.decode("utf-8")
    lines = text.splitlines(keepends=True)

    assert lines == EXPECTED_LINES, (
        f"File '{COLLECTION_FILE}' contents do not match the expected 9 lines "
        "exactly. Differences detected."
    )