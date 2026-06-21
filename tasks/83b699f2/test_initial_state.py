# test_initial_state.py
#
# This pytest suite validates the initial state of the operating system
# before the student’s automation runs.
#
# What we check:
#   • /home/user/logs/access.log exists and is a regular file.
#   • The file contains exactly the ten expected lines (including the
#     terminating newline characters).
#   • The count of lines whose HTTP status code is 404 equals 3.
#
# We deliberately DO NOT reference anything inside /home/user/alerts/
# because those paths are supposed to be created by the student later.

import gzip
from pathlib import Path

import pytest


ACCESS_LOG_PATH = Path("/home/user/logs/access.log")

EXPECTED_LINES = [
    "127.0.0.1 - - [12/May/2023:06:25:24 +0000] \"GET /index.html HTTP/1.1\" 200 1024\n",
    "127.0.0.1 - - [12/May/2023:06:25:25 +0000] \"GET /favicon.ico HTTP/1.1\" 404 209\n",
    "192.168.0.5 - - [12/May/2023:06:25:26 +0000] \"GET /missing.png HTTP/1.1\" 404 512\n",
    "10.0.0.1 - - [12/May/2023:06:25:27 +0000] \"POST /login HTTP/1.1\" 200 2048\n",
    "10.0.0.2 - - [12/May/2023:06:25:28 +0000] \"GET /dashboard HTTP/1.1\" 301 342\n",
    "172.16.0.3 - - [12/May/2023:06:25:29 +0000] \"GET /secret HTTP/1.1\" 403 128\n",
    "127.0.0.1 - - [12/May/2023:06:25:30 +0000] \"GET /robots.txt HTTP/1.1\" 200 67\n",
    "192.168.0.5 - - [12/May/2023:06:25:31 +0000] \"GET /notfound.html HTTP/1.1\" 404 256\n",
    "10.0.0.1 - - [12/May/2023:06:25:32 +0000] \"GET /index.html HTTP/1.1\" 200 1024\n",
    "10.0.0.2 - - [12/May/2023:06:25:33 +0000] \"GET /contact HTTP/1.1\" 200 512\n",
]


def _read_text_file(path: Path) -> list[str]:
    """
    Read a text file and return its lines with trailing newlines preserved.
    Supports plain text as well as .gz compressed files (just in case).
    """
    if path.suffix == ".gz":
        with gzip.open(path, "rt", encoding="utf-8") as fh:
            return fh.readlines()
    with path.open("r", encoding="utf-8") as fh:
        return fh.readlines()


@pytest.mark.dependency()
def test_access_log_exists():
    """Ensure the access log file exists and is a regular file."""
    assert ACCESS_LOG_PATH.exists(), (
        f"Expected access log at {ACCESS_LOG_PATH} but it does not exist."
    )
    assert ACCESS_LOG_PATH.is_file(), (
        f"Expected {ACCESS_LOG_PATH} to be a regular file."
    )


@pytest.mark.dependency(depends=["test_access_log_exists"])
def test_access_log_contents_exact():
    """Validate that the access log contains the exact expected lines."""
    lines = _read_text_file(ACCESS_LOG_PATH)

    assert len(lines) == len(EXPECTED_LINES), (
        f"{ACCESS_LOG_PATH} should contain {len(EXPECTED_LINES)} lines "
        f"but has {len(lines)}."
    )

    for i, (actual, expected) in enumerate(zip(lines, EXPECTED_LINES), start=1):
        assert actual == expected, (
            f"Line {i} in {ACCESS_LOG_PATH} differs from the expected content.\n"
            f"Expected: {expected!r}\n"
            f"Found:    {actual!r}"
        )


@pytest.mark.dependency(depends=["test_access_log_exists"])
def test_access_log_404_count():
    """Count the number of 404 status codes and ensure it equals 3."""
    lines = _read_text_file(ACCESS_LOG_PATH)
    count_404 = sum(" 404 " in line for line in lines)

    assert count_404 == 3, (
        f"Expected exactly 3 lines with status code 404 in {ACCESS_LOG_PATH}, "
        f"but found {count_404}."
    )