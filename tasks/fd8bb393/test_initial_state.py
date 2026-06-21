# test_initial_state.py
#
# This pytest suite verifies the *initial* operating-system / filesystem
# state before the student runs their solution command.  In particular, it
# checks that the PostgreSQL start-up file `/home/user/.psqlrc` is **not**
# already present with the exact final desired contents.  The student’s
# forthcoming command must therefore create or overwrite this file.
#
# Requirements enforced here:
#   1.  The home directory `/home/user` must exist.
#   2.  Either the file `/home/user/.psqlrc` does not exist *or*
#       it exists but its bytes differ from the required final
#       contents ("\set VERBOSITY verbose\n\timing\n").
#
# Only Python’s stdlib and pytest are used.


import os
import pathlib
import pytest


HOME_DIR = pathlib.Path("/home/user")
PSQLRC_PATH = HOME_DIR / ".psqlrc"

# The exact content the file is supposed to have *after* the student acts.
EXPECTED_FINAL_CONTENT = b"\\set VERBOSITY verbose\n\\timing\n"


def test_home_directory_exists():
    """Ensure the baseline `/home/user` directory is present."""
    assert HOME_DIR.is_dir(), (
        "Expected the home directory '/home/user' to exist. "
        "Without it, subsequent tasks cannot be completed."
    )


def test_psqlrc_not_already_finalised():
    """
    Verify that `/home/user/.psqlrc` is not already in its final required
    state.  The student must create or overwrite this file; if it already
    contains the correct bytes, the exercise would be moot.
    """
    if not PSQLRC_PATH.exists():
        # File absent → good initial state.
        return

    # File exists; ensure contents differ from the final required bytes.
    actual_bytes = PSQLRC_PATH.read_bytes()
    assert actual_bytes != EXPECTED_FINAL_CONTENT, (
        f"The file '{PSQLRC_PATH}' already exists with the exact required "
        "final content.  The environment should start without this file "
        "so that the student can demonstrate its creation."
    )