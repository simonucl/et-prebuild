# test_initial_state.py
#
# Pytest suite that validates the filesystem *before* the student starts
# working on the “compression report” task.  It confirms that the original
# asset files exist exactly as described and that no artefacts that the
# student is supposed to create are present yet.

import os
import stat
import pytest

# --------------------------------------------------------------------------- #
# Constants used throughout the tests
# --------------------------------------------------------------------------- #
HOME = "/home/user"
ASSETS_DIR = os.path.join(HOME, "webapp", "assets")
PERFORMANCE_DIR = os.path.join(HOME, "performance")

MAIN_JS = os.path.join(ASSETS_DIR, "main.js")
STYLE_CSS = os.path.join(ASSETS_DIR, "style.css")

MAIN_GZ = MAIN_JS + ".gz"
STYLE_GZ = STYLE_CSS + ".gz"

REPORT_LOG = os.path.join(PERFORMANCE_DIR, "compression_report.log")

# Ground-truth about the files’ sizes and line content
MAIN_JS_LINE = "console.log('hello performance');\n"
STYLE_CSS_LINE = "body { margin: 0; padding: 0; }\n"

MAIN_JS_LINES = 100
STYLE_CSS_LINES = 100

MAIN_JS_SIZE = len(MAIN_JS_LINE.encode()) * MAIN_JS_LINES   # 34 * 100 = 3400
STYLE_CSS_SIZE = len(STYLE_CSS_LINE.encode()) * STYLE_CSS_LINES  # 32 * 100 = 3200


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _assert_regular_file(path: str) -> os.stat_result:
    """
    Assert that the given path exists and is a regular file.
    Returns the result of os.stat(path) on success.
    """
    assert os.path.exists(path), f"Expected file at '{path}' does not exist."
    st = os.stat(path)
    assert stat.S_ISREG(st.st_mode), f"Path '{path}' exists but is not a regular file."
    return st


# --------------------------------------------------------------------------- #
# Tests that verify the pre-existing files
# --------------------------------------------------------------------------- #
def test_original_files_exist():
    """Both original asset files must exist as regular files."""
    _assert_regular_file(MAIN_JS)
    _assert_regular_file(STYLE_CSS)


def test_original_file_sizes_and_contents():
    """
    Validate that the asset files have the exact byte-sizes and contents
    described in the specification.
    """
    # --- main.js ----------------------------------------------------------- #
    st_main = _assert_regular_file(MAIN_JS)
    assert st_main.st_size == MAIN_JS_SIZE, (
        f"'{MAIN_JS}' size mismatch: expected {MAIN_JS_SIZE} bytes, "
        f"found {st_main.st_size}."
    )
    with open(MAIN_JS, "r", encoding="utf-8") as fh:
        lines = fh.readlines()
    assert len(lines) == MAIN_JS_LINES, (
        f"'{MAIN_JS}' should contain {MAIN_JS_LINES} lines, "
        f"found {len(lines)}."
    )
    assert all(line == MAIN_JS_LINE for line in lines), (
        f"One or more lines in '{MAIN_JS}' do not match the expected content."
    )

    # --- style.css --------------------------------------------------------- #
    st_style = _assert_regular_file(STYLE_CSS)
    assert st_style.st_size == STYLE_CSS_SIZE, (
        f"'{STYLE_CSS}' size mismatch: expected {STYLE_CSS_SIZE} bytes, "
        f"found {st_style.st_size}."
    )
    with open(STYLE_CSS, "r", encoding="utf-8") as fh:
        lines = fh.readlines()
    assert len(lines) == STYLE_CSS_LINES, (
        f"'{STYLE_CSS}' should contain {STYLE_CSS_LINES} lines, "
        f"found {len(lines)}."
    )
    assert all(line == STYLE_CSS_LINE for line in lines), (
        f"One or more lines in '{STYLE_CSS}' do not match the expected content."
    )


# --------------------------------------------------------------------------- #
# Tests that ensure *no* student-generated artefacts are present yet
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "path,description",
    [
        (MAIN_GZ, "compressed JavaScript file main.js.gz"),
        (STYLE_GZ, "compressed CSS file style.css.gz"),
        (REPORT_LOG, "compression report log file"),
    ],
)
def test_no_generated_files_exist_yet(path, description):
    """
    The .gz files and the compression report must NOT exist prior to the
    student’s solution being run.
    """
    assert not os.path.exists(path), (
        f"Pre-condition failed: {description!s} ('{path}') already exists, "
        f"but it should not be present before the task is attempted."
    )


def test_performance_directory_absent():
    """
    The /home/user/performance directory should not exist yet.  The student’s
    solution is expected to create it.
    """
    assert not os.path.exists(PERFORMANCE_DIR), (
        f"Directory '{PERFORMANCE_DIR}' unexpectedly exists. "
        f"It should be created by the student’s script, not supplied in the "
        f"initial state."
    )