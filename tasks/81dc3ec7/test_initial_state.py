# test_initial_state.py
#
# Pytest suite that validates the initial, pre-action filesystem state
# for the “flat-text database” exercise.
#
# This file checks only the resources that must exist *before* the
# student performs any operations.  It deliberately does NOT look for
# any output artefacts such as ops_latest.log.

import os
import stat
import pytest

BASE_DIR = "/home/user/site_users"

# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
def read_file(path):
    """Return the full byte content of *path*; fail with a clear message
    if the file is unreadable for any reason."""
    if not os.path.isfile(path):
        pytest.fail(f"Expected file not found: {path}")
    try:
        with open(path, "rb") as fh:
            return fh.read()
    except OSError as exc:
        pytest.fail(f"Could not open {path!r}: {exc}")

def assert_text_file_content(path, expected):
    """Assert that *path* exists and its *binary* content matches
    *expected* (a str).  Comparison is byte-for-byte, including the
    final newline."""
    actual_bytes = read_file(path)
    try:
        actual_text = actual_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        pytest.fail(f"File {path!r} is not valid UTF-8 text: {exc}")

    if actual_text != expected:
        # Show a helpful, unified diff in the assertion error.
        import difflib
        diff = "\n".join(
            difflib.unified_diff(
                expected.splitlines(keepends=True),
                actual_text.splitlines(keepends=True),
                fromfile="expected",
                tofile="actual",
            )
        )
        pytest.fail(
            f"Content mismatch in {path}.\n"
            f"Unified diff (expected → actual):\n{diff}"
        )

# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------
def test_directory_exists_and_writable():
    """The base directory must exist, be a directory, and be writable."""
    assert os.path.exists(BASE_DIR), f"Directory missing: {BASE_DIR}"
    assert os.path.isdir(BASE_DIR), f"Path is not a directory: {BASE_DIR}"
    assert os.access(BASE_DIR, os.W_OK), (
        f"Directory {BASE_DIR} is not writable by the current user."
    )

@pytest.mark.parametrize(
    "relative_path,expected_content",
    [
        (
            "users.db",
            (
                "alice:active:alice@example.com\n"
                "bob:active:bob@example.com\n"
                "carol:disabled:carol@oldmail.com\n"
                "dave:active:dave@example.com\n"
            ),
        ),
        (
            "pending_additions.txt",
            (
                "eve eve@example.com\n"
                "frank frank@example.com\n"
                "carol carol@newmail.com\n"
            ),
        ),
        (
            "pending_deactivations.txt",
            (
                "bob\n"
                "frank\n"
            ),
        ),
        (
            "pending_email_updates.txt",
            (
                "alice alice@newdomain.com\n"
                "carol carol@newdomain.com\n"
            ),
        ),
    ],
)
def test_files_have_exact_expected_content(relative_path, expected_content):
    """Each initial file must exist and contain the precise expected text."""
    full_path = os.path.join(BASE_DIR, relative_path)
    assert_text_file_content(full_path, expected_content)