# test_initial_state.py
#
# Pytest suite that verifies the *initial* state of the filesystem
# before the student begins the restore exercise.
#
# It checks that
#   • the backup archive exists and is a regular file;
#   • the working directory /home/user/restore_test is NOT present yet;
#   • the archive contains the five mandatory files with the exact sizes
#     and MD-5 checksums stipulated in the task description.
#
# Only the Python standard library and pytest are used.

import hashlib
import os
import tarfile

import pytest

HOME = "/home/user"
ARCHIVE_PATH = os.path.join(HOME, "backups", "site_config_backup.tar.gz")
RESTORE_DIR = os.path.join(HOME, "restore_test")

# Mapping: archive member path  -> (expected_md5, expected_size)
EXPECTED_FILES = {
    "etc/nginx/nginx.conf": (
        "c3fcd3d76192e4007dfb496cca67e13b",
        26,
    ),
    "etc/nginx/conf.d/default.conf": (
        "900150983cd24fb0d6963f7d28e17f72",
        3,
    ),
    "var/www/html/index.html": (
        "0cc175b9c0f1b6a831c399e269772661",
        1,
    ),
    "var/www/html/healthcheck.php": (
        "d41d8cd98f00b204e9800998ecf8427e",
        0,
    ),
    "var/www/html/assets/style.css": (
        "f96b697d7cb7938d525a2f31aaf161d0",
        14,
    ),
}


def _canonical(name: str) -> str:
    """
    Return a canonicalised archive member name:
    • Strip any leading "./" that tar might prepend.
    """
    return name.lstrip("./")


def test_archive_exists_and_is_regular_file():
    assert os.path.exists(
        ARCHIVE_PATH
    ), f"Expected backup archive not found: {ARCHIVE_PATH}"
    assert os.path.isfile(
        ARCHIVE_PATH
    ), f"{ARCHIVE_PATH} exists but is not a regular file"


def test_restore_directory_absent():
    assert not os.path.exists(
        RESTORE_DIR
    ), f"Directory {RESTORE_DIR} should *not* exist before the exercise starts"


def test_archive_contains_expected_files_with_correct_content():
    # Open the tarball once and keep it open during the assertions
    try:
        tar = tarfile.open(ARCHIVE_PATH, mode="r:gz")
    except (tarfile.ReadError, FileNotFoundError) as exc:
        pytest.fail(f"Could not open archive {ARCHIVE_PATH}: {exc}")

    # Build a set of canonical member names for quick lookup
    member_names = {_canonical(m.name) for m in tar.getmembers()}

    for rel_path, (expected_md5, expected_size) in EXPECTED_FILES.items():
        # 1. Presence
        assert (
            rel_path in member_names
        ), f"Archive is missing required file: {rel_path}"

        # 2. Retrieve the member object (handle possible './' prefix)
        try:
            member = tar.getmember(rel_path)
        except KeyError:
            member = tar.getmember(f"./{rel_path}")  # fallback

        # 3. Must be a regular file
        assert member.isfile(), f"{rel_path} in archive is not a regular file"

        # 4. Size check (tar header size)
        assert (
            member.size == expected_size
        ), f"{rel_path}: expected size {expected_size} bytes, found {member.size} bytes in archive"

        # 5. MD-5 checksum of the *stored* file content
        extracted = tar.extractfile(member)
        assert (
            extracted is not None
        ), f"Could not read {rel_path} from archive"

        data = extracted.read()
        actual_md5 = hashlib.md5(data).hexdigest()
        assert (
            actual_md5 == expected_md5
        ), f"{rel_path}: expected md5 {expected_md5}, got {actual_md5}"

        # Double-check read size equals tar header size
        assert (
            len(data) == expected_size
        ), f"{rel_path}: tar header size {member.size} vs actual data length {len(data)}"

    tar.close()