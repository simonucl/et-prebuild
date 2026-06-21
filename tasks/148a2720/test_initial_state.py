# test_initial_state.py
#
# Pytest suite to validate the initial state of the operating-system /
# filesystem *before* the student performs any actions for the
# “certificate–maintenance utility” task.
#
# What we check here (and nothing more):
#   1. The directory /home/user/certs exists and has mode 755.
#   2. It contains two *.pem files: alpha.pem and beta.pem.
#   3. Those files have mode 644 and **exactly** the expected contents.
#
# NOTE: We deliberately do *not* test for anything related to the
# output artefacts (e.g. /home/user/cert_utils or cert_report.json),
# because the task rules forbid checking for output paths at this
# stage.

import os
import stat
import pytest

CERTS_DIR = "/home/user/certs"
ALPHA_PEM = os.path.join(CERTS_DIR, "alpha.pem")
BETA_PEM = os.path.join(CERTS_DIR, "beta.pem")

EXPECTED_ALPHA_CONTENT = (
    "-----BEGIN CERTIFICATE-----\n"
    "Dummy certificate placeholder only for testing utilities.\n"
    "Serial Number: 01\n"
    "Not After : 2030-12-31 23:59:59 GMT\n"
    "Subject CN=alpha.example.io\n"
    "-----END CERTIFICATE-----\n"
)

EXPECTED_BETA_CONTENT = (
    "-----BEGIN CERTIFICATE-----\n"
    "Dummy certificate placeholder only for testing utilities.\n"
    "Serial Number: 02\n"
    "Not After : 2025-06-15 12:00:00 GMT\n"
    "Subject CN=beta.example.io\n"
    "-----END CERTIFICATE-----\n"
)


def _mode(path):
    "Return the permission bits (e.g., 0o755) for a filesystem object."
    return stat.S_IMODE(os.stat(path).st_mode)


def test_certs_directory_exists_and_permissions():
    assert os.path.isdir(
        CERTS_DIR
    ), f"Required directory {CERTS_DIR!r} is missing."
    expected_mode = 0o755
    actual_mode = _mode(CERTS_DIR)
    assert (
        actual_mode == expected_mode
    ), f"{CERTS_DIR!r} must have permissions {oct(expected_mode)}, found {oct(actual_mode)}."


@pytest.mark.parametrize(
    "file_path, expected_content",
    [
        (ALPHA_PEM, EXPECTED_ALPHA_CONTENT),
        (BETA_PEM, EXPECTED_BETA_CONTENT),
    ],
)
def test_pem_files_exist_permissions_and_contents(file_path, expected_content):
    assert os.path.isfile(
        file_path
    ), f"Expected certificate file {file_path!r} is missing."

    expected_mode = 0o644
    actual_mode = _mode(file_path)
    assert (
        actual_mode == expected_mode
    ), f"{file_path!r} must have permissions {oct(expected_mode)}, found {oct(actual_mode)}."

    with open(file_path, "r", newline="") as fh:
        contents = fh.read()

    assert (
        contents == expected_content
    ), (
        f"Contents of {file_path!r} do not match the expected certificate text. "
        "Remember that blank lines and spacing must be exact."
    )