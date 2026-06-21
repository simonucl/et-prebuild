# test_initial_state.py
#
# Pytest suite that validates the file-system state *before* the student
# performs any actions for the “standardise the release-directory layout”
# exercise.
#
# These tests assert ONLY the pre-existing conditions described in the task
# text.  Anything that should be created by the student (v1.2.0 directory,
# current symlink, per-release config.yml symlinks, operation log, …) is
# explicitly asserted *not* to exist yet so that the post-task tests can
# confirm their creation later on.
#
# The student’s environment must therefore satisfy every assertion in this
# file *before* they run their provisioning script.


import os
from pathlib import Path
import stat

# Constant paths for convenience
HOME = Path("/home/user")
APP_DIR = HOME / "app"
RELEASES_DIR = APP_DIR / "releases"
SHARED_DIR = APP_DIR / "shared"
LOGS_DIR = APP_DIR / "logs"

V100_DIR = RELEASES_DIR / "v1.0.0"
V110_DIR = RELEASES_DIR / "v1.1.0"
V120_DIR = RELEASES_DIR / "v1.2.0"          # Must NOT exist yet

CURRENT_SYMLINK = APP_DIR / "current"       # Must NOT exist yet
OP_LOG = LOGS_DIR / "symlink_setup.log"     # Must NOT exist yet


def _assert_is_dir(path: Path):
    assert path.exists(), f"Expected directory {path} to exist."
    assert path.is_dir(), f"Expected {path} to be a directory, but it is not."
    # Basic permission sanity: directory should be readable & executable
    mode = path.stat().st_mode
    assert mode & stat.S_IRUSR and mode & stat.S_IXUSR, (
        f"Directory {path} should be readable and traversable by the user."
    )


def _assert_file_with_content(path: Path, expected: str):
    assert path.exists(), f"Expected file {path} to exist."
    assert path.is_file(), f"Expected {path} to be a regular file."
    with path.open("r", encoding="utf-8") as f:
        content = f.read()
    assert content == expected, (
        f"File {path} has unexpected content.\n"
        f"Expected (repr): {expected!r}\n"
        f"Found    (repr): {content!r}"
    )


def test_top_level_directories_exist():
    """
    /home/user/app, /home/user/app/releases, /home/user/app/shared,
    and /home/user/app/logs must all exist prior to the task.
    """
    for directory in (APP_DIR, RELEASES_DIR, SHARED_DIR, LOGS_DIR):
        _assert_is_dir(directory)


def test_existing_release_directories_exist():
    """
    The two pre-existing releases (v1.0.0 and v1.1.0) must be present.
    """
    for rel_dir in (V100_DIR, V110_DIR):
        _assert_is_dir(rel_dir)


def test_release_directories_contain_only_readme():
    """
    Each pre-existing release directory must *only* contain README.txt with
    the correct content.
    """
    expected_files = {
        V100_DIR: "Version 1.0.0\n",
        V110_DIR: "Version 1.1.0\n",
    }

    for rel_dir, expected_content in expected_files.items():
        items = list(rel_dir.iterdir())
        assert items, f"{rel_dir} is empty; expected README.txt."
        assert len(items) == 1 and items[0].name == "README.txt", (
            f"{rel_dir} should contain exactly one file named README.txt, "
            f"but found: {[p.name for p in items]}"
        )
        _assert_file_with_content(items[0], expected_content)


def test_shared_config_exists_and_contents():
    """
    /home/user/app/shared/config.yml must exist with the two expected lines.
    """
    cfg = SHARED_DIR / "config.yml"
    _assert_file_with_content(cfg, "db: prod\ncache: redis\n")


def test_current_symlink_does_not_exist_yet():
    """
    The 'current' symbolic link must NOT exist before the student runs
    their provisioning steps.
    """
    assert not CURRENT_SYMLINK.exists(), (
        f"Symlink {CURRENT_SYMLINK} should NOT exist yet."
    )


def test_new_release_directory_does_not_exist_yet():
    """
    The v1.2.0 directory must be created by the student; it should not be
    present in the initial state.
    """
    assert not V120_DIR.exists(), (
        f"Directory {V120_DIR} should NOT exist prior to the task."
    )


def test_no_config_symlinks_in_release_dirs_yet():
    """
    The config.yml symlinks inside each release directory are created/updated
    by the task and therefore must not exist at this point.
    """
    for rel_dir in (V100_DIR, V110_DIR):
        candidate = rel_dir / "config.yml"
        assert not candidate.exists(), (
            f"Unexpected pre-existing file {candidate}; it should be absent."
        )


def test_operation_log_absent_initially():
    """
    The operation log is produced by the student script and therefore must
    not exist beforehand.
    """
    assert not OP_LOG.exists(), (
        f"Log file {OP_LOG} should NOT exist before the task is run."
    )