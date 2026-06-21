# test_initial_state.py
#
# This pytest suite validates the initial, immutable state of the
# filesystem before the student starts working on the task.
#
# It _only_ checks for items that must already exist.  It does **NOT**
# look for the artefacts that the student is asked to create
# (e.g. `/home/user/profiles/function_frequency.log`).

import os
from pathlib import Path

import pytest

PROFILES_DIR = Path("/home/user/profiles")
CALLSTACK_LOG = PROFILES_DIR / "callstack.log"

# The exact 22 lines (each must be terminated by a single '\n')
EXPECTED_CALLSTACK_LINES = [
    "malloc",
    "free",
    "malloc",
    "memcpy",
    "malloc",
    "memcpy",
    "free",
    "read",
    "write",
    "read",
    "malloc",
    "free",
    "memcpy",
    "write",
    "write",
    "malloc",
    "free",
    "read",
    "memset",
    "memset",
    "malloc",
    "write",
]

###############################################################################
# Helper utilities
###############################################################################


def read_text(path: Path) -> str:
    """Read text from *path*, raising a helpful assertion if it fails."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:  # pragma: no cover
        pytest.fail(f"Required file not found: {path}")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {path}: {exc}")


###############################################################################
# Tests
###############################################################################


def test_profiles_directory_exists():
    assert PROFILES_DIR.exists(), (
        "Directory '/home/user/profiles' must exist before the task begins. "
        "It is missing."
    )
    assert PROFILES_DIR.is_dir(), (
        f"Expected '{PROFILES_DIR}' to be a directory, "
        "but something else exists there."
    )


def test_callstack_log_exists_and_is_file():
    assert CALLSTACK_LOG.exists(), (
        "Required input file '/home/user/profiles/callstack.log' is missing."
    )
    assert CALLSTACK_LOG.is_file(), (
        f"Expected '{CALLSTACK_LOG}' to be a regular file."
    )


def test_callstack_log_content_exact():
    """
    The call-stack dump must contain exactly the 22 lines specified in the
    task description, each terminated by a single LF (\\n).  No extra whitespace,
    no extra blank lines.
    """
    data = read_text(CALLSTACK_LOG)

    # 1. File must terminate with exactly one newline so that `wc -l`
    #    counts the correct number of lines.
    assert data.endswith("\n"), (
        f"File '{CALLSTACK_LOG}' must end with a single newline character "
        "('\\n')."
    )

    # 2. There must not be an extra blank line at the end.
    # splitlines(keepends=False) discards newline characters.
    lines = data.splitlines()
    assert len(lines) == 22, (
        f"File '{CALLSTACK_LOG}' must contain exactly 22 lines; "
        f"found {len(lines)}."
    )

    # 3. Content must match exactly, line for line.
    assert lines == EXPECTED_CALLSTACK_LINES, (
        "Content of '/home/user/profiles/callstack.log' does not match the "
        "expected initial data.\n"
        "Expected lines:\n"
        f"{EXPECTED_CALLSTACK_LINES}\n\n"
        "Actual lines:\n"
        f"{lines}"
    )