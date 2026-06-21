# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state before the student runs any commands.  It checks that the staging
# directory with the three solver archives exists and that each file has the
# exact byte-size and content expected by the assignment.
#
# NOTE:
# • We purposefully do NOT look for /home/user/curation/logs or
#   solver_inventory.csv – those are to be created later by the student.

import os
import pytest

STAGING_DIR = "/home/user/curation/binaries"

# Expected archives with their reference contents (ASCII) and sizes.
EXPECTED_ARCHIVES = {
    "cbc-2.10.5-linux-x86_64.tar.gz": (
        "CBC binary placeholder v2.10.5\n",
        31,
    ),
    "glpk-5.0-linux-x86_64.tar.gz": (
        "GLPK binary placeholder v5.0\n",
        29,
    ),
    "scip-8.0.3-linux-x86_64.tar.gz": (
        "SCIP binary placeholder v8.0.3\n",
        31,
    ),
}


def test_staging_directory_exists_and_is_directory():
    assert os.path.exists(
        STAGING_DIR
    ), f"The staging directory {STAGING_DIR!r} is missing."
    assert os.path.isdir(
        STAGING_DIR
    ), f"{STAGING_DIR!r} exists but is not a directory."


def test_archive_set_is_exact():
    """
    Verify that the staging directory contains *exactly* the three expected
    .tar.gz archives and no additional ones.  Extra or missing archives could
    lead to an incorrect inventory produced by the student later on.
    """
    # List every *.tar.gz file present in the staging directory.
    present_archives = sorted(
        f
        for f in os.listdir(STAGING_DIR)
        if f.endswith(".tar.gz") and os.path.isfile(os.path.join(STAGING_DIR, f))
    )

    expected_archives_sorted = sorted(EXPECTED_ARCHIVES)

    assert (
        present_archives == expected_archives_sorted
    ), (
        "The staging directory must contain exactly the following archives:\n"
        f"  {expected_archives_sorted}\n"
        f"Found instead:\n"
        f"  {present_archives}"
    )


@pytest.mark.parametrize("archive_name", EXPECTED_ARCHIVES.keys())
def test_each_archive_exists_with_correct_size_and_content(archive_name):
    """
    For every expected archive:
      • The file must exist.
      • Its byte-size must match the reference size.
      • The byte contents must match the reference text exactly.
    """
    expected_content, expected_size = EXPECTED_ARCHIVES[archive_name]
    path = os.path.join(STAGING_DIR, archive_name)

    # Existence check.
    assert os.path.isfile(
        path
    ), f"Expected archive {path!r} is missing or not a regular file."

    # Size check (via filesystem metadata).
    actual_size = os.path.getsize(path)
    assert (
        actual_size == expected_size
    ), f"{archive_name}: expected size {expected_size} bytes, found {actual_size} bytes."

    # Content check.
    with open(path, "rb") as fh:
        data = fh.read()

    # Ensure we deal strictly with bytes so that sizes line up precisely.
    expected_bytes = expected_content.encode("ascii")
    assert (
        data == expected_bytes
    ), f"{archive_name}: file contents do not match the expected reference buffer."