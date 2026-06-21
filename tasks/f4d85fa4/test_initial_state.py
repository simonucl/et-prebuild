# test_initial_state.py
#
# Pytest suite that validates the expected *initial* operating‐system / filesystem
# state **before** the student’s solution runs.  It checks that the raw scan files
# are present and intact, and that no backup artefacts have been created yet.
#
# The tests purposefully *fail fast* with clear, actionable error messages so that
# students immediately understand what prerequisite is missing in their workspace.
#
# Constraints respected:
#   • Uses only stdlib + pytest
#   • Absolute paths are used for every filesystem check
#   • Does *not* touch or rely on any of the yet-to-be-created output files
#   • Single file; can be parsed directly by the grading harness
#
# Assumed base paths
#   /home/user/vuln_scans/raw/
#   /home/user/vuln_scans/backup/  (must **not** exist yet)

from pathlib import Path
import pytest

HOME = Path("/home/user")
BASE_DIR = HOME / "vuln_scans"
RAW_DIR = BASE_DIR / "raw"
BACKUP_DIR = BASE_DIR / "backup"

RAW_FILES = {
    RAW_DIR / "initial_network.nmap": "# Nmap 7.93 scan initiated",
    RAW_DIR / "ssh_bruteforce.hydra": "Hydra v9.1",
    RAW_DIR / "webdir_enum.gobuster": "Gobuster v3.3.0",
}

ARCHIVE_PATH = BACKUP_DIR / "scans_backup_20230915.tar.gz"
MANIFEST_PATH = BACKUP_DIR / "scans_backup_20230915.sha256"
LOG_PATH = BACKUP_DIR / "backup.log"


@pytest.mark.order(1)
def test_raw_directory_exists():
    """Ensure the raw scan directory exists and is a directory."""
    assert RAW_DIR.exists(), f"Required directory missing: {RAW_DIR}"
    assert RAW_DIR.is_dir(), f"Expected {RAW_DIR} to be a directory."


@pytest.mark.order(2)
@pytest.mark.parametrize(
    "filepath,needle",
    [(p, s) for p, s in RAW_FILES.items()],
)
def test_each_raw_file_present_and_contains_expected_snippet(filepath: Path, needle: str):
    """
    Confirm that each expected raw file exists, is a regular file,
    is non-empty, and contains a distinctive substring.
    """
    assert filepath.exists(), f"Required file missing: {filepath}"
    assert filepath.is_file(), f"Expected {filepath} to be a regular file."

    content = filepath.read_text(encoding="utf-8", errors="ignore")
    assert content, f"{filepath} is empty."
    assert needle in content, (
        f"{filepath} does not appear to have the expected contents: "
        f"substring '{needle}' not found."
    )


@pytest.mark.order(3)
def test_backup_artifacts_absent():
    """
    Ensure no backup artefacts (directory, archive, manifest, log) are present yet.
    The student’s solution is supposed to create these; they must *not* pre-exist.
    """
    assert not BACKUP_DIR.exists(), (
        f"Backup directory {BACKUP_DIR} already exists. "
        "The environment should be pristine before the solution runs."
    )
    # If, for some reason, the directory exists but the grader still wants to allow it,
    # we additionally guard against already-created artefacts.
    assert not ARCHIVE_PATH.exists(), f"Archive should not exist yet: {ARCHIVE_PATH}"
    assert not MANIFEST_PATH.exists(), f"Manifest should not exist yet: {MANIFEST_PATH}"
    assert not LOG_PATH.exists(), f"Log file should not exist yet: {LOG_PATH}"