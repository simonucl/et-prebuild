# test_initial_state.py
#
# This pytest file validates the *initial* state of the OS / filesystem
# before the student performs any action on the trouble-ticket.
#
# It asserts that:
#   1. The open ticket directory exists at the exact expected path.
#   2. The file `description.txt` exists inside that directory.
#   3. The contents of `description.txt` are exactly
#        "User cannot connect to VPN\n"
#   4. The parent directory for resolved tickets already exists.
#
# NOTE:
#   • We intentionally do NOT check for the future output directory
#     `/home/user/support/tickets/resolved/12345` (or its contents),
#     because that path is supposed to be created only **after** the
#     student completes the task; testing it here would violate the
#     “no output files or directories” rule.

import os
from pathlib import Path

OPEN_TICKET_DIR = Path("/home/user/support/tickets/open/12345")
DESCRIPTION_FILE = OPEN_TICKET_DIR / "description.txt"
RESOLVED_PARENT_DIR = Path("/home/user/support/tickets/resolved")


def test_open_ticket_directory_exists():
    """The open ticket directory must exist before any action is taken."""
    assert OPEN_TICKET_DIR.is_dir(), (
        f"Expected directory {OPEN_TICKET_DIR} is missing. "
        "The ticket cannot be processed if the source directory is absent."
    )


def test_description_file_exists():
    """description.txt must exist inside the open ticket directory."""
    assert DESCRIPTION_FILE.is_file(), (
        f"Expected file {DESCRIPTION_FILE} is missing. "
        "The ticket description must remain intact."
    )


def test_description_file_contents():
    """description.txt must contain the exact, unmodified line."""
    expected_content = "User cannot connect to VPN\n"
    try:
        with DESCRIPTION_FILE.open("r", encoding="utf-8") as fp:
            actual_content = fp.read()
    except FileNotFoundError:
        pytest.fail(f"Cannot open {DESCRIPTION_FILE}; file is missing.")

    assert actual_content == expected_content, (
        "description.txt does not contain the expected text.\n"
        f"Expected: {repr(expected_content)}\n"
        f"Actual:   {repr(actual_content)}"
    )


def test_resolved_parent_directory_exists():
    """
    The parent directory for resolved tickets should pre-exist so the move can
    succeed without the student having to create it.
    """
    assert RESOLVED_PARENT_DIR.is_dir(), (
        f"Expected directory {RESOLVED_PARENT_DIR} is missing. "
        "Create the parent 'resolved' directory before proceeding."
    )