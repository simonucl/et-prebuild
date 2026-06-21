# test_initial_state.py
"""
Pytest suite to assert the *initial* filesystem layout for the ETL project.

These checks run **before** the student implements the security scanner.
They intentionally avoid looking for any of the expected output artefacts
(e.g. security/scan_secrets, scan_report.json, scan_run.log).

The suite verifies only the presence and basic contents of the starter files
shipped with the project.
"""

import re
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constants                                                                   
# --------------------------------------------------------------------------- #
ROOT = Path("/home/user/etl_project").resolve()

EXISTING_FILES = {
    "extract": ROOT / "extract.py",
    "transform": ROOT / "transform.py",
    "loader": ROOT / "load" / "loader.py",
    "readme": ROOT / "README.md",
}


@pytest.fixture(scope="session")
def root_dir():
    assert ROOT.is_dir(), (
        f"Required project root directory '{ROOT}' not found. "
        "Ensure the initial project has been copied to the correct location."
    )
    return ROOT


@pytest.mark.parametrize("key", EXISTING_FILES.keys())
def test_required_files_exist(root_dir, key):
    """Each starter file must be present."""
    path = EXISTING_FILES[key]
    assert path.is_file(), f"Expected starter file '{path}' is missing."


def test_extract_py_content():
    """extract.py should contain a callable extract() definition."""
    path = EXISTING_FILES["extract"]
    content = path.read_text().splitlines()
    assert any("def extract" in line for line in content), (
        "extract.py does not appear to define an `extract()` function."
    )
    # Expect exactly 5 lines in the prototype
    assert len(content) == 5, (
        f"extract.py should initially contain 5 lines, found {len(content)}."
    )


def test_loader_py_content():
    """load/loader.py must be a short stub (3 lines)."""
    path = EXISTING_FILES["loader"]
    lines = path.read_text().splitlines()
    assert len(lines) == 3, (
        f"load/loader.py should contain 3 lines in the starter template, "
        f"found {len(lines)}."
    )
    assert any("def load" in line for line in lines), (
        "load/loader.py does not define a `load()` function as expected."
    )


def test_transform_py_contains_hard_coded_secret():
    """
    transform.py is expected to *already* contain one hard-coded AWS secret
    on line 3 so the student’s future scanner has something to detect.
    """
    path = EXISTING_FILES["transform"]
    lines = path.read_text().splitlines()

    secret_regexes = [
        re.compile(r"(?i)aws[_-]?secret"),
        re.compile(r"(?i)aws[_-]?access[_-]?key"),
    ]

    # Ensure there are at least 3 lines so that line index 2 exists.
    assert len(lines) >= 3, (
        "transform.py is expected to be at least 3 lines long "
        "to house the dummy AWS secret."
    )

    offending_line = lines[2]  # 1-based line number 3

    assert any(regex.search(offending_line) for regex in secret_regexes), (
        "Line 3 of transform.py does not contain the expected dummy "
        "AWS credential string that the future scanner must flag."
    )


def test_readme_exists_and_is_nonempty():
    """README.md must exist and contain text."""
    path = EXISTING_FILES["readme"]
    content = path.read_text().strip()
    assert content, "README.md exists but is empty."
    assert "ETL" in content.upper(), "README.md should mention 'ETL' project."