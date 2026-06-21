# test_initial_state.py
#
# This pytest suite validates the *initial* on-disk state that must be
# present before the student begins any work.  It deliberately does **not**
# look for the output directory or the files that the exercise asks the
# student to create later.  If any of the checks below fail, the accompanying
# assertion message should make it clear what is missing or incorrect.
#
# Allowed imports: only the Python stdlib and pytest.

import os
import stat
import pytest

HOME = "/home/user"
PROVISION_DIR = os.path.join(HOME, "provision")
SERVERS_LIST = os.path.join(PROVISION_DIR, "servers.list")

EXPECTED_SERVERS_LIST_LINES = [
    "web-1,10.1.1.10,ubuntu18",
    "web-2,10.1.1.11,ubuntu18",
    "db-1,10.1.2.20,centos7",
    "cache-1,10.1.3.30,alpine3",
    "msg-queue,10.1.4.40,debian10",
]


def test_provision_directory_exists_and_writable():
    """The directory /home/user/provision must already exist and be writable."""
    assert os.path.exists(PROVISION_DIR), (
        f"Required directory {PROVISION_DIR!r} is missing."
    )
    assert os.path.isdir(PROVISION_DIR), (
        f"Expected {PROVISION_DIR!r} to be a directory, but it is not."
    )

    # Check write permission for the current user
    mode = os.stat(PROVISION_DIR).st_mode
    writable = bool(mode & stat.S_IWUSR)
    assert writable, (
        f"Directory {PROVISION_DIR!r} exists but is not writable by the current user."
    )


def test_servers_list_file_exists_with_correct_contents():
    """
    The file /home/user/provision/servers.list must exist and contain
    exactly the five expected CSV lines, each LF-terminated and with no
    extra blank lines.
    """
    assert os.path.exists(SERVERS_LIST), (
        f"Required file {SERVERS_LIST!r} is missing."
    )
    assert os.path.isfile(SERVERS_LIST), (
        f"Expected {SERVERS_LIST!r} to be a regular file, but it is not."
    )

    with open(SERVERS_LIST, "r", encoding="utf-8") as fh:
        contents = fh.read()

    # Split on '\n' but keep the trailing empty element (if the file ends
    # with an extra newline) so we can detect superfluous blank lines.
    lines = contents.split("\n")

    # If the file ends with a newline, the last element will be ''.  Remove
    # exactly one such empty string at the end, if present.
    if lines and lines[-1] == "":
        lines.pop()

    assert lines == EXPECTED_SERVERS_LIST_LINES, (
        "The contents of {0!r} do not match the expected 5-line CSV data.\n"
        "Expected:\n{1}\n\nFound:\n{2}".format(
            SERVERS_LIST,
            "\n".join(EXPECTED_SERVERS_LIST_LINES),
            "\n".join(lines),
        )
    )


@pytest.mark.skip(reason="Output artefacts should not exist yet.")
def test_output_directory_not_preexisting():
    """
    This test is intentionally skipped; it documents the expectation that
    /home/user/provision/output should NOT be present before the student runs
    their solution.  Skipping avoids enforcing absence while still conveying
    the intention.
    """
    output_dir = os.path.join(PROVISION_DIR, "output")
    assert not os.path.exists(output_dir), (
        f"Directory {output_dir!r} unexpectedly exists before the task begins."
    )