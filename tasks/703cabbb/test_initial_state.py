# test_initial_state.py
"""
Pytest suite to verify the initial filesystem state BEFORE the student performs
any actions for the “deploybot / ci-admins” exercise.

What must already be true:

1. Directory /home/user/ci_access/ exists.
2. File /home/user/ci_access/users.csv exists and contains EXACTLY the two
   starter lines, each terminated by a single Unix newline:
       alice,ci-viewers\n
       bob,ci-operators\n
3. Directory /home/user/ci_access/artifacts MUST NOT exist yet.
4. File /home/user/ci_access/audit.log MUST NOT exist yet.

If any of these pre-conditions are violated, the exercise itself cannot be
graded reliably, so we fail fast with clear error messages.
"""
from pathlib import Path

import pytest

CI_ROOT = Path("/home/user/ci_access")
USERS_CSV = CI_ROOT / "users.csv"
ARTIFACTS_DIR = CI_ROOT / "artifacts"
AUDIT_LOG = CI_ROOT / "audit.log"


def test_ci_access_directory_exists():
    assert CI_ROOT.is_dir(), (
        f"Expected directory {CI_ROOT} to exist before the exercise starts."
    )


def test_users_csv_initial_content():
    # 1. File must exist
    assert USERS_CSV.exists(), f"Expected {USERS_CSV} to exist."

    # 2. Read contents exactly as text
    contents = USERS_CSV.read_text(encoding="utf-8")

    # 3. File must end with a single trailing newline
    assert contents.endswith(
        "\n"
    ), f"{USERS_CSV} must end with a single Unix newline (\\n)."

    # 4. Split into lines (drop the trailing newline, so no empty string)
    lines = contents.rstrip("\n").split("\n")

    expected_lines = ["alice,ci-viewers", "bob,ci-operators"]

    # 5. Must have exactly the two starter lines, in any order, with no extras
    assert sorted(lines) == sorted(
        expected_lines
    ), (
        f"{USERS_CSV} must contain exactly these two lines (order unimportant):\n"
        f"  {expected_lines}\n"
        f"Current contents:\n  {lines}"
    )


def test_artifacts_directory_absent():
    assert not ARTIFACTS_DIR.exists(), (
        f"Directory {ARTIFACTS_DIR} should NOT exist yet. "
        "The student will create it."
    )


def test_audit_log_absent():
    assert not AUDIT_LOG.exists(), (
        f"File {AUDIT_LOG} should NOT exist yet. "
        "The student will create it."
    )