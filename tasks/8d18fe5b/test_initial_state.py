# test_initial_state.py
#
# This test-suite verifies that the filesystem is in a *clean* state
# before the student begins the exercise.  None of the directories,
# files, or symlinks that the task asks the student to create should
# exist yet.

from pathlib import Path
import os
import pytest

BASE_DIR = Path("/home/user/mlops")

# All artefacts that must *not* be present before the student starts.
MUST_NOT_EXIST = [
    BASE_DIR,
    BASE_DIR / "exp1",
    BASE_DIR / "exp2",
    BASE_DIR / "exp3",
    BASE_DIR / "exp1" / "artefact.txt",
    BASE_DIR / "exp2" / "artefact.txt",
    BASE_DIR / "exp3" / "artefact.txt",
    BASE_DIR / "current",
    BASE_DIR / "latest_artefact.txt",
    BASE_DIR / "experiment_symlink_log.txt",
]


@pytest.mark.parametrize("path", MUST_NOT_EXIST)
def test_pristine_filesystem(path: Path):
    """
    Ensure that none of the artefacts that the student is expected to
    create are already present.  A pre-existing file, directory, or
    symlink would make the task trivial or break idempotency.
    """
    # Generic message for a clean, instructional failure.
    msg = (
        f"\nUnexpected pre-existing path detected:\n"
        f"    {path}\n"
        f"Please start the task in a clean environment where the path above "
        f"does *not* exist."
    )

    # Resolve symlinks in case somebody tried to be clever
    # and hid the artefact through an indirection.
    try:
        exists = path.exists() or path.is_symlink()
    except FileNotFoundError:
        # Rare corner case on some filesystems; treat as non-existent.
        exists = False

    assert not exists, msg


def test_no_residual_entries_inside_base():
    """
    If /home/user/mlops already exists for whatever reason (perhaps the
    student created it for a previous, unrelated exercise), *nothing*
    inside it should clash with what the current task will create.
    """
    if not BASE_DIR.exists():
        pytest.skip("/home/user/mlops does not exist yet — good starting point.")

    banned = {"exp1", "exp2", "exp3", "current", "latest_artefact.txt", "experiment_symlink_log.txt"}
    offending = sorted(p for p in os.listdir(BASE_DIR) if p in banned)

    assert not offending, (
        "\nThe following entries already exist inside /home/user/mlops but "
        "must not be present before the task starts:\n    "
        + "\n    ".join(offending)
    )