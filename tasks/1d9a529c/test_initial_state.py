# test_initial_state.py
#
# This pytest suite validates the machine *before* the learner starts
# working on the assignment.  It confirms that the provided on-premises
# INI file (service.ini) is in place and unmodified, that the working
# directory exists, and that no output artefacts are present yet.

import os
from pathlib import Path

CLOUD_DIR = Path("/home/user/cloud-migration")
INI_FILE = CLOUD_DIR / "service.ini"
OUTPUT_DIR = CLOUD_DIR / "output"

# The exact contents that must be present in /home/user/cloud-migration/service.ini
EXPECTED_INI_CONTENT = (
    "[compute]\n"
    "instance_type=t3.medium\n"
    "region=us-east-1\n"
    "\n"
    "[database]\n"
    "engine=postgres\n"
    "version=13\n"
    "storage=100\n"
    "\n"
    "[network]\n"
    "cidr=10.0.0.0/16\n"
    "ports=22,80,443\n"
)

def test_cloud_directory_exists():
    """The base directory /home/user/cloud-migration/ must already exist."""
    assert CLOUD_DIR.is_dir(), (
        f"Expected directory {CLOUD_DIR} to exist, but it does not."
    )

def test_service_ini_exists():
    """service.ini must exist in the base directory."""
    assert INI_FILE.is_file(), (
        f"Expected file {INI_FILE} to exist, but it does not."
    )

def test_service_ini_contents_are_exact():
    """service.ini must match the canonical contents byte-for-byte."""
    actual = INI_FILE.read_text(encoding="utf-8")
    assert actual == EXPECTED_INI_CONTENT, (
        "The content of service.ini does not match the expected initial fixture.\n"
        "---- Expected ----\n"
        f"{EXPECTED_INI_CONTENT!r}\n"
        "---- Actual ----\n"
        f"{actual!r}"
    )

def test_no_extra_files_in_cloud_directory():
    """
    The base directory should contain exactly one regular file: service.ini.
    Subdirectories or additional files would indicate a polluted starting state.
    """
    files = sorted(p.name for p in CLOUD_DIR.iterdir() if p.is_file())
    assert files == ["service.ini"], (
        f"Unexpected files present in {CLOUD_DIR}. "
        f"Expected only ['service.ini'] but found {files}."
    )

def test_output_directory_absent_initially():
    """
    The /home/user/cloud-migration/output/ directory must NOT exist yet.
    It will be created by the learner during the exercise.
    """
    assert not OUTPUT_DIR.exists(), (
        f"Directory {OUTPUT_DIR} should not exist before the task starts."
    )