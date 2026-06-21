# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the operating-system /
# filesystem *before* the student performs any of the required steps for the
# “cloud migration” task.  The assertions below guarantee that none of the
# artefacts expected *after* the task are already present and that the user’s
# ~/.bashrc has not yet been modified.
#
# If any of these tests fail it means the environment is **not clean** and the
# subsequent grading of the student’s work would be unreliable.

import os
from pathlib import Path

import pytest


HOME = Path("/home/user")
CLOUD_DIR = HOME / "cloud_migration"
CONFIG_FILE = CLOUD_DIR / "config.env"
LOG_FILE = CLOUD_DIR / "setup_verification.log"
BASHRC = HOME / ".bashrc"
EXPECTED_BASHRC_TRAILER = (
    "source /home/user/cloud_migration/config.env  # added by migration-setup"
)


@pytest.mark.describe("Initial filesystem must be clean")
class TestInitialState:
    def test_cloud_migration_directory_may_exist_but_must_be_clean(self):
        """
        The task asks the student to create /home/user/cloud_migration if it
        does not exist.  Regardless of whether the directory is present, the
        two files that *will* be created inside it (config.env, setup_verification.log)
        must NOT exist yet.
        """
        # The directory itself may or may not exist – that's fine.
        if CLOUD_DIR.exists():
            assert CLOUD_DIR.is_dir(), (
                f"Expected {CLOUD_DIR} to be a directory if it exists, "
                f"but found something else."
            )

        assert not CONFIG_FILE.exists(), (
            f"{CONFIG_FILE} already exists, but it must be created by the "
            f"student.  Remove it so the environment is clean."
        )
        assert not LOG_FILE.exists(), (
            f"{LOG_FILE} already exists, but it must be created by the "
            f"student.  Remove it so the environment is clean."
        )

    def test_bashrc_not_already_modified(self):
        """
        The student will append a specific `source …` line to ~/.bashrc.
        Ensure this line is NOT already present as the very last line (and, for
        robustness, not anywhere in the file).  If ~/.bashrc does not exist,
        that is also acceptable.
        """
        if not BASHRC.exists():
            # No .bashrc → definitely not modified yet; nothing more to test.
            return

        bashrc_text = BASHRC.read_text(encoding="utf-8", errors="replace")
        lines = bashrc_text.splitlines()

        # Assert the file does not already contain the expected trailer line.
        assert EXPECTED_BASHRC_TRAILER not in lines, (
            f"The line:\n\n    {EXPECTED_BASHRC_TRAILER}\n\n"
            f"is already present in {BASHRC}.  The initial environment must be "
            f"clean; remove the line so the student can add it."
        )

        # Extra safety: check that the last *non-empty* line is not the trailer.
        for line in reversed(lines):
            if line.strip():  # skip empty / whitespace-only lines at EOF
                last_non_empty = line
                break
        else:
            last_non_empty = ""

        assert last_non_empty != EXPECTED_BASHRC_TRAILER, (
            f"The last non-empty line of {BASHRC} is already the expected "
            f"trailer line.  The file must not be pre-modified."
        )