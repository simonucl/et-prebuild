# test_initial_state.py
#
# Pytest suite that validates the initial on-disk state before the
# student performs any action for the “world-writable sweep” exercise.
#
# The tests assert that the given directory tree already exists exactly
# as described in the task statement.  Any mismatch will raise a clear
# explanatory failure so that students immediately see what is wrong
# with their environment (and not with their solution).

import os
import stat
import pytest


AUDIT_ROOT = "/home/user/audit_data"


@pytest.mark.parametrize(
    "path, kind, size, perm_oct",
    [
        # path                               kind      size  permissions
        (f"{AUDIT_ROOT}",                   "dir",    None, "755"),
        (f"{AUDIT_ROOT}/secure.txt",        "file",    512, "644"),
        (f"{AUDIT_ROOT}/public.log",        "file",   2048, "666"),  # world-writable
        (f"{AUDIT_ROOT}/notes",             "file",    256, "600"),
        (f"{AUDIT_ROOT}/subdir",            "dir",    None, "755"),
        (f"{AUDIT_ROOT}/subdir/expose.sh",  "file",   1024, "777"),  # world-writable
    ],
)
def test_expected_entities_present(path, kind, size, perm_oct):
    """
    Assert that every expected file or directory exists with the correct
    type, permissions, and (for files) size.
    """
    assert os.path.exists(path), f"Expected {path!r} to exist."

    st = os.stat(path, follow_symlinks=False)

    if kind == "file":
        assert stat.S_ISREG(st.st_mode), f"{path} should be a regular file."
        assert st.st_size == size, (
            f"{path}: expected size {size} bytes, found {st.st_size} bytes."
        )
    elif kind == "dir":
        assert stat.S_ISDIR(st.st_mode), f"{path} should be a directory."
    else:
        pytest.fail(f"Internal test error: unknown kind {kind!r} for {path!r}")

    # Permissions: compare the lowest three (or four) octal digits.
    actual_perm = f"{st.st_mode & 0o777:o}"
    assert actual_perm == perm_oct.lstrip("0"), (
        f"{path}: expected permissions {perm_oct}, found {actual_perm}."
    )


def test_no_unexpected_entries(tmp_path_factory):
    """
    Ensure that no extra files or directories exist directly under
    /home/user/audit_data other than the ones specified.  (We do not
    recurse into subdirectories for this check.)
    """
    expected_top_level = {
        "secure.txt",
        "public.log",
        "notes",
        "subdir",
    }

    try:
        entries = set(os.listdir(AUDIT_ROOT))
    except FileNotFoundError:
        pytest.fail(f"Directory {AUDIT_ROOT} is missing entirely.")

    unexpected = entries - expected_top_level
    assert not unexpected, (
        f"Found unexpected item(s) in {AUDIT_ROOT}: {', '.join(sorted(unexpected))}"
    )