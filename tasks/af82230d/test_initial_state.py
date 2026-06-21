# test_initial_state.py
#
# This pytest suite verifies that the training container starts
# with the exact mock-service structure the assignment describes.
#
# WHAT IS VERIFIED
# ----------------
# 1. The directory /home/user/mock_services exists and has 0755 perms.
# 2. The three JSON files auth.json, user.json and payment.json
#    a) exist
#    b) are the correct byte-size
#    c) contain the exact, byte-for-byte content (including trailing \n)
#
# IMPORTANT:  The output artefact /home/user/api_test.log is *not* touched
#             here (per the grading rules).

import os
import stat
import pytest

BASE_DIR = "/home/user/mock_services"

EXPECTED_FILES = {
    "auth.json":    (b'{"status":"ok","service":"auth"}\n',    33),
    "user.json":    (b'{"status":"ok","service":"user"}\n',    33),
    "payment.json": (b'{"status":"ok","service":"payment"}\n', 36),
}


def _octal_permissions(path: str) -> str:
    """Return the permission bits of *path* as a 4-digit octal string."""
    return oct(os.stat(path).st_mode & 0o777)


def test_mock_services_directory_exists_and_permissions():
    """
    The base directory must exist, be a directory, and have 0755 permissions.
    """
    assert os.path.isdir(BASE_DIR), (
        f"Required directory {BASE_DIR} is missing or is not a directory."
    )

    expected_perm = 0o755
    actual_perm = os.stat(BASE_DIR).st_mode & 0o777
    assert actual_perm == expected_perm, (
        f"Directory {BASE_DIR} must have permissions 755, "
        f"but has {_octal_permissions(BASE_DIR)}."
    )


@pytest.mark.parametrize("filename, expected", EXPECTED_FILES.items())
def test_mock_service_files_exist_and_contents(filename, expected):
    """
    Each required JSON file must exist and match the exact expected bytes.
    """
    expected_bytes, expected_size = expected
    path = os.path.join(BASE_DIR, filename)

    # Existence
    assert os.path.isfile(path), f"Required file {path} is missing."

    # Size
    actual_size = os.path.getsize(path)
    assert actual_size == expected_size, (
        f"File {path} should be {expected_size} bytes but is {actual_size} bytes."
    )

    # Content
    with open(path, "rb") as fh:
        actual_bytes = fh.read()

    assert actual_bytes == expected_bytes, (
        f"File {path} contents do not match the expected bytes.\n"
        f"Expected: {expected_bytes!r}\n"
        f"Found:    {actual_bytes!r}"
    )