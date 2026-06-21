# test_initial_state.py
#
# This pytest suite validates that the starting operating-system state
# is suitable for the student to perform the task described in the
# assignment.  It purposefully AVOIDS looking for (or at) any of the
# files, directories, or symlinks that the student is expected to
# create later on.

import os
from pathlib import Path

import pytest


HOME_DIR = Path("/home/user")
QA_ENV_DIR = HOME_DIR / "qa_env"


def _attempt_write(test_path: Path) -> None:
    """
    Helper that tries to create and remove a small file inside
    `test_path.parent`.  Raises pytest.Fail if the operation fails.
    The file is removed in all cases to keep the environment pristine.
    """
    try:
        with test_path.open("w") as fh:
            fh.write("probe")
    except OSError as exc:      # covers PermissionError and friends
        pytest.fail(
            f"Cannot write inside directory {test_path.parent!s}: {exc}"
        )
    finally:
        # Best-effort cleanup; ignore if the file was never created.
        try:
            test_path.unlink()
        except FileNotFoundError:
            pass


def test_home_directory_exists_and_is_directory():
    """
    /home/user must exist and be a directory; the whole exercise
    depends on it.
    """
    assert HOME_DIR.exists(), "/home/user does not exist."
    assert HOME_DIR.is_dir(), "/home/user exists but is not a directory."


def test_home_directory_is_writable():
    """
    The student needs to be able to create files and directories under
    /home/user, so make sure write permission is available.
    """
    probe_file = HOME_DIR / f".pytest_write_probe_{os.getpid()}"
    _attempt_write(probe_file)


def test_qa_env_is_creatable_or_writable():
    """
    The work area /home/user/qa_env must either:
      • not exist yet (in which case we must be able to create it), or
      • exist and be writable.

    The test makes a minimal write probe to verify permissions and
    leaves the directory unchanged when it is pre-existing.
    """
    if QA_ENV_DIR.exists():
        assert QA_ENV_DIR.is_dir(), (
            "/home/user/qa_env exists but is not a directory."
        )
        probe_file = QA_ENV_DIR / f".pytest_write_probe_{os.getpid()}"
        _attempt_write(probe_file)
    else:
        # Try to create the directory and then remove it again so as
        # not to interfere with the student's future work.
        try:
            QA_ENV_DIR.mkdir(parents=False)
        except OSError as exc:
            pytest.fail(
                f"Unable to create the directory /home/user/qa_env: {exc}"
            )
        else:
            # Clean up after ourselves.
            try:
                QA_ENV_DIR.rmdir()
            except OSError as exc:
                pytest.fail(
                    f"Could not remove the test directory /home/user/qa_env "
                    f"that was just created: {exc}"
                )