# test_initial_state.py
# Pytest suite to validate the initial workspace state for the mobile CI task.
#
# Rules & scope
# 1.  Verify only the PRE-EXISTING items that must be in place _before_ the
#    learner performs any action.
# 2.  Never check for, or mention, any of the artefacts the learner is asked
#    to create (e.g. the reports directory or the failure report file).
# 3.  Use only the Python standard library + pytest.
# 4.  All assertion messages must clearly describe what is missing or wrong.

import pathlib
import pytest


# --------------------------------------------------------------------------- #
# Constants describing the expected initial state.
# --------------------------------------------------------------------------- #
CI_ROOT = pathlib.Path("/home/user/mobile_ci")
BUILD_LOG = CI_ROOT / "build_pipeline.log"

EXPECTED_BUILD_LOG_LINES = [
    "[2023-08-21 10:01:03] BUILD 101: core - SUCCESS\n",
    "[2023-08-21 10:05:47] BUILD 102: ui - FAILED\n",
    "[2023-08-21 10:12:11] BUILD 103: networking - SUCCESS\n",
    "[2023-08-21 10:15:29] BUILD 104: feature-auth - FAILED\n",
    "[2023-08-21 10:22:58] BUILD 105: feature-payments - FAILED\n",
    "[2023-08-21 10:30:42] BUILD 106: analytics - SUCCESS\n",
    "[2023-08-21 10:33:27] BUILD 107: push-notifications - SUCCESS\n",
    "[2023-08-21 10:38:55] BUILD 108: ui - FAILED\n",
]


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_ci_root_directory_exists():
    """/home/user/mobile_ci must exist and be a directory."""
    assert CI_ROOT.exists(), (
        f"Required directory {CI_ROOT} is missing. "
        "The initial workspace must be present."
    )
    assert CI_ROOT.is_dir(), (
        f"{CI_ROOT} exists but is not a directory. "
        "Expected a directory for the mobile CI workspace."
    )


def test_build_log_exists_and_contents():
    """Validate that build_pipeline.log exists and contains the exact 8 lines."""
    assert BUILD_LOG.exists(), (
        f"Required file {BUILD_LOG} is missing. "
        "The task relies on this historical build log."
    )
    assert BUILD_LOG.is_file(), (
        f"{BUILD_LOG} exists but is not a regular file."
    )

    # Read the entire file in binary mode first to verify the last byte is '\n'
    with BUILD_LOG.open("rb") as fh:
        content_bytes = fh.read()
        assert content_bytes.endswith(b"\n"), (
            "build_pipeline.log must end with a single Unix LF (\\n) newline."
        )

    # Now read in text mode for line-by-line comparison.
    with BUILD_LOG.open("r", encoding="utf-8") as fh:
        lines = fh.readlines()

    assert lines == EXPECTED_BUILD_LOG_LINES, (
        "build_pipeline.log contents do not match the expected initial state.\n"
        "Expected lines:\n"
        + "".join(EXPECTED_BUILD_LOG_LINES)
        + "\nActual lines:\n"
        + "".join(lines)
    )


@pytest.mark.skip(reason="Placeholder for future initial-state tests")
def test_placeholder():
    """
    This test is intentionally skipped.  It exists solely to indicate where
    additional initial-state validations could be placed in the future without
    affecting the current grading rubric.
    """
    pass