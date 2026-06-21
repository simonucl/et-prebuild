# test_initial_state.py
#
# This pytest suite validates the *initial* state of the filesystem
# before the student performs any actions.  It asserts that:
#
# 1. The legacy release tarball exists at the expected location and has
#    the correct permissions.
# 2. The tarball is a valid gzip-compressed tar archive whose contents
#    exactly match the specification (both files and directories).
# 3. The parent directory that will later hold the extracted tree exists.
# 4. The directory that will later receive the build log is **absent**.
# 5. The extracted release directory is **absent** (nothing has been
#    unpacked yet).
#
# Only the Python standard library and pytest are used.

import os
import stat
import tarfile
import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

HOME = "/home/user"
OLD_RELEASES_DIR = os.path.join(HOME, "old_releases")
TARBALL_PATH = os.path.join(OLD_RELEASES_DIR, "release_v1.tar.gz")
EXPECTED_TARBALL_PERM = 0o644
EXPECTED_DIR_PERM = 0o755

# Directory that *will* be created by the student (must not exist yet)
BUILD_LOGS_DIR = os.path.join(HOME, "build_logs")

# Directory that *will* appear after extraction (must not exist yet)
EXTRACTED_RELEASE_DIR = os.path.join(OLD_RELEASES_DIR, "release_v1")

# Expected members inside the tarball
EXPECTED_DIRS_IN_TAR = {
    "release_v1",
    "release_v1/bin",
    "release_v1/src",
}
EXPECTED_FILES_IN_TAR = {
    "release_v1/LICENSE",
    "release_v1/README.md",
    "release_v1/bin/run.sh",
    "release_v1/src/main.c",
}

# All expected members (files + directories)
EXPECTED_TAR_MEMBERS = EXPECTED_DIRS_IN_TAR | EXPECTED_FILES_IN_TAR


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def mode_bits(path):
    """
    Return the permission bits (e.g. 0o755) of the filesystem entry `path`.
    """
    return stat.S_IMODE(os.lstat(path).st_mode)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_old_releases_directory_exists_and_permissions():
    assert os.path.isdir(OLD_RELEASES_DIR), (
        f"Directory {OLD_RELEASES_DIR!r} is missing. "
        "The legacy releases folder must already exist."
    )
    perms = mode_bits(OLD_RELEASES_DIR)
    assert perms == EXPECTED_DIR_PERM, (
        f"Directory {OLD_RELEASES_DIR!r} has permissions {oct(perms)}, "
        f"expected {oct(EXPECTED_DIR_PERM)}."
    )


def test_tarball_exists_and_permissions():
    assert os.path.isfile(TARBALL_PATH), (
        f"Tarball {TARBALL_PATH!r} is missing. "
        "It must be present before any extraction can happen."
    )
    perms = mode_bits(TARBALL_PATH)
    assert perms == EXPECTED_TARBALL_PERM, (
        f"Tarball {TARBALL_PATH!r} has permissions {oct(perms)}, "
        f"expected {oct(EXPECTED_TARBALL_PERM)}."
    )


def test_tarball_is_valid_and_contains_expected_members():
    try:
        with tarfile.open(TARBALL_PATH, mode="r:gz") as tf:
            member_names = {m.name.rstrip("/") for m in tf.getmembers()}
            missing = EXPECTED_TAR_MEMBERS - member_names
            extra   = member_names - EXPECTED_TAR_MEMBERS

            assert not missing, (
                f"Tarball {TARBALL_PATH!r} is missing the following members: "
                f"{sorted(missing)}"
            )
            assert not extra, (
                f"Tarball {TARBALL_PATH!r} contains unexpected members: "
                f"{sorted(extra)}"
            )

            # Validate each file/dir type and (for files) that mode is 0644 and size > 0.
            for member in tf.getmembers():
                name = member.name.rstrip("/")
                if name in EXPECTED_DIRS_IN_TAR:
                    assert member.isdir(), (
                        f"Tarball member {name!r} should be a directory."
                    )
                    # Directory permissions are expected to be 0755
                    perms = stat.S_IMODE(member.mode)
                    assert perms == EXPECTED_DIR_PERM, (
                        f"Directory member {name!r} has permissions {oct(perms)}, "
                        f"expected {oct(EXPECTED_DIR_PERM)}."
                    )
                elif name in EXPECTED_FILES_IN_TAR:
                    assert member.isfile(), (
                        f"Tarball member {name!r} should be a regular file."
                    )
                    perms = stat.S_IMODE(member.mode)
                    assert perms == EXPECTED_TARBALL_PERM, (
                        f"File member {name!r} has permissions {oct(perms)}, "
                        f"expected {oct(EXPECTED_TARBALL_PERM)}."
                    )
                    assert member.size > 0, (
                        f"File member {name!r} has size 0; expected non-empty content."
                    )
                else:
                    # Should never reach here due to earlier extra-member check.
                    pass
    except tarfile.TarError as exc:
        pytest.fail(f"Unable to open {TARBALL_PATH!r} as a gzip-compressed tar archive: {exc}")


def test_build_logs_directory_does_not_exist_yet():
    assert not os.path.exists(BUILD_LOGS_DIR), (
        f"Directory {BUILD_LOGS_DIR!r} should NOT exist yet. "
        "It is expected to be created by the student."
    )


def test_release_directory_not_yet_extracted():
    assert not os.path.exists(EXTRACTED_RELEASE_DIR), (
        f"Directory {EXTRACTED_RELEASE_DIR!r} should NOT exist before extraction."
    )