# test_initial_state.py
"""
Pytest suite that validates the *initial* operating-system / filesystem state
*before* the student performs any action.

It checks that:
1.  The projects directory and its immediate sub-directories exist.
2.  The internal sub-structure (selected files / sub-folders) exists.
3.  Each project directory currently consumes the disk space described in the
   task’s truth table, rounded **down** to whole MiB.
4.  The expected output file `/home/user/disk_usage_report.log` does **NOT**
   yet exist.

Only stdlib and pytest are used, and failures include clear explanations.
"""

import os
from pathlib import Path

import pytest

# Constants ------------------------------------------------------------------

HOME = Path("/home/user")
PROJECTS_DIR = HOME / "projects"
REPORT_FILE = HOME / "disk_usage_report.log"

# Expected first-level project directories and their sizes (MiB, rounded down)
EXPECTED_PROJECT_SIZES = {
    "app_alpha": 4,   # 4 MiB
    "app_beta": 2,    # 2 MiB
    "app_gamma": 6,   # 6 MiB
}

# Expected sub-structure for a quick smoke-check
EXPECTED_STRUCTURE = {
    "app_alpha": {"bin", "log", "README.md"},
    "app_beta": {"data", "docs"},
    "app_gamma": {"src", "tests", "report.pdf"},
}


# Helper ---------------------------------------------------------------------

def directory_size_bytes(path: Path) -> int:
    """
    Recursively walk *path* and return the cumulative size in bytes of all
    regular files contained therein.
    Directory entry sizes themselves are ignored because they are filesystem
    dependent and typically negligible for this level of granularity.
    """
    total = 0
    for root, _dirs, files in os.walk(path):
        for fname in files:
            try:
                total += (Path(root) / fname).stat().st_size
            except FileNotFoundError:
                # The file disappeared between os.walk listing and stat; ignore.
                pass
    return total


# Tests ----------------------------------------------------------------------

def test_projects_directory_exists():
    assert PROJECTS_DIR.is_dir(), (
        f"Required parent directory '{PROJECTS_DIR}' is missing."
    )


@pytest.mark.parametrize("proj_name", sorted(EXPECTED_PROJECT_SIZES))
def test_each_project_directory_exists(proj_name):
    proj_path = PROJECTS_DIR / proj_name
    assert proj_path.is_dir(), (
        f"Project directory '{proj_path}' is missing."
    )


@pytest.mark.parametrize("proj_name,expected_size_mib",
                         sorted(EXPECTED_PROJECT_SIZES.items()))
def test_project_directory_sizes(proj_name, expected_size_mib):
    """
    Verify that each project directory currently consumes the expected amount
    of disk space, **rounded down** to the nearest MiB.
    """
    proj_path = PROJECTS_DIR / proj_name
    size_bytes = directory_size_bytes(proj_path)
    size_mib = size_bytes // (1024 * 1024)  # rounded down
    assert size_mib == expected_size_mib, (
        f"Size mismatch for '{proj_path}': expected {expected_size_mib} MiB, "
        f"found {size_mib} MiB (raw bytes: {size_bytes})."
    )


@pytest.mark.parametrize("proj_name,expected_children",
                         sorted(EXPECTED_STRUCTURE.items()))
def test_expected_children_present(proj_name, expected_children):
    """
    Perform a quick existence check for key files/directories within each
    project.  This is *not* exhaustive, but enough to catch an incomplete
    set-up.
    """
    proj_path = PROJECTS_DIR / proj_name
    missing = []
    for child in expected_children:
        if not (proj_path / child).exists():
            missing.append(child)
    assert not missing, (
        f"In project '{proj_name}', the following expected items are missing: "
        f"{', '.join(missing)}"
    )


def test_report_file_not_yet_present():
    """
    The student has not executed their script yet, so the report file should
    NOT exist at this stage.
    """
    assert not REPORT_FILE.exists(), (
        f"Output file '{REPORT_FILE}' already exists before the task has "
        f"started; initial state should be clean."
    )