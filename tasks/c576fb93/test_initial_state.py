# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state that must be
# present before the student’s solution runs.  It intentionally does **not**
# check for any of the output artefacts that the student is supposed to
# create later.

import pathlib
import textwrap

import pytest

HOME = pathlib.Path("/home/user")
LOG_ROOT = HOME / "mobile_ci" / "logs"

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def read_file(path: pathlib.Path) -> str:
    """
    Read a text file and normalise all line endings to '\n'.
    """
    data = path.read_text(encoding="utf-8")
    return data.replace("\r\n", "\n")


def normalise_expected(multiline_str: str) -> str:
    """
    Dedent the triple-quoted string and make sure it ends with exactly one
    trailing newline, so comparison with on-disk files is reliable.
    """
    txt = textwrap.dedent(multiline_str).lstrip("\n")
    if not txt.endswith("\n"):
        txt += "\n"
    return txt


# --------------------------------------------------------------------------- #
# Expected directory structure
# --------------------------------------------------------------------------- #
def test_logs_directory_exists():
    assert LOG_ROOT.is_dir(), (
        f"Expected directory {LOG_ROOT} to exist. "
        "Make sure the mobile_ci/logs directory structure is present."
    )


# --------------------------------------------------------------------------- #
# Expected set of daily log files
# --------------------------------------------------------------------------- #
EXPECTED_FILES = {
    LOG_ROOT / "build_2024-06-01.log",
    LOG_ROOT / "build_2024-06-02.log",
    LOG_ROOT / "build_2024-06-03.log",
}


def test_expected_log_files_present_and_no_extras():
    actual_files = {p for p in LOG_ROOT.glob("build_*.log") if p.is_file()}
    missing = EXPECTED_FILES - actual_files
    unexpected = actual_files - EXPECTED_FILES

    assert not missing, (
        "The following expected daily log files are missing:\n"
        + "\n".join(str(p) for p in sorted(missing))
    )
    assert not unexpected, (
        "Found unexpected extra log files in the logs directory:\n"
        + "\n".join(str(p) for p in sorted(unexpected))
    )


# --------------------------------------------------------------------------- #
# Expected file contents
# --------------------------------------------------------------------------- #
EXPECTED_CONTENT = {
    LOG_ROOT
    / "build_2024-06-01.log": normalise_expected(
        """
        === BUILD START ===
        JobID: 1001
        Variant: debug
        Timestamp: 2024-06-01T10:15:00Z
        Status: SUCCESS
        === BUILD END ===

        === BUILD START ===
        JobID: 1002
        Variant: release
        Timestamp: 2024-06-01T11:00:00Z
        Status: FAILURE
        Reason: Unit tests failed
        === BUILD END ===
        """
    ),
    LOG_ROOT
    / "build_2024-06-02.log": normalise_expected(
        """
        === BUILD START ===
        JobID: 1003
        Variant: debug
        Timestamp: 2024-06-02T09:05:00Z
        Status: FAILURE
        Reason: Gradle compilation error
        === BUILD END ===

        === BUILD START ===
        JobID: 1004
        Variant: release
        Timestamp: 2024-06-02T14:20:00Z
        Status: SUCCESS
        === BUILD END ===
        """
    ),
    LOG_ROOT
    / "build_2024-06-03.log": normalise_expected(
        """
        === BUILD START ===
        JobID: 1005
        Variant: release
        Timestamp: 2024-06-03T08:40:00Z
        Status: FAILURE
        Reason: Lint violations
        === BUILD END ===
        """
    ),
}


@pytest.mark.parametrize("file_path", sorted(EXPECTED_CONTENT.keys()))
def test_log_file_content_exact_match(file_path: pathlib.Path):
    assert file_path.exists(), f"Expected log file {file_path} does not exist."

    on_disk = read_file(file_path)
    expected = EXPECTED_CONTENT[file_path]

    assert (
        on_disk == expected
    ), f"Contents of {file_path} do not match the expected template."