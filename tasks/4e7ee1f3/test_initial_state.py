# test_initial_state.py
#
# This pytest file validates that the original INI-style configuration
# files required by the assignment are present *before* the student’s
# solution runs.  It performs **read-only** checks on the filesystem
# under /home/user/docs/configs and verifies the exact byte-for-byte
# contents of each expected file.  It purposely avoids touching or
# asserting anything about the output directory (/home/user/docs/reports)
# because the assignment rules forbid that.

import os
import textwrap
import pytest

BASE_DIR = "/home/user/docs/configs"

EXPECTED_INIS = {
    "settings.ini": textwrap.dedent(
        """\
        [general]
        author=alice
        version=1.2.3

        [paths]
        home=/home/alice
        temp=/tmp/project
        """
    ),
    "database.ini": textwrap.dedent(
        """\
        [connection]
        host=localhost
        port=5432
        user=dbuser

        [pools]
        min=1
        max=15
        """
    ),
    "ui.ini": textwrap.dedent(
        """\
        [window]
        width=1024
        height=768

        [theme]
        color=dark
        font=Roboto
        """
    ),
}


def _read_file(path):
    """Read a text file in UTF-8 and normalise line endings to '\n'."""
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read().replace("\r\n", "\n")


def test_configs_directory_exists():
    assert os.path.isdir(
        BASE_DIR
    ), f"Required directory {BASE_DIR!r} is missing."


def test_expected_ini_files_present():
    actual_files = {f for f in os.listdir(BASE_DIR) if f.endswith(".ini")}
    missing = set(EXPECTED_INIS) - actual_files
    assert not missing, (
        "The following required .ini files are missing from "
        f"{BASE_DIR!r}: {', '.join(sorted(missing))}"
    )


@pytest.mark.parametrize("filename, expected_content", EXPECTED_INIS.items())
def test_ini_contents_are_correct(filename, expected_content):
    path = os.path.join(BASE_DIR, filename)
    assert os.path.isfile(
        path
    ), f"Expected INI file {path!r} is missing."
    actual_content = _read_file(path)

    # Ensure file ends with a single trailing newline for exactness.
    if not expected_content.endswith("\n"):
        expected_content += "\n"

    assert (
        actual_content == expected_content
    ), (
        f"Contents of {path!r} do not match the expected template.\n\n"
        "----- EXPECTED -----\n"
        f"{expected_content}\n"
        "-----  FOUND  -----\n"
        f"{actual_content}\n"
        "--------------------"
    )