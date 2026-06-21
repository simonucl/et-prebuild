# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the filesystem
# before the student starts working on the assignment.
#
# The checks performed here purposefully exclude any assertions about
# the output artifact `/home/user/certs/compliance_audit.log`, because
# that file must not exist yet (and the rubric explicitly forbids
# testing for output files in the “initial‐state” suite).

import os
import pathlib
import re

import pytest

HOME = pathlib.Path("/home/user")
CERTS_DIR = HOME / "certs"

# Expected certificate files and the notAfter dates they must contain
EXPECTED_CERTS = {
    "website_valid.pem": "Nov 12 12:00:00 2031 GMT",
    "old_service.pem": "Jan  1 00:00:00 2021 GMT",
}

NOTAFTER_RE = re.compile(r"^notAfter=(.+)\s*$")


def read_notafter_line(cert_path: pathlib.Path) -> str:
    """
    Return the value that follows 'notAfter=' inside the certificate file.

    The function scans all lines to be tolerant of minor formatting
    differences (header lines, blank lines, etc.).
    """
    with cert_path.open("r", encoding="utf-8") as fp:
        for line in fp:
            m = NOTAFTER_RE.match(line)
            if m:
                return m.group(1)
    raise AssertionError(
        f"'notAfter=' line not found in certificate file: {cert_path}"
    )


def test_certs_directory_exists():
    assert CERTS_DIR.exists(), f"Required directory is missing: {CERTS_DIR}"
    assert CERTS_DIR.is_dir(), f"Expected {CERTS_DIR} to be a directory."


def test_expected_certificate_files_present():
    actual_pems = {
        p.name for p in CERTS_DIR.iterdir() if p.is_file() and p.suffix == ".pem"
    }
    missing = set(EXPECTED_CERTS) - actual_pems
    extras = actual_pems - set(EXPECTED_CERTS)

    assert not missing, (
        "The following required .pem files are missing from "
        f"{CERTS_DIR}: {', '.join(sorted(missing))}"
    )
    # Extras are allowed but warn if unexpected pem files appear
    assert not extras, (
        "Unexpected .pem files present in the certs directory: "
        f"{', '.join(sorted(extras))}"
    )


@pytest.mark.parametrize("filename,expected_date", EXPECTED_CERTS.items())
def test_certificate_notafter_values(filename, expected_date):
    cert_path = CERTS_DIR / filename
    assert cert_path.exists(), f"Missing certificate file: {cert_path}"

    extracted_date = read_notafter_line(cert_path)
    assert (
        extracted_date == expected_date
    ), (
        f"Certificate {filename} has an unexpected notAfter date.\n"
        f"  Expected: {expected_date!r}\n"
        f"  Found   : {extracted_date!r}"
    )