# test_initial_state.py
#
# This pytest suite validates the *initial* operating-system / filesystem state
# expected **before** the student writes any solution code.  If any of these
# tests fail, the starting environment is not what the assignment describes,
# so the grader (or the student) should correct the setup first.

import os
from pathlib import Path

import pytest


HOME = Path("/home/user")
MANIFEST_DIR = HOME / "manifests"
POLICY_DIR = HOME / "policy_reports"
REPORT_FILE = POLICY_DIR / "latest_tag_report.log"

# --------------------------------------------------------------------------- #
# 1. Existence of required manifest files and directory                       #
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize(
    "path",
    [
        MANIFEST_DIR,
        MANIFEST_DIR / "deployment.yaml",
        MANIFEST_DIR / "statefulset.yaml",
    ],
)
def test_required_paths_exist(path):
    """Ensure that /home/user/manifests and the two YAML files exist."""
    assert path.exists(), f"Expected path missing: {path}"
    if path.is_file():
        assert path.stat().st_size > 0, f"File {path} is empty; expected contents."


# --------------------------------------------------------------------------- #
# 2. Validate exact line counts and key image references in each manifest     #
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize(
    ("filename", "expected_lines", "line_no", "expected_image"),
    [
        ("deployment.yaml", 19, 17, "image: nginx:latest"),
        ("statefulset.yaml", 20, 18, "image: redis:latest"),
    ],
)
def test_manifest_content(filename, expected_lines, line_no, expected_image):
    """
    Check:
      • total line count
      • that the specific line number contains the expected ':latest' image tag
    """
    file_path = MANIFEST_DIR / filename
    lines = file_path.read_text(encoding="utf-8").splitlines()

    # 1-based line numbers, as in task description
    assert (
        len(lines) == expected_lines
    ), f"{filename} should have {expected_lines} lines, found {len(lines)}."

    # Fetch the specific line (convert to 0-based index)
    try:
        actual_line = lines[line_no - 1]
    except IndexError:
        pytest.fail(
            f"{filename} was expected to have a line {line_no}, but has only {len(lines)} lines."
        )

    # Strip leading/trailing whitespace for a robust comparison
    assert (
        actual_line.strip() == expected_image
    ), f"{filename}: line {line_no} expected '{expected_image}', found '{actual_line.strip()}'."


# --------------------------------------------------------------------------- #
# 3. Ensure that the compliance report directory & file do NOT exist yet      #
# --------------------------------------------------------------------------- #

def test_policy_report_absence():
    """At the start, /home/user/policy_reports and its report file must NOT exist."""
    assert not POLICY_DIR.exists(), (
        f"Directory {POLICY_DIR} should not exist before the student runs their "
        "solution."
    )
    assert not REPORT_FILE.exists(), (
        f"Report file {REPORT_FILE} should not exist before the student runs their "
        "solution."
    )