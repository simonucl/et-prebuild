# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state before the
# student starts working on the “certificate vulnerability sweep” task.
#
# It checks that:
#   • the expected certificate directory and files exist;
#   • each certificate file contains the exact key lines the assignment
#     description specifies;
#   • the scan_results directory as well as the output log file do NOT
#     exist yet (the student must create them).
#
# Only Python’s stdlib and pytest are used.

from pathlib import Path
import pytest

CERT_DIR = Path("/home/user/targets/certs")
SCAN_RESULTS_DIR = Path("/home/user/targets/scan_results")
LOG_FILE = SCAN_RESULTS_DIR / "cert_vuln.log"

EXPECTED_CERTS = {
    "goodcorp.pem": {
        "Subject": "Subject: CN=good.example.com",
        "Signature": "Signature Algorithm: sha256WithRSAEncryption",
        "Not After": "Not After : Dec 31 23:59:59 2035 GMT",
    },
    "weakcorp.pem": {
        "Subject": "Subject: CN=weak.example.com",
        "Signature": "Signature Algorithm: sha1WithRSAEncryption",
        "Not After": "Not After : Dec 31 23:59:59 2035 GMT",
    },
    "oldcorp.pem": {
        "Subject": "Subject: CN=expired.example.com",
        "Signature": "Signature Algorithm: sha256WithRSAEncryption",
        "Not After": "Not After : Jan  1 00:00:00 2020 GMT",
    },
}


def _collect_lines(path: Path):
    """
    Return a dictionary that maps a line's *prefix* (before the first colon)
    to the full line with surrounding whitespace stripped.
    """
    lines = {}
    for raw in path.read_text().splitlines():
        stripped = raw.strip()
        if ":" in stripped:
            prefix = stripped.split(":", 1)[0]  # 'Subject', 'Signature Algorithm', ...
            lines[prefix] = stripped
    return lines


def test_certificate_directory_exists():
    assert CERT_DIR.is_dir(), (
        f"Expected certificate directory {CERT_DIR} to exist and be a directory."
    )


@pytest.mark.parametrize("file_name", EXPECTED_CERTS.keys())
def test_certificate_file_exists(file_name):
    file_path = CERT_DIR / file_name
    assert file_path.is_file(), (
        f"Expected certificate file {file_path} to exist."
    )


@pytest.mark.parametrize("file_name, expectations", EXPECTED_CERTS.items())
def test_certificate_file_contents(file_name, expectations):
    """
    Verify that each certificate file contains the exact expected lines
    for Subject, Signature Algorithm, and Not After.
    """
    file_path = CERT_DIR / file_name
    found_lines = _collect_lines(file_path)

    # Subject line
    expected_subject = expectations["Subject"]
    actual_subject = found_lines.get("Subject")
    assert actual_subject == expected_subject, (
        f"{file_name}: expected Subject line '{expected_subject}', "
        f"but found '{actual_subject}'."
    )

    # Signature Algorithm line
    expected_sig = expectations["Signature"]
    actual_sig = found_lines.get("Signature Algorithm")
    assert actual_sig == expected_sig, (
        f"{file_name}: expected Signature Algorithm line '{expected_sig}', "
        f"but found '{actual_sig}'."
    )

    # Not After line
    expected_na = expectations["Not After"]
    actual_na = found_lines.get("Not After ")
    # Note: 'Not After ' (with a space) is exactly how openssl formats it.
    assert actual_na == expected_na, (
        f"{file_name}: expected Not After line '{expected_na}', "
        f"but found '{actual_na}'."
    )


def test_scan_results_directory_does_not_exist_yet():
    assert not SCAN_RESULTS_DIR.exists(), (
        f"The directory {SCAN_RESULTS_DIR} should NOT exist before the student "
        f"runs their solution."
    )


def test_log_file_does_not_exist_yet():
    assert not LOG_FILE.exists(), (
        f"The output log file {LOG_FILE} should NOT exist before the student "
        f"runs their solution."
    )