# test_initial_state.py
#
# This pytest suite verifies that the working environment is in the
# expected *initial* (pre-task) state for the “backup-and-restore”
# exercise.  Nothing produced by the student’s forthcoming workflow
# should exist yet: neither the sample file, nor the backup archive,
# nor the two-line report file.  Detecting any of those artefacts now
# would indicate that the environment is contaminated and would give
# the student an unfair head start.

import os
from pathlib import Path
import tarfile
import pytest

HOME = Path("/home/user")
WORKDIR = HOME / "restore_test"

# The artefacts that must **not** exist before the student starts.
ORIGINAL_TXT = WORKDIR / "original.txt"
BACKUP_TGZ = WORKDIR / "backup.tgz"
REPORT_LOG = WORKDIR / "restore_report.log"

@pytest.mark.describe("Validate pristine state before the exercise starts")
class TestInitialState:
    def test_home_directory_exists(self):
        assert HOME.is_dir(), (
            f"Expected the home directory {HOME} to exist. "
            "The testing environment itself is broken."
        )

    def test_working_directory_may_or_may_not_exist(self):
        # The task says “create … if it does not yet exist”, so either
        # situation is acceptable.  We merely assert that, if it *does*
        # exist, it is indeed a directory (and not, say, a file or a symlink).
        if WORKDIR.exists():
            assert WORKDIR.is_dir(), (
                f"{WORKDIR} already exists but is not a directory. "
                "Please remove or rename the object so the student can "
                "create the required working directory."
            )

    @pytest.mark.parametrize(
        "path_",
        [ORIGINAL_TXT, BACKUP_TGZ, REPORT_LOG],
        ids=["original.txt", "backup.tgz", "restore_report.log"],
    )
    def test_no_required_files_are_present_yet(self, path_):
        assert not path_.exists(), (
            f"The file {path_} should NOT exist before the student begins "
            "the exercise.  Remove it so the student can create it from scratch."
        )

    def test_no_preexisting_backup_archive(self):
        """
        Even if another file named ‘backup.tgz’ exists somewhere else,
        it must not be in the working directory.  Should someone have
        created /home/user/restore_test/backup.tgz already, make sure
        it is removed so the student does the work.
        """
        if BACKUP_TGZ.exists():
            with pytest.raises(AssertionError):
                # Force a clear, dedicated failure message that also
                # hints at the unwanted presence of an archive.
                assert False, (
                    f"Found unexpected backup archive at {BACKUP_TGZ}. "
                    "The initial state must *not* include a pre-made archive."
                )

    def test_tar_utility_is_available(self):
        """
        The student will need the ‘tar’ utility.  Ensure it is available
        on the PATH.  We cannot import tarfile’s external command usage,
        so we fall back to shutil.which.
        """
        import shutil

        tar_path = shutil.which("tar")
        assert tar_path is not None, (
            "The ‘tar’ program is not available in the execution environment. "
            "Install it or make sure it is on the PATH before the exercise begins."
        )