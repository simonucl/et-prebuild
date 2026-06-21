# test_initial_state.py
#
# This pytest suite validates the *initial* operating-system state
# expected **before** the student performs any action.  It checks only
# pre-existing resources and deliberately avoids inspecting any files
# that the student is supposed to create (per task instructions).
#
# What we verify:
# 1. The directory /home/user/docs exists.
# 2. The helper script /home/user/docs/generate_docs.sh exists and is
#    executable.
#
# If any of these prerequisites are missing or mis-configured, the
# corresponding test will fail with an explanatory message.

import os
import stat
from pathlib import Path

DOCS_DIR = Path("/home/user/docs")
GENERATE_SCRIPT = DOCS_DIR / "generate_docs.sh"


def test_docs_directory_exists():
    """The directory /home/user/docs must be present at test start."""
    assert DOCS_DIR.exists(), (
        f"Expected directory '{DOCS_DIR}' is missing. "
        "Create it before running the exercise."
    )
    assert DOCS_DIR.is_dir(), (
        f"'{DOCS_DIR}' exists but is not a directory. "
        "Ensure it is a directory with the correct path."
    )


def test_generate_docs_script_exists_and_is_executable():
    """
    The helper script /home/user/docs/generate_docs.sh must already
    exist and have at least one execute bit set (user, group or other).
    """
    assert GENERATE_SCRIPT.exists(), (
        f"Required script '{GENERATE_SCRIPT}' is missing. "
        "It should be present before the exercise begins."
    )
    assert GENERATE_SCRIPT.is_file(), (
        f"'{GENERATE_SCRIPT}' exists but is not a regular file."
    )

    # Check that the script is executable by *someone* (user, group, or other).
    mode = GENERATE_SCRIPT.stat().st_mode
    is_executable = bool(mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))

    assert is_executable, (
        f"Script '{GENERATE_SCRIPT}' exists but is not marked executable. "
        "Add execute permissions (e.g., chmod +x)."
    )