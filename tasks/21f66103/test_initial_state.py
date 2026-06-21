# test_initial_state.py
#
# This test-suite validates that the *initial* filesystem state
# matches the specification *before* the student performs any
# actions.  If any assertion fails, the accompanying error message
# pinpoints exactly what is missing or inconsistent.
#
# NOTE:  We intentionally do NOT test for the presence of any files
#        or directories that the student must create as part of the
#        assignment (e.g. /home/user/archives or the tarball).

import os
from pathlib import Path
import pytest


# ---------------------------------------------------------------------------
# Paths that MUST exist before the task starts
# ---------------------------------------------------------------------------
HOME = Path("/home/user").resolve()

# Directories
EXPECTED_DIRS = [
    HOME / "provisioning",
    HOME / "provisioning" / "scripts",
    HOME / "provisioning" / "scripts" / "utils",
]

# Files with their expected contents (byte-for-byte)
EXPECTED_FILES_AND_CONTENTS = {
    HOME / "provisioning" / "scripts" / "deploy.sh": (
        "#!/bin/bash\n"
        "echo \"Deploying application...\"\n"
    ),
    HOME / "provisioning" / "scripts" / "teardown.sh": (
        "#!/bin/bash\n"
        "echo \"Tearing down...\"\n"
    ),
    HOME / "provisioning" / "scripts" / "utils" / "common.sh": (
        "#!/bin/bash\n"
        "log() { echo \"[`date`] $1\"; }\n"
    ),
    HOME / "provisioning" / "scripts" / "README.md": (
        "# Provisioning Scripts\n"
        "This directory contains helper scripts for deploying and tearing down infrastructure.\n"
    ),
}


# ---------------------------------------------------------------------------
# Directory existence
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("path", EXPECTED_DIRS)
def test_required_directories_exist(path: Path):
    assert path.is_dir(), f"Required directory is missing: {path}"


# ---------------------------------------------------------------------------
# File existence
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("path", EXPECTED_FILES_AND_CONTENTS.keys())
def test_required_files_exist(path: Path):
    assert path.is_file(), f"Required file is missing: {path}"


# ---------------------------------------------------------------------------
# File content verification
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("path,expected_content", EXPECTED_FILES_AND_CONTENTS.items())
def test_required_files_have_correct_content(path: Path, expected_content: str):
    actual_content = path.read_text(encoding="utf-8")
    assert (
        actual_content == expected_content
    ), (
        f"Content mismatch in {path}.\n\n"
        f"EXPECTED:\n{expected_content!r}\n\n"
        f"FOUND:\n{actual_content!r}\n"
    )