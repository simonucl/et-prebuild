# test_initial_state.py
"""
Pytest suite that validates the *initial* state of the operating system
before the student starts working on the “block_suspicious_ip.sh” task.

These tests make sure that nothing related to the required deliverable
is already present so that the student must create everything from
scratch.

Only standard library + pytest are used.
"""
import os
from pathlib import Path
import stat
import pytest

HOME_DIR = Path("/home/user")
FIREWALL_DIR = HOME_DIR / "firewall"
BLOCK_SCRIPT = FIREWALL_DIR / "block_suspicious_ip.sh"


def test_firewall_directory_absent_or_empty():
    """
    The directory /home/user/firewall should either not exist or be empty
    at the start of the exercise.

    Rationale:
    • Ensures the student creates the directory if missing.
    • Prevents pre-populated files from giving the student undue hints
      or causing false positives in later grading.
    """
    if not FIREWALL_DIR.exists():
        # Good: directory is absent
        assert True
    else:
        assert FIREWALL_DIR.is_dir(), (
            f"{FIREWALL_DIR} exists but is not a directory; "
            "please remove or rename it before starting the task."
        )

        contents = list(FIREWALL_DIR.iterdir())
        assert (
            len(contents) == 0
        ), (
            f"{FIREWALL_DIR} is expected to be empty at the start, "
            f"but it already contains: {[p.name for p in contents]}"
        )


def test_block_script_does_not_exist_yet():
    """
    The script /home/user/firewall/block_suspicious_ip.sh must not exist
    before the student creates it.
    """
    assert not BLOCK_SCRIPT.exists(), (
        f"{BLOCK_SCRIPT} already exists; remove it so the student can "
        "create the file as part of this exercise."
    )


def _mode_to_str(mode_int: int) -> str:
    """
    Helper: convert a file mode integer (from stat.S_IMODE) into the
    string representation produced by `ls -l`, e.g. '-rwx------'.
    """
    perms = ['-'] * 9
    flags = [
        (stat.S_IRUSR, 0, 'r'),
        (stat.S_IWUSR, 1, 'w'),
        (stat.S_IXUSR, 2, 'x'),
        (stat.S_IRGRP, 3, 'r'),
        (stat.S_IWGRP, 4, 'w'),
        (stat.S_IXGRP, 5, 'x'),
        (stat.S_IROTH, 6, 'r'),
        (stat.S_IWOTH, 7, 'w'),
        (stat.S_IXOTH, 8, 'x'),
    ]
    for flag, idx, char in flags:
        if mode_int & flag:
            perms[idx] = char
    return '-' + ''.join(perms)


@pytest.mark.parametrize("path_obj", [FIREWALL_DIR, BLOCK_SCRIPT])
def test_paths_absent_have_no_permissions(path_obj):
    """
    If the path objects are absent, they naturally have no permissions.
    This parametric test makes sure that *if* they exist (perhaps due to
    accidental leftovers), they are flagged for cleanup before the
    exercise begins.
    """
    if path_obj.exists():
        mode = stat.S_IMODE(path_obj.stat().st_mode)
        mode_str = _mode_to_str(mode)
        pytest.fail(
            f"{path_obj} already exists with permissions {mode_str}. "
            "The initial state must not contain this path."
        )