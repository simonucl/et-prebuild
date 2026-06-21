# test_initial_state.py
#
# Pytest suite to validate the starting filesystem state *before* the student
# executes any solution commands for the “dataset manifest” exercise.
#
# We verify that:
#   1. /home/user/datasets exists and is a directory.
#   2. The first–level dataset sub-directories (astronomy, climate, epidemiology)
#      exist and are directories.
#   3. Each expected data file exists as a regular readable file.
#   4. No unexpected items are present inside each dataset directory
#      (i.e. the directory contains exactly the files listed in the task
#      description and no additional files or sub-directories).

from pathlib import Path
import os
import stat
import pytest

ROOT = Path("/home/user/datasets")

# Mapping of dataset sub-directory → iterable of **regular files** expected inside it
EXPECTED_STRUCTURE = {
    "astronomy": ["galaxies.tsv"],
    "climate": ["temp.csv", "rainfall.csv"],
    "epidemiology": ["flu_2020.csv", "covid_2020.csv", "measles_2019.csv"],
}


def _is_regular_readable_file(path: Path) -> bool:
    """
    Helper: True if `path` exists, is a regular file, and is readable
    by the current user.
    """
    if not path.exists() or not path.is_file():
        return False
    # Check readability bit for user
    st_mode = path.stat().st_mode
    return bool(st_mode & stat.S_IRUSR)


def test_root_directory_exists():
    assert ROOT.exists(), f"Expected directory {ROOT} to exist."
    assert ROOT.is_dir(), f"Expected {ROOT} to be a directory."


@pytest.mark.parametrize("subdir, expected_files", EXPECTED_STRUCTURE.items())
def test_dataset_subdirectory_contents(subdir, expected_files):
    sub_path = ROOT / subdir
    assert sub_path.exists(), f"Expected sub-directory {sub_path} to exist."
    assert sub_path.is_dir(), f"Expected {sub_path} to be a directory."

    # Convert to set for order-insensitive comparison
    expected_set = {sub_path / fn for fn in expected_files}

    # Gather actual regular files directly inside the sub-directory
    actual_set = {
        p
        for p in sub_path.iterdir()
        if p.is_file()
    }

    # Verify presence of all expected files
    missing = expected_set - actual_set
    assert not missing, (
        f"Missing expected file(s) in {sub_path}: "
        + ", ".join(str(p) for p in sorted(missing))
    )

    # Verify there are no unexpected files
    unexpected = actual_set - expected_set
    assert not unexpected, (
        f"Unexpected extra file(s) in {sub_path}: "
        + ", ".join(str(p) for p in sorted(unexpected))
    )

    # Finally, ensure each expected file is a *readable* regular file
    unreadable = [p for p in expected_set if not _is_regular_readable_file(p)]
    assert not unreadable, (
        f"The following expected file(s) are not regular readable files: "
        + ", ".join(str(p) for p in unreadable)
    )