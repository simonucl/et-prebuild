# test_initial_state.py
#
# This pytest suite validates that the *initial* operating-system / filesystem
# state is correct **before** the student attempts the mirroring task.
#
# Rules respected:
#   • Only stdlib + pytest are used.
#   • We check the full, absolute paths.
#   • We *do not* look for any of the output files or directories that the
#     student is expected to create (/home/user/artifacts/… or
#     /home/user/sync_logs/…).
#   • Failure messages are explicit so the student immediately sees what is
#     missing or broken.

import os
import shutil
import stat
import pytest

# --------------------------------------------------------------------------- #
# Constants describing the required upstream artefact and environment
# --------------------------------------------------------------------------- #

UPSTREAM_FILE = "/home/user/remote_repo/libalpha/libalpha-1.2.3.tar.gz"
EXPECTED_CONTENT_SNIPPET = b"This is libalpha binary version 1.2.3"


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _read_upstream_sample(path: str, length: int = 64) -> bytes:
    """
    Read up to `length` bytes from the upstream file.  We only need a snippet
    to confirm we have the *right* file in place.
    """
    with open(path, "rb") as fh:
        return fh.read(length)


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #

def test_upstream_file_exists_and_is_regular():
    """
    The remote artefact that the student must mirror *must* already exist and
    be a regular, non-empty file.
    """
    assert os.path.exists(UPSTREAM_FILE), (
        f"Required upstream file is missing:\n    {UPSTREAM_FILE}\n"
        "Create it before attempting the mirroring task."
    )

    # Must be a *file*, not a directory, symlink, etc.
    assert os.path.isfile(UPSTREAM_FILE), (
        f"Path exists but is not a regular file:\n    {UPSTREAM_FILE}"
    )

    # File must be non-empty.
    size = os.path.getsize(UPSTREAM_FILE)
    assert size > 0, (
        f"Upstream file is empty (size == 0 bytes):\n    {UPSTREAM_FILE}"
    )

    # Basic sanity check: file should be readable.
    mode = os.stat(UPSTREAM_FILE).st_mode
    assert mode & stat.S_IRUSR, (
        f"Upstream file is not readable by the current user:\n    {UPSTREAM_FILE}"
    )


def test_upstream_file_contains_expected_content_snippet():
    """
    Verify that the beginning of the upstream file contains the expected marker
    string so we are sure the correct version is stored.
    """
    snippet = _read_upstream_sample(UPSTREAM_FILE)
    assert EXPECTED_CONTENT_SNIPPET in snippet, (
        "The upstream file does not contain the expected content.  "
        "It should start with the text:\n"
        "    'This is libalpha binary version 1.2.3'\n"
        f"Upstream path checked:\n    {UPSTREAM_FILE}"
    )


def test_rsync_is_available_in_path():
    """
    The task *recommends* rsync and the automated tests rely on its output
    format.  Ensure that `rsync` is discoverable in the current PATH.
    """
    rsync_path = shutil.which("rsync")
    assert rsync_path is not None, (
        "The `rsync` executable was not found in your PATH.  "
        "Install it or ensure it is discoverable so you can complete the "
        "mirroring task with a single command."
    )