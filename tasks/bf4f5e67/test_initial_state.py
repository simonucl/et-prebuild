# test_initial_state.py
#
# This pytest suite validates the expected *initial* state of the
# filesystem before the student’s solution runs.  It checks that the
# pre-staged “project” workspace exists exactly as specified.
#
# NOTE: Per the grading rules *do not* test for the presence (or
# absence) of the output file /home/user/permission_audit.log.  Only
# the pre-existing project tree is verified here.

import os
import stat
import pytest

# ----------------------------------------------------------------------
# Expected initial objects.
#
# Each entry is a tuple of:
#   (absolute_path, expected_octal_mode, expected_kind)
# where expected_kind ∈ {'file', 'dir'}.
# ----------------------------------------------------------------------
EXPECTED_LAYOUT = [
    ("/home/user/project",                       0o755, 'dir'),
    ("/home/user/project/config.cfg",            0o644, 'file'),
    ("/home/user/project/scripts",               0o755, 'dir'),
    ("/home/user/project/scripts/build.sh",      0o750, 'file'),
    ("/home/user/project/data",                  0o700, 'dir'),
    ("/home/user/project/data/raw.txt",          0o600, 'file'),
]

# ----------------------------------------------------------------------
# Parametrised tests ----------------------------------------------------
# ----------------------------------------------------------------------

@pytest.mark.parametrize("path, expected_mode, kind", EXPECTED_LAYOUT)
def test_path_exists_with_correct_type(path, expected_mode, kind):
    """
    Ensure that the path exists and is of the correct type (file/dir).
    """
    assert os.path.exists(path), f"Expected {path!r} to exist, but it does not."

    if kind == 'file':
        assert os.path.isfile(path), f"Expected {path!r} to be a regular file."
    elif kind == 'dir':
        assert os.path.isdir(path), f"Expected {path!r} to be a directory."
    else:  # Should never happen—defensive programming
        pytest.fail(f"Internal test error: unknown kind {kind!r} for {path!r}.")


@pytest.mark.parametrize("path, expected_mode, _", EXPECTED_LAYOUT)
def test_path_has_expected_permissions(path, expected_mode, _):
    """
    Verify that each path has the exact numeric permission bits expected.
    Only the low 9 bits (rwx for user/group/other) are checked.
    """
    st_mode = os.stat(path).st_mode
    actual_mode = stat.S_IMODE(st_mode)          # isolate permission bits (e.g. 0o755)

    assert actual_mode == expected_mode, (
        f"Incorrect permissions on {path!r}: "
        f"expected {oct(expected_mode)[2:]}, got {oct(actual_mode)[2:]}."
    )