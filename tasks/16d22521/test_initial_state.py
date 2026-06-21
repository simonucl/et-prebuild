# test_initial_state.py
#
# This test-suite asserts the *pre-existing* state of the filesystem that
# must be in place **before** the student’s backup script is executed.
#
# IMPORTANT:
#   • Only objects that already exist in the exercise description are checked.
#   • No checks are performed for any file or directory that the student is
#     supposed to create (e.g. /home/user/backups or /home/user/backup_logs).
#   • All paths are absolute, as required.
#
# The tests intentionally keep to the Python stdlib + pytest.

import os
import stat
import hashlib
import pytest

CONFIG_DIR = "/home/user/configs"

# Mapping of absolute paths → expected file contents (as bytes)
EXPECTED_FILES = {
    "/home/user/configs/app.conf": (
        b"# Application configuration\n"
        b"port=8080\n"
        b"debug=true\n"
    ),
    "/home/user/configs/db.yml": (
        b"database:\n"
        b"  host: localhost\n"
        b"  port: 5432\n"
        b"  user: app\n"
        b"  password: secret\n"
    ),
    "/home/user/configs/nginx/nginx.conf": (
        b"user www-data;\n"
        b"worker_processes auto;\n"
        b"events { worker_connections 1024; }\n"
        b"http {\n"
        b"    server {\n"
        b"        listen 80;\n"
        b"        location / {\n"
        b"            proxy_pass http://127.0.0.1:8080;\n"
        b"        }\n"
        b"    }\n"
        b"}\n"
    ),
}


def _mode(path):
    """Return the permission bits of a path as an int (e.g. 0o755)."""
    return stat.S_IMODE(os.stat(path).st_mode)


def _is_readable_file(path):
    """True if 'path' is a regular file that can be read by the current user."""
    return os.path.isfile(path) and os.access(path, os.R_OK)


def test_config_directory_exists_and_permissions():
    """
    /home/user/configs must already exist, be a directory, and not be
    world-writable (permission bits 0755 expected).
    """
    assert os.path.isdir(CONFIG_DIR), (
        f"Expected directory {CONFIG_DIR} to exist before running the script."
    )

    perms = _mode(CONFIG_DIR)
    assert perms == 0o755, (
        f"Directory {CONFIG_DIR} should have permissions 0755, "
        f"found {oct(perms)} instead."
    )


@pytest.mark.parametrize("path", [
    "/home/user/configs/nginx",
])
def test_required_subdirectories_exist(path):
    assert os.path.isdir(path), f"Required directory {path} is missing."
    perms = _mode(path)
    assert perms == 0o755, (
        f"Directory {path} should have permissions 0755, "
        f"found {oct(perms)} instead."
    )


@pytest.mark.parametrize("path,expected_bytes", list(EXPECTED_FILES.items()))
def test_preexisting_files_exist_and_contents_unchanged(path, expected_bytes):
    # File must exist and be readable
    assert _is_readable_file(path), f"Required file {path} is missing or not readable."

    # File must *not* be executable (should be 0644)
    perms = _mode(path)
    assert perms == 0o644, (
        f"File {path} should have permissions 0644, found {oct(perms)} instead."
    )

    # Contents must match exactly
    with open(path, "rb") as fh:
        actual = fh.read()
    assert actual == expected_bytes, (
        f"Contents of {path} differ from the expected initial state."
    )

    # Checksum sanity check
    expected_digest = hashlib.sha256(expected_bytes).hexdigest()
    actual_digest = hashlib.sha256(actual).hexdigest()
    assert actual_digest == expected_digest, (
        f"SHA-256 digest of {path} does not match the expected value."
    )