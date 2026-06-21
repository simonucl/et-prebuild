# test_initial_state.py
"""
Pytest suite that verifies the initial operating-system / file-system state
*before* the student’s solution is executed.

Rules enforced by these tests
1. The certificate source directory /home/user/certs/input exists.
2. Exactly three *.pem files are present directly inside that directory
   (no recursion) and they have the expected file names.
3. Every certificate contains single-line key/value pairs for the four required
   fields: Subject, Issuer, NotBefore, NotAfter.
4. DAYS_VALIDITY, calculated as floor((NotAfter-NotBefore) / 86400 s), matches
   the reference values shipped with the task image.
5. The diagnostics output directory /home/user/cert_diagnostics either does
   not exist yet or, if it does, contains no pre-existing diagnostics log
   (so the student starts from a clean slate).
"""

import os
import glob
import datetime

import pytest


HOME = "/home/user"
CERT_DIR = os.path.join(HOME, "certs", "input")
OUT_DIR = os.path.join(HOME, "cert_diagnostics")

# Expected filenames and DAYS_VALIDITY values (kept in sync with fixture data)
EXPECTED_FILES = {
    "example_root.pem": 30,
    "www_acme_com.pem": 183,
    "expired_test.pem": 14,
}


@pytest.fixture(scope="module")
def pem_paths():
    """Return a dict {filename: full_path} for the PEM files that exist."""
    paths = {
        os.path.basename(p): p
        for p in glob.glob(os.path.join(CERT_DIR, "*.pem"))
        if os.path.isfile(p)
    }
    return paths


def test_cert_directory_exists():
    assert os.path.isdir(CERT_DIR), (
        f"The directory {CERT_DIR!r} is missing.  "
        "All source certificates must reside here."
    )


def test_exactly_three_pem_files_present(pem_paths):
    found = set(pem_paths)
    expected = set(EXPECTED_FILES)
    assert found == expected, (
        "PEM file mismatch.\n"
        f"Expected (exactly): {sorted(expected)}\n"
        f"Found            : {sorted(found)}"
    )


def _parse_cert_file(path):
    """
    Read the certificate and return a dict with keys:
    Subject, Issuer, NotBefore, NotAfter (all strings)
    """
    record_keys = {"Subject", "Issuer", "NotBefore", "NotAfter"}
    parsed = {}
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            if "=" not in line:
                continue
            key, value = line.rstrip("\n").split("=", 1)
            if key in record_keys:
                parsed[key] = value
    return parsed


@pytest.mark.parametrize("fname, expected_days", EXPECTED_FILES.items())
def test_certificate_fields_and_validity(pem_paths, fname, expected_days):
    full_path = pem_paths[fname]
    parsed = _parse_cert_file(full_path)

    # 1. Make sure all required keys exist once.
    missing = {"Subject", "Issuer", "NotBefore", "NotAfter"} - parsed.keys()
    assert not missing, (
        f"{full_path}: Missing required key(s): {', '.join(sorted(missing))}"
    )

    # 2. Validate date format and compute DAYS_VALIDITY.
    fmt = "%Y-%m-%d %H:%M:%S"
    try:
        not_before = datetime.datetime.strptime(parsed["NotBefore"], fmt)
        not_after = datetime.datetime.strptime(parsed["NotAfter"], fmt)
    except ValueError as exc:
        pytest.fail(f"{full_path}: Date parsing failed – {exc}")

    assert not_after > not_before, (
        f"{full_path}: NotAfter ({parsed['NotAfter']}) "
        f"is not later than NotBefore ({parsed['NotBefore']})."
    )

    delta_days = (not_after - not_before).days
    assert (
        delta_days == expected_days
    ), f"{full_path}: Expected DAYS_VALIDITY {expected_days}, got {delta_days}."


def test_no_preexisting_output_logs():
    """
    The diagnostics directory should not contain a cert_diagnostic_*.log before
    the student script runs.  If the directory does not exist at all that is
    also acceptable.
    """
    if not os.path.exists(OUT_DIR):
        # Directory absent – that is perfectly fine for the initial state.
        return

    assert os.path.isdir(OUT_DIR), (
        f"{OUT_DIR!r} exists but is not a directory.  "
        "Please remove or rename it before running the task."
    )

    existing_logs = glob.glob(os.path.join(OUT_DIR, "cert_diagnostic_*.log"))
    assert not existing_logs, (
        "There are pre-existing diagnostics log files:\n"
        + "\n".join(existing_logs)
        + "\nThe directory must be empty so the student's script can write "
        "exactly one new log file."
    )