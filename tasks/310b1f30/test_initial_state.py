# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the filesystem
# before the student performs any actions.  It confirms that the three
# pre-existing objects are present with their original, deliberately
# insecure permissions.  The tests must all pass *before* the student
# begins the task; afterwards they are expected to fail once the
# student has fixed the permissions.
#
# NOTE:  Intentionally **do not** test for the presence or absence of
#        /home/user/mobile-pipeline/permission_audit.log because that
#        file is considered output material according to the rubric.

import os
import stat
import pytest

# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
def _mode(path):
    """
    Return the permission bits (e.g. 0o755) for a filesystem object.
    """
    return stat.S_IMODE(os.stat(path).st_mode)


def _octal(mode_int):
    """
    Convert an int (e.g. 0o755) to its three-digit octal string '755'.
    """
    return f"{mode_int:o}"


# ----------------------------------------------------------------------
# Parameterised specification of the initial state
# ----------------------------------------------------------------------
SPEC = [
    {
        "path": "/home/user/mobile-pipeline/build_android.sh",
        "is_dir": False,
        "expected_mode": 0o777,
    },
    {
        "path": "/home/user/mobile-pipeline/logs",
        "is_dir": True,
        "expected_mode": 0o755,
    },
    {
        "path": "/home/user/mobile-pipeline/release_signing.key",
        "is_dir": False,
        "expected_mode": 0o644,
    },
]


# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------
@pytest.mark.parametrize("entry", SPEC)
def test_presence_and_mode(entry):
    """
    Verify that each required filesystem object exists with the *original*
    expected permissions.
    """
    path         = entry["path"]
    is_dir       = entry["is_dir"]
    expected     = entry["expected_mode"]

    assert os.path.exists(path), (
        f"Required path is missing: {path!r}"
    )

    if is_dir:
        assert os.path.isdir(path), (
            f"Expected a directory at {path}, but it is not a directory."
        )
    else:
        assert os.path.isfile(path), (
            f"Expected a file at {path}, but it is not a regular file."
        )

    actual_mode = _mode(path)
    assert actual_mode == expected, (
        f"Incorrect permissions for {path}.\n"
        f"  Expected: {_octal(expected)}\n"
        f"  Found:    {_octal(actual_mode)}"
    )


def test_build_android_shebang():
    """
    Confirm that /home/user/mobile-pipeline/build_android.sh starts with
    the correct shebang ('#!/bin/bash').
    """
    script_path = "/home/user/mobile-pipeline/build_android.sh"
    assert os.path.isfile(script_path), (
        f"Script {script_path} is missing."
    )

    with open(script_path, "r", encoding="utf-8", errors="ignore") as fp:
        first_line = fp.readline().rstrip("\n")

    expected_shebang = "#!/bin/bash"
    assert first_line == expected_shebang, (
        f"build_android.sh has wrong or missing shebang.\n"
        f"  Expected first line: {expected_shebang!r}\n"
        f"  Found:               {first_line!r}"
    )