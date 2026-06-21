# test_initial_state.py
#
# Pytest suite to validate the **initial** OS/FS state _before_ the student
# performs any action for the “tiny disk-usage snapshot” exercise.
#
# Rules verified:
#   • /home/user/logs exists and is a directory.
#   • Exactly three regular log files are present:
#       - access.log  (500  bytes, 100 lines)
#       - error.log   (250  bytes, 50  lines)
#       - app.log     (1000 bytes, 200 lines)
#   • No extra regular files are in /home/user/logs.
#   • Each file’s content is the literal ASCII string "line\n" repeated
#     the expected number of times.

import os
import stat
import pytest

LOG_DIR = "/home/user/logs"

EXPECTED_FILES = {
    "access.log": {"size": 500, "lines": 100},
    "error.log":  {"size": 250, "lines": 50},
    "app.log":    {"size": 1000, "lines": 200},
}


@pytest.fixture(scope="module")
def log_dir_contents():
    """Yield a dict mapping file name → os.stat_result for regular files in LOG_DIR."""
    if not os.path.exists(LOG_DIR):
        pytest.fail(f"Required directory {LOG_DIR!r} does not exist.")
    if not os.path.isdir(LOG_DIR):
        pytest.fail(f"Expected {LOG_DIR!r} to be a directory.")
    contents = {}
    for name in os.listdir(LOG_DIR):
        path = os.path.join(LOG_DIR, name)
        st = os.lstat(path)
        if stat.S_ISREG(st.st_mode):  # only count regular files
            contents[name] = st
    return contents


def test_exact_regular_files_present(log_dir_contents):
    """Ensure that exactly the expected log files (and only those) exist."""
    expected_set = set(EXPECTED_FILES)
    present_set = set(log_dir_contents)
    missing = expected_set - present_set
    extra   = present_set - expected_set
    assert not missing, (
        f"Missing expected file(s) in {LOG_DIR}: {', '.join(sorted(missing))}"
    )
    assert not extra, (
        f"Unexpected extra regular file(s) in {LOG_DIR}: {', '.join(sorted(extra))}\n"
        "Directory should contain only the three specified log files _before_ the student runs."
    )
    assert len(present_set) == 3, "There should be exactly three regular log files."


@pytest.mark.parametrize("filename,meta", EXPECTED_FILES.items())
def test_file_size_and_line_count(filename, meta):
    """Verify each file's byte-size and line count as described."""
    path = os.path.join(LOG_DIR, filename)

    # Confirm existence and file type
    assert os.path.exists(path), f"Required file {path} is missing."
    assert os.path.isfile(path), f"{path} must be a regular file (not directory, symlink, etc.)."

    # Size check
    actual_size = os.path.getsize(path)
    expected_size = meta["size"]
    assert actual_size == expected_size, (
        f"{filename}: expected size {expected_size} bytes, found {actual_size} bytes."
    )

    # Content / line-count check
    with open(path, "rb") as f:
        content = f.read()

    # Every line must literally be b"line\n"
    if content:
        lines = content.split(b"\n")
        # After split the last element will be b'' because file ends with '\n'
        if lines and lines[-1] == b'':
            lines = lines[:-1]
    else:
        lines = []

    expected_lines = meta["lines"]
    assert len(lines) == expected_lines, (
        f"{filename}: expected {expected_lines} lines, found {len(lines)}."
    )
    bad_lines = [i for i, ln in enumerate(lines, 1) if ln != b"line"]
    assert not bad_lines, (
        f"{filename}: line(s) {bad_lines} do not exactly equal the string 'line'."
    )