# test_initial_state.py
#
# Pytest suite that verifies the *initial* on-disk state expected by the
# assignment “Identify every world-writable regular file”.
#
# These tests must pass *before* the student runs their solution.  They confirm
# that the project tree already contains the exact files, directories and
# permission bits described in the task statement.
#
# IMPORTANT
# ---------
# * Do NOT check for the output artefacts the student must create
#   (e.g. /home/user/audit or the *.log file).  We only validate the
#   pre-existing layout under /home/user/project.
# * All failures raise explicit, easy-to-understand messages so that any
#   deviation from the canonical initial state is immediately obvious.
#
# Allowed imports: only stdlib + pytest
import os
import stat
from pathlib import Path

PROJECT_ROOT = Path("/home/user/project").resolve()

# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
def filemode(path: Path) -> str:
    """
    Return a 10-character permission string identical to `ls -l` output,
    e.g. '-rw-rw-rw-' or 'drwxrwxrwx'.
    """
    return stat.filemode(path.stat().st_mode)


def is_world_writable(path: Path) -> bool:
    """
    Return True if 'others' have write permission on the given path.
    Only meaningful for regular files (S_ISREG).
    """
    mode = path.stat().st_mode
    return bool(mode & stat.S_IWOTH)


# ----------------------------------------------------------------------
# Ground-truth taken from the task description
# ----------------------------------------------------------------------
EXPECTED_FILES = {
    PROJECT_ROOT / "data.db": "-rw-rw-rw-",
    PROJECT_ROOT / "file1.sh": "-rw-r--r--",
    PROJECT_ROOT / "file2.txt": "-rw-rw-r--",
    PROJECT_ROOT / "logs" / "app.log": "-rw-r--r--",
    PROJECT_ROOT / "scripts" / "install.sh": "-rwxr-xr-x",
    PROJECT_ROOT / "tmp" / "cache.tmp": "-rw-rw-rw-",
}

EXPECTED_DIRS = {
    PROJECT_ROOT: "drwx",  # we only check that it's a directory; mode bits are verified selectively
    PROJECT_ROOT / "logs": "drwxrwxrwx",
    PROJECT_ROOT / "scripts": "drwxr-xr-x",
    PROJECT_ROOT / "tmp": "drwxrwxrwt",
}

WORLD_WRITABLE_FILES = {
    PROJECT_ROOT / "data.db": "-rw-rw-rw-",
    PROJECT_ROOT / "tmp" / "cache.tmp": "-rw-rw-rw-",
}

# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------
def test_project_root_exists_and_is_directory():
    assert PROJECT_ROOT.exists(), f"{PROJECT_ROOT} is missing."
    assert PROJECT_ROOT.is_dir(), f"{PROJECT_ROOT} is not a directory."


def test_expected_directories_exist_and_modes():
    for path, expected_prefix in EXPECTED_DIRS.items():
        assert path.exists(), f"Directory {path} is missing."
        assert path.is_dir(), f"{path} exists but is not a directory."
        actual_mode = filemode(path)
        assert actual_mode.startswith(expected_prefix), (
            f"Directory {path} has mode {actual_mode!r}, "
            f"expected to start with {expected_prefix!r}."
        )


def test_expected_files_exist_and_modes():
    for path, expected_mode in EXPECTED_FILES.items():
        assert path.exists(), f"File {path} is missing."
        assert path.is_file(), f"{path} exists but is not a regular file."
        actual_mode = filemode(path)
        assert (
            actual_mode == expected_mode
        ), f"{path} has mode {actual_mode!r}, expected {expected_mode!r}."


def test_world_writable_files_are_exactly_the_expected_set():
    # Discover all world-writable *regular* files under the project directory
    discovered = {}
    for dirpath, dirnames, filenames in os.walk(PROJECT_ROOT):
        for name in filenames:
            p = Path(dirpath) / name
            try:
                st = p.stat(follow_symlinks=False)
            except FileNotFoundError:
                # File got removed between os.walk and stat; report clearly
                pytest.fail(f"File {p} disappeared while scanning.")
            if stat.S_ISREG(st.st_mode) and is_world_writable(p):
                discovered[p] = filemode(p)

    # Compare against ground truth
    assert (
        discovered == WORLD_WRITABLE_FILES
    ), (
        "The set of world-writable regular files does not match the expected "
        "initial state.\n"
        f"Expected: {WORLD_WRITABLE_FILES}\n"
        f"Found   : {discovered}"
    )