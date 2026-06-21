# test_initial_state.py
#
# This pytest suite validates that the container starts from the *clean*
# prerequisite state expected by the assignment *before* the student’s
# restore script runs.  If any of these tests fail, the container has
# been tampered with or the fixture was prepared incorrectly.

import os
import stat
import glob

import pytest

HOME = "/home/user"
BACKUP_DIR = os.path.join(HOME, "backup", "certs")
ACTIVE_DIR = os.path.join(HOME, "certs")
AUDIT_DIR = os.path.join(HOME, "cert_restore")

EXPECTED_PEMS = {
    "rootCA.pem": "-----BEGIN CERTIFICATE-----\nroot-ca-placeholder\n-----END CERTIFICATE-----\n",
    "intermediateCA.pem": "-----BEGIN CERTIFICATE-----\nintermediate-ca-placeholder\n-----END CERTIFICATE-----\n",
    "server.pem": "-----BEGIN CERTIFICATE-----\nserver-cert-placeholder\n-----END CERTIFICATE-----\n",
}


def _mode(path):
    """Return POSIX permission bits, e.g. 0o644."""
    return stat.S_IMODE(os.stat(path).st_mode)


def test_required_directories_exist():
    """Validate that the key directory scaffold exists."""
    for path in (
        HOME,
        os.path.join(HOME, "backup"),
        BACKUP_DIR,
        ACTIVE_DIR,
    ):
        assert os.path.isdir(path), f"Expected directory {path!r} to exist."


def test_backup_contains_expected_pems_only():
    """Ensure the backup directory has exactly the expected .pem files."""
    found = sorted(
        os.path.basename(p) for p in glob.glob(os.path.join(BACKUP_DIR, "*.pem"))
    )
    expected = sorted(EXPECTED_PEMS.keys())
    assert (
        found == expected
    ), f"Backup cert list mismatch.\nExpected: {expected}\nFound   : {found}"


@pytest.mark.parametrize("filename,expected_content", EXPECTED_PEMS.items())
def test_backup_pem_contents_and_permissions(filename, expected_content):
    """Each backup .pem file must have the exact expected content & perms."""
    path = os.path.join(BACKUP_DIR, filename)
    assert os.path.isfile(path), f"Missing backup cert: {path}"
    with open(path, encoding="utf-8") as fh:
        data = fh.read()
    assert (
        data == expected_content
    ), f"Content of {filename} differs from specification."

    # World-readable 0644 permissions are required.
    assert (
        _mode(path) == 0o644
    ), f"Permissions for {filename} should be 0644, found {oct(_mode(path))}."


def test_active_certs_dir_is_empty():
    """The live cert directory must start out empty of *.pem files."""
    pem_files = glob.glob(os.path.join(ACTIVE_DIR, "*.pem"))
    assert (
        not pem_files
    ), f"{ACTIVE_DIR} should be empty of .pem files, found: {pem_files}"


def test_audit_path_absent():
    """No audit directory or log should exist before the restore operation."""
    assert not os.path.exists(
        AUDIT_DIR
    ), f"{AUDIT_DIR} should NOT exist prior to the restore step."