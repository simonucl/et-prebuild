# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system / filesystem
# state before the student starts working on the “backup integrity” task.
#
# The tests assert that:
#   • All prerequisite files and directories exist in their expected
#     locations and contain the exact bytes specified in the assignment.
#   • None of the artefacts that the student is supposed to create/modify
#     (e.g. the verification log, bumped version, CHANGELOG additions)
#     are present yet.
#
# The assertions purposefully fail with clear, actionable error messages
# should any part of the initial state be missing or incorrect.
#
# Only Python stdlib and pytest are used—as required.

import hashlib
import os
import textwrap
import pytest

HOME = "/home/user"
BACKUP_TOOL_DIR = os.path.join(HOME, "backup-tool")
BACKUP_ARCHIVE_DIR = os.path.join(HOME, "backup-archives", "2023-06-01")
VERIFICATION_LOG_DIR = os.path.join(HOME, "verification_logs")
VERIFICATION_LOG_PATH = os.path.join(VERIFICATION_LOG_DIR, "2023-06-01-integrity.log")


def read_file(path):
    """Utility helper that reads a file as text (UTF-8)."""
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def sha256_hex(path):
    """Return SHA-256 hex digest of file located at *path*."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def test_version_txt_exists_and_is_2_5_0():
    """Verify /backup-tool/version.txt exists and reads exactly '2.5.0\\n'."""
    version_path = os.path.join(BACKUP_TOOL_DIR, "version.txt")
    assert os.path.isfile(
        version_path
    ), f"Expected version file not found at {version_path!r}"

    content = read_file(version_path)
    assert (
        content == "2.5.0\n"
    ), f"{version_path!r} should contain '2.5.0\\n' but contains {content!r}"


def test_changelog_initial_content():
    """Verify that CHANGELOG.md contains only the pre-task sections."""
    changelog_path = os.path.join(BACKUP_TOOL_DIR, "CHANGELOG.md")
    assert os.path.isfile(
        changelog_path
    ), f"CHANGELOG.md missing at {changelog_path!r}"

    expected = textwrap.dedent(
        """\
        ## [2.5.0] - 2023-05-20
        - Added remote snapshot capability.

        ## [2.4.0] - 2023-04-10
        - Introduced incremental compression.

        """
    )
    actual = read_file(changelog_path)
    assert (
        actual == expected
    ), "Initial CHANGELOG.md content does not match the expected pre-task entries."


@pytest.mark.parametrize(
    "filename,expected_content",
    [
        ("backup1.txt", "Alpha backup file\n"),
        ("backup2.txt", "Beta backup file\n"),
    ],
)
def test_backup_files_exist_with_correct_content(filename, expected_content):
    """Ensure each backup file exists and contains the exact expected payload."""
    path = os.path.join(BACKUP_ARCHIVE_DIR, filename)
    assert os.path.isfile(
        path
    ), f"Required backup file {filename!r} missing at {path!r}"

    actual = read_file(path)
    assert (
        actual == expected_content
    ), f"Content mismatch in {filename!r}. Expected {expected_content!r}, got {actual!r}"


def test_manifest_file_exists_and_has_expected_incorrect_hashes():
    """
    Confirm manifest.sha256 exists and contains the *intentionally incorrect*
    SHA-256 sums specified in the exercise.
    Additionally, demonstrate that the listed sums do NOT match the files’
    real digests—verifying the setup for later 'FAIL' results.
    """
    manifest_path = os.path.join(BACKUP_ARCHIVE_DIR, "manifest.sha256")
    assert os.path.isfile(
        manifest_path
    ), f"Manifest file missing at {manifest_path!r}"

    expected_manifest = (
        f"{'e'*64}  backup1.txt\n"
        f"{'f'*64}  backup2.txt\n"
    )
    actual_manifest = read_file(manifest_path)
    assert (
        actual_manifest == expected_manifest
    ), "Manifest file content does not match the expected initial state."

    # Extra sanity-check: prove that the manifest hashes are indeed wrong.
    listed_hashes = {
        "backup1.txt": "e" * 64,
        "backup2.txt": "f" * 64,
    }
    for fname, bad_hash in listed_hashes.items():
        real_hash = sha256_hex(os.path.join(BACKUP_ARCHIVE_DIR, fname))
        assert (
            real_hash != bad_hash
        ), f"Setup error: real hash for {fname!r} unexpectedly equals the bad hash."


def test_verification_log_not_present_yet():
    """
    The verification log directory or file should NOT exist before
    the student carries out the assignment.
    """
    if os.path.exists(VERIFICATION_LOG_PATH):
        pytest.fail(
            f"Verification log {VERIFICATION_LOG_PATH!r} already exists—"
            "it must be created by the student, not pre-populated."
        )