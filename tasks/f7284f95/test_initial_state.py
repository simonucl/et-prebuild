# test_initial_state.py
#
# This pytest suite verifies the *initial* state of the machine
# before the learner carries out the assignment described in the
# prompt.  In particular, it confirms that the diagnostics artefacts
# do **not** exist yet, and that the Linux /proc files required to
# build them **do** exist.  If any of these checks fail, the learner
# starts from an unexpected state and should clean it up before
# proceeding.

import os
import stat
import shutil
import pytest
from pathlib import Path

HOME = Path("/home/user")
DIAG_DIR = HOME / "diagnostics"
CSV_FILE = DIAG_DIR / "system_snapshot.csv"
README_FILE = DIAG_DIR / "README.txt"

# ---------- Helper utilities -------------------------------------------------


def _exists(p: Path) -> bool:
    """Return True if the path exists (symlink, file, or directory)."""
    return p.exists() or p.is_symlink()


# ---------- Tests ------------------------------------------------------------


def test_home_directory_exists():
    """Sanity-check: /home/user must be present for the exercise."""
    assert HOME.is_dir(), (
        f"Expected the home directory {HOME} to exist, "
        "but it is missing. This environment is not set up for the exercise."
    )


@pytest.mark.parametrize(
    "proc_file",
    ["/proc/uptime", "/proc/meminfo", "/proc/loadavg"],
)
def test_required_proc_files_exist(proc_file):
    """Confirm that the Linux /proc files we will query later are present."""
    assert os.path.isfile(proc_file), (
        f"Required system file {proc_file} is missing. "
        "The exercise presumes a Linux environment with /proc mounted."
    )


@pytest.mark.parametrize("binary", ["date", "hostname"])
def test_required_binaries_available(binary):
    """Ensure that the minimal external commands we intend to use are available."""
    found = shutil.which(binary)
    assert found is not None, (
        f"The command '{binary}' is not found in PATH. "
        "It is required to generate the diagnostic snapshot."
    )


def test_diagnostics_directory_absent():
    """
    Before the student starts, /home/user/diagnostics must *not* exist.
    A pre-existing directory could contain old files and confuse grading.
    """
    assert not _exists(DIAG_DIR), (
        f"The directory {DIAG_DIR} already exists. "
        "Please start from a clean state by removing it before continuing."
    )


@pytest.mark.parametrize("path_obj", [CSV_FILE, README_FILE])
def test_output_files_absent(path_obj):
    """Neither system_snapshot.csv nor README.txt should exist yet."""
    assert not _exists(path_obj), (
        f"Found unexpected file at {path_obj}. "
        "Remove any leftover artefacts before starting the task."
    )