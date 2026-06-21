# test_initial_state.py
#
# Pytest suite to validate the initial filesystem state **before**
# the student performs any actions for the “release-notes tidy-up” task.
#
# Expectations:
#   1. /home/user/docs/user_guide.md must exist and contain the original,
#      unpatched text (v1.0 header, “recieve” typo, etc.).
#   2. /home/user/docs/fix_user_guide.patch must NOT exist yet.
#   3. /home/user/docs/verification.log must NOT exist yet.
#
# Any deviation from this baseline should fail with a clear,
# descriptive assertion message.
#
# NOTE: Uses only Python’s stdlib and pytest.

import textwrap
from pathlib import Path

DOCS_DIR = Path("/home/user/docs")
USER_GUIDE = DOCS_DIR / "user_guide.md"
PATCH_FILE = DOCS_DIR / "fix_user_guide.patch"
VERIFICATION_LOG = DOCS_DIR / "verification.log"


def test_docs_directory_exists():
    assert DOCS_DIR.is_dir(), f"Expected directory {DOCS_DIR} to exist."


def test_user_guide_initial_contents():
    assert USER_GUIDE.is_file(), (
        f"Expected initial guide file at {USER_GUIDE} to exist."
    )

    raw = USER_GUIDE.read_text(encoding="utf-8")

    expected = textwrap.dedent(
        """\
        # MyApp User Guide v1.0

        Welcome! In this document you will learn how to instal and configure MyApp.

        To recieve updates, subscribe to our newsletter.

        Happy hacking!
        """
    )

    # Ensure newline conventions (LF) exactly match expectations
    expected_with_final_nl = expected + "\n" if not expected.endswith("\n") else expected
    assert (
        raw == expected_with_final_nl
    ), (
        "The contents of user_guide.md do not match the expected initial state.\n"
        "If you have already patched the file, reset it to the original version "
        "before running these tests."
    )

    # Additional sanity check: file should be 7 lines long.
    assert len(raw.splitlines()) == 7, (
        "user_guide.md should contain exactly 7 lines in its initial state."
    )


def test_patch_file_absent():
    assert not PATCH_FILE.exists(), (
        f"Patch file {PATCH_FILE} should NOT exist before the task is performed."
    )


def test_verification_log_absent():
    assert not VERIFICATION_LOG.exists(), (
        f"Verification log {VERIFICATION_LOG} should NOT exist before the task is performed."
    )