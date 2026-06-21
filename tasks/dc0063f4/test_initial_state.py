# test_initial_state.py
"""
Pytest suite that validates the **initial** state of the filesystem before the
student performs any actions for the micro-benchmark task.

The checks are intentionally strict so that any deviation from the described
starting conditions is reported with a clear, actionable error message.
"""

import os
import stat
import textwrap

import pytest

HOME = "/home/user"
APP_DIR = os.path.join(HOME, "app")
V1_SCRIPT = os.path.join(APP_DIR, "v1", "process_data.sh")
V2_SCRIPT = os.path.join(APP_DIR, "v2", "process_data.sh")
DEPLOY_DIR = os.path.join(HOME, "deploy")          # must NOT exist yet
CSV_PATH = os.path.join(DEPLOY_DIR, "perf_results.csv")  # must NOT exist yet


def _assert_is_executable_file(path: str) -> None:
    """
    Helper that asserts a path exists, is a regular file and has its executable
    bit set for the current user.
    """
    assert os.path.exists(path), f"Expected file '{path}' does not exist."
    st = os.stat(path)
    assert stat.S_ISREG(st.st_mode), f"'{path}' exists but is not a regular file."
    assert os.access(path, os.X_OK), f"'{path}' is not marked as executable."


@pytest.mark.parametrize(
    "path, expected_sleep",
    [
        (V1_SCRIPT, "sleep 1"),
        (V2_SCRIPT, "sleep 0.25"),
    ],
)
def test_script_files_exist_and_are_executable(path, expected_sleep):
    """Both process_data.sh scripts must exist and be executable."""
    _assert_is_executable_file(path)

    # Check for required snippets inside the script so that students start
    # from the exact baseline implementation.
    with open(path, "r", encoding="utf-8") as fh:
        content = fh.read()

    # 1. Shebang
    assert content.startswith("#!/usr/bin/env bash"), (
        f"File '{path}' must start with the shebang '#!/usr/bin/env bash'."
    )

    # 2. Echo statement (fuzzy match to avoid Unicode dash pitfalls)
    version = "v1" if "v1" in path else "v2"
    expected_echo_fragment = f"echo \"Processing data"
    assert expected_echo_fragment in content and version in content, (
        f"File '{path}' should contain an echo line mentioning '{version}'."
    )

    # 3. Sleep duration
    assert expected_sleep in content, (
        f"File '{path}' should contain the line '{expected_sleep}'."
    )

    # 4. UNIX line endings only (no CRLF)
    with open(path, "rb") as fh_bin:
        raw = fh_bin.read()
    assert b"\r\n" not in raw, f"File '{path}' must use UNIX line endings only."


def test_directory_layout():
    """
    Verify that the expected directory structure under /home/user/app exists.
    """
    for subdir in ("v1", "v2"):
        dir_path = os.path.join(APP_DIR, subdir)
        assert os.path.isdir(dir_path), (
            f"Required directory '{dir_path}' is missing."
        )

    # Check that no unexpected deploy directory is present yet.
    assert not os.path.exists(DEPLOY_DIR), (
        "The directory '/home/user/deploy' must NOT exist before the benchmark "
        "is executed."
    )
    # Likewise, ensure the CSV file does not pre-exist.
    assert not os.path.exists(CSV_PATH), (
        f"File '{CSV_PATH}' should not exist in the initial state."
    )


def test_readme_for_future_reference():
    """
    Optional sanity check: provide a helpful failure message if the whole
    /home/user/app directory tree is absent (mis-mounted volume, etc.).
    """
    assert os.path.isdir(APP_DIR), textwrap.dedent(
        f"""
        The directory '{APP_DIR}' is missing. This typically indicates that the
        project source tree was not mounted or unpacked correctly in the
        execution environment. Ensure that the following structure exists:

            /home/user/app/v1/process_data.sh
            /home/user/app/v2/process_data.sh
        """
    )