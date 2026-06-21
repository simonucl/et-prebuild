# test_initial_state.py
#
# This test-suite validates the *initial* state of the filesystem before
# the student’s solution is executed.  If any of these tests fail, the
# environment is not what the assignment anticipates and the evaluation
# should abort early.
#
# Rules enforced here:
#   • Repository layout under /home/user/repo/ is present.
#   • Both SSH configuration files exist with the exact expected contents.
#   • Only one file contains the forbidden string “PermitRootLogin yes”.
#   • The compliance directory and findings file do NOT exist yet.
#
# Standard library + pytest only.

from pathlib import Path
import pytest

HOME = Path("/home/user")
REPO_DIR = HOME / "repo"
CONFIG_DIR = REPO_DIR / "config"
COMPLIANCE_DIR = HOME / "compliance"
FINDINGS_FILE = COMPLIANCE_DIR / "root_login_findings.log"


@pytest.fixture(scope="module")
def sshd_config_contents():
    return [
        "# OpenSSH server configuration",
        "Port 22",
        "Protocol 2",
        "PasswordAuthentication yes",
        "# allow root login",
        "PermitRootLogin yes",
        "ChallengeResponseAuthentication no",
    ]


@pytest.fixture(scope="module")
def sshd_config_alt_contents():
    return [
        "# Alternative config",
        "Port 2222",
        "Protocol 2",
        "PermitRootLogin no",
    ]


def test_repository_structure_exists():
    assert REPO_DIR.is_dir(), f"Repository directory {REPO_DIR} is missing"
    assert CONFIG_DIR.is_dir(), f"Config directory {CONFIG_DIR} is missing"


def test_config_files_exist():
    f1 = CONFIG_DIR / "sshd_config"
    f2 = CONFIG_DIR / "sshd_config_alt"
    assert f1.is_file(), f"Expected file {f1} is missing"
    assert f2.is_file(), f"Expected file {f2} is missing"


def _read_lines(path: Path):
    """Read file and return list of lines without trailing newlines."""
    return path.read_text(encoding="utf-8").splitlines()


def test_sshd_config_exact_contents(sshd_config_contents):
    path = CONFIG_DIR / "sshd_config"
    lines = _read_lines(path)
    assert (
        lines == sshd_config_contents
    ), f"Contents of {path} do not match expected lines.\nExpected:\n{sshd_config_contents}\nActual:\n{lines}"


def test_sshd_config_alt_exact_contents(sshd_config_alt_contents):
    path = CONFIG_DIR / "sshd_config_alt"
    lines = _read_lines(path)
    assert (
        lines == sshd_config_alt_contents
    ), f"Contents of {path} do not match expected lines.\nExpected:\n{sshd_config_alt_contents}\nActual:\n{lines}"


def test_only_one_file_contains_permit_root_login_yes():
    """Exactly one file (sshd_config) must contain 'PermitRootLogin yes'."""
    offending_lines = []
    for file_path in CONFIG_DIR.rglob("*"):
        if not file_path.is_file():
            continue
        for idx, line in enumerate(_read_lines(file_path), start=1):
            if "PermitRootLogin yes" == line.strip():
                offending_lines.append((file_path, idx, line.strip()))
    assert (
        len(offending_lines) == 1
    ), f"Expected exactly one occurrence of 'PermitRootLogin yes' but found {len(offending_lines)}: {offending_lines}"
    # Verify that it is the correct file and on line 6
    file_path, idx, _ = offending_lines[0]
    expected_path = CONFIG_DIR / "sshd_config"
    assert (
        file_path == expected_path and idx == 6
    ), f"'PermitRootLogin yes' expected in {expected_path}:6 but found in {file_path}:{idx}"


def test_compliance_directory_absent():
    assert not COMPLIANCE_DIR.exists(), (
        f"Compliance directory {COMPLIANCE_DIR} should NOT exist before the "
        "student runs their solution."
    )


def test_findings_file_absent():
    assert not FINDINGS_FILE.exists(), (
        f"Findings file {FINDINGS_FILE} should NOT exist before the "
        "student runs their solution."
    )