# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating system
# before the student’s solution runs.  It confirms that the prerequisite
# log files are present with the exact expected content and that no output
# artefacts created by the student solution exist yet.
#
# The checks deliberately fail with clear error messages if anything is
# missing or already present.

import os
from pathlib import Path

HOME_DIR = Path("/home/user")
PIPELINE_LOG_DIR = HOME_DIR / "pipeline" / "logs"
ERROR_LOG = PIPELINE_LOG_DIR / "error.log"
PIPELINE_LOG = PIPELINE_LOG_DIR / "pipeline.log"

SUPPORT_TARBALL = HOME_DIR / "support_bundle.tgz"
COLLECTION_LOG = HOME_DIR / "collection.log"


def _read_bytes(path: Path) -> bytes:
    """Utility: read file as bytes, helpful for precise comparison."""
    with path.open("rb") as f:
        return f.read()


def test_pipeline_log_directory_exists():
    """Ensure the pipeline log directory exists."""
    assert PIPELINE_LOG_DIR.is_dir(), (
        f"Required directory {PIPELINE_LOG_DIR} is missing. "
        "The initial machine should already contain the pipeline log directory."
    )


def test_required_log_files_exist():
    """Both required log files must exist."""
    missing = [p for p in (ERROR_LOG, PIPELINE_LOG) if not p.is_file()]
    assert not missing, (
        "The following required log file(s) are missing: "
        + ", ".join(str(p) for p in missing)
    )


def test_error_log_content_is_exact():
    """error.log content must match the expected single line exactly."""
    expected = b"[2023-01-01 00:00:01] ERROR Pipeline crashed at step 3\n"
    actual = _read_bytes(ERROR_LOG)
    assert actual == expected, (
        f"{ERROR_LOG} content mismatch.\n"
        f"Expected: {expected!r}\n"
        f"Actual:   {actual!r}"
    )


def test_pipeline_log_content_is_exact():
    """pipeline.log content must match the expected single line exactly."""
    expected = b"[2023-01-01 00:00:00] INFO  Pipeline started\n"
    actual = _read_bytes(PIPELINE_LOG)
    assert actual == expected, (
        f"{PIPELINE_LOG} content mismatch.\n"
        f"Expected: {expected!r}\n"
        f"Actual:   {actual!r}"
    )


def test_no_output_files_exist_yet():
    """
    Before the student runs their solution, the support bundle and collection
    log MUST NOT exist.  Their presence would indicate the task has already
    been performed or the workspace is dirty.
    """
    unexpected = [p for p in (SUPPORT_TARBALL, COLLECTION_LOG) if p.exists()]
    assert not unexpected, (
        "The following file(s) already exist but should not before the task "
        "is attempted: " + ", ".join(str(p) for p in unexpected)
    )