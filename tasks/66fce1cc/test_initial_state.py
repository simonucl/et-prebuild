# test_initial_state.py
#
# This test-suite verifies that the starting filesystem state is exactly as
# described in the task _before_ the student performs any action.
#
# It checks:
#   • The presence and contents of /home/user/company_certs/alpha.crt
#   • The presence and contents of /home/user/company_certs/bravo.crt
#   • That no additional *.crt files are present beneath /home/user/company_certs/
#   • The absence of /home/user/compliance_logs/ (it must be created by the student)
#
# Only stdlib + pytest are used as required.

from pathlib import Path
import hashlib
import pytest
import textwrap

HOME = Path("/home/user")
CERT_DIR = HOME / "company_certs"
COMPLIANCE_DIR = HOME / "compliance_logs"


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def sha256_hex(path: Path) -> str:
    """Return the hex-encoded SHA-256 of a file."""
    h = hashlib.sha256()
    with path.open("rb") as fp:
        for chunk in iter(lambda: fp.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def read_file(path: Path) -> str:
    """Read a text file with universal newlines and normalise to '\n'."""
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


# --------------------------------------------------------------------------- #
# Expected certificate file contents (verbatim, including newlines)
# --------------------------------------------------------------------------- #
ALPHA_EXPECTED = textwrap.dedent(
    """\
    -----BEGIN CERTIFICATE-----
    MIIBrzCCAVSgAwIBAgIUBEHPxfN3E3xaQa58aeGeq/QAdzMwCgYIKoZIzj0EAwIw
    EzERMA8GA1UEAwwIYWxwaGEuY29tMB4XDTIzMDgwMTAwMDAwMFoXDTI0MDgwMTAw
    MDAwMFowEzERMA8GA1UEAwwIYWxwaGEuY29tMFkwEwYHKoZIzj0CAQYIKoZIzj0D
    AQcDQgAEi0JPFpKnzGWx/89ZbduCMsZ/HXXIQK5vCk1vZ1tcHTTX3e8DqRL3Ojax
    /P6MqxsVXni4eWhv14jArlTc95xJCaNTMFEwHQYDVR0OBBYEFLcdLXx+3CX6XcnG
    V7H5PHeTtNKgMB8GA1UdIwQYMBaAFLcdLXx+3CX6XcnGV7H5PHeTtNKgMA8GA1Ud
    EwEB/wQFMAMBAf8wCgYIKoZIzj0EAwIDSQAwRgIhAKZDdp2PbgM3N3aR6Vrn956x
    BY2NU4VFIfE88ll/aT0cAiEA+2CevulaHYodEc/WWEDuJeayQMZT6X0hgqP/d9vy
    q6A=
    -----END CERTIFICATE-----
    """
)

BRAVO_EXPECTED = textwrap.dedent(
    """\
    -----BEGIN CERTIFICATE-----
    MIIBqTCCAU+gAwIBAgIUYr2vNhbbX6YsJhBKt3vnDnN/SfAwCgYIKoZIzj0EAwIw
    FDESMBAGA1UEAwwJYnJhdm8uY29tMB4XDTIzMDgwMTAwMDAwMFoXDTI0MDgwMTAw
    MDAwMFowFDESMBAGA1UEAwwJYnJhdm8uY29tMFkwEwYHKoZIzj0CAQYIKoZIzj0D
    AQcDQgAEcJsteUms9UpAJZciV06P88GJEqn3Ejj6inUeJ8V+RaHcRUW2KIiMzFxL
    0X58F3RDeo63eVUsVTNff7kwh28zd6NTMFEwHQYDVR0OBBYEFFIqhzyapMI2vlA9
    SxrdbidKfnUSMB8GA1UdIwQYMBaAFFIqhzyapMI2vlA9SxrdbidKfnUSMA8GA1Ud
    EwEB/wQFMAMBAf8wCgYIKoZIzj0EAwIDRwAwRAIgUoil58x2oyS9MhUlCT3VkOIT
    pFmS6r30YIOCQM7DDDeCIHsCIFlfLaHruM3aMcMBXNIN1qNbfXDnpa9eKJeNEqXW
    xup6
    -----END CERTIFICATE-----
    """
)


# --------------------------------------------------------------------------- #
# Tests verifying initial state
# --------------------------------------------------------------------------- #
def test_company_certs_directory_exists_and_is_directory():
    assert CERT_DIR.exists(), f"Expected directory {CERT_DIR} to exist."
    assert CERT_DIR.is_dir(), f"{CERT_DIR} exists but is not a directory."


def test_expected_certificate_files_exist_with_correct_contents():
    alpha_path = CERT_DIR / "alpha.crt"
    bravo_path = CERT_DIR / "bravo.crt"

    # Presence
    for p in (alpha_path, bravo_path):
        assert p.exists(), f"Expected certificate file {p} to exist."
        assert p.is_file(), f"{p} exists but is not a regular file."

    # Contents (compare after stripping trailing newline differences)
    alpha_content = read_file(alpha_path).rstrip("\n")
    bravo_content = read_file(bravo_path).rstrip("\n")

    assert (
        alpha_content == ALPHA_EXPECTED.rstrip("\n")
    ), f"Contents of {alpha_path} do not match the expected certificate."
    assert (
        bravo_content == BRAVO_EXPECTED.rstrip("\n")
    ), f"Contents of {bravo_path} do not match the expected certificate."


def test_no_additional_crt_files_present():
    crt_files = list(CERT_DIR.rglob("*.crt"))
    expected = {CERT_DIR / "alpha.crt", CERT_DIR / "bravo.crt"}
    assert set(crt_files) == expected, (
        "Unexpected number of *.crt files detected in "
        f"{CERT_DIR}. Expected exactly {sorted(expected)}, but found "
        f"{sorted(crt_files)}."
    )


def test_compliance_logs_directory_absent():
    assert not COMPLIANCE_DIR.exists(), (
        f"The directory {COMPLIANCE_DIR} should NOT exist at the initial state. "
        "It must be created by the student solution."
    )