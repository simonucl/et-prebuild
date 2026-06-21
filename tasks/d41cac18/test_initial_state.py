# test_initial_state.py
#
# Pytest suite to validate the initial operating-system / filesystem
# state *before* the student performs any actions.

import os
import stat
import pytest

HOME = "/home/user"
RAW_DIR = os.path.join(HOME, "raw_data")

EXPECTED_FILES = {
    os.path.join(RAW_DIR, "test_cases.list"): """\
TC001:UserLogin:env1
TC002:UserLogout:env1
TC003:PurchaseItem:env2
TC004:CancelOrder:env2
TC005:ApplyCoupon:env3
""",
    os.path.join(RAW_DIR, "statuses.log"): """\
TC001,PASS
TC002,FAIL
TC003,PASS
TC004,SKIP
TC005,FAIL
""",
    os.path.join(RAW_DIR, "durations.csv"): """\
TC001;1023
TC002;980
TC003;2150
TC004;1500
TC005;1175
""",
}


def _read_text(path: str) -> str:
    """
    Read a text file using universal newlines so that any newline style
    in the file is normalised to '\n'.  This makes it possible to compare
    the file’s content to the Python string literals below in a platform
   -independent way.  The file is opened in binary mode first so that we
    can raise a helpful error if it is not a regular file.
    """
    st = os.stat(path)
    if not stat.S_ISREG(st.st_mode):
        pytest.fail(f"Expected {path!r} to be a regular file, "
                    f"but its mode is {oct(st.st_mode)}")

    # Re-open in text mode with universal newlines for comparison.
    with open(path, "r", encoding="utf-8", newline=None) as f:
        return f.read()


def test_raw_data_directory_exists_and_is_directory():
    assert os.path.isdir(RAW_DIR), (
        f"Required directory {RAW_DIR!r} is missing "
        f"or is not recognised as a directory."
    )


@pytest.mark.parametrize("path,expected_content", EXPECTED_FILES.items())
def test_expected_file_exists(path, expected_content):
    assert os.path.isfile(path), (
        f"Expected file {path!r} does not exist."
    )


@pytest.mark.parametrize("path,expected_content", EXPECTED_FILES.items())
def test_expected_file_contents_exact(path, expected_content):
    """
    Validate that the file contents EXACTLY match the specification.
    Trailing newlines are significant and therefore included in the
    expected_content literals above.
    """
    actual = _read_text(path)
    assert actual == expected_content, (
        f"Contents of {path!r} do not match the required initial state.\n\n"
        f"--- Expected ---\n{expected_content!r}\n"
        f"--- Actual ---\n{actual!r}\n"
    )