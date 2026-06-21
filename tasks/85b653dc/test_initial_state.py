# test_initial_state.py
#
# This pytest suite verifies that the workspace is still in its pristine
# “before-the-student-starts” condition.
#
# For this particular exercise, NOTHING should have been created yet:
#   • The log file  /home/user/analysis/timezone_analysis.log
#   • (Optionally) even the directory  /home/user/analysis/
#
# If any of these artefacts already exist, it means someone has jumped ahead
# or a previous run did not clean up correctly.  In that case we raise a clear
# assertion so the learner knows what must be removed before beginning.
#
# The tests intentionally do *not* touch anything outside the standard
# library and pytest, per the project guidelines.

from pathlib import Path

HOME = Path("/home/user")
ANALYSIS_DIR = HOME / "analysis"
LOG_FILE = ANALYSIS_DIR / "timezone_analysis.log"


def test_log_file_absent():
    """
    The target log file must NOT exist before the student starts the task.
    Its presence would indicate that the exercise was already completed or
    that a previous run left residual data, both of which break a clean start.
    """
    assert not LOG_FILE.exists(), (
        f"The file {LOG_FILE} already exists but should NOT be present at the "
        f"start of the exercise.  Please remove it before running the task."
    )


def test_directory_clean_or_absent():
    """
    The parent directory may or may not exist.  If it *does* exist, it must be
    completely empty so that leftover files from earlier attempts cannot mask
    mistakes in the current run.
    """
    if ANALYSIS_DIR.exists():
        unexpected = [p for p in ANALYSIS_DIR.iterdir() if p != LOG_FILE]
        assert not unexpected, (
            f"The directory {ANALYSIS_DIR} should be empty before the task "
            f"begins, but it contains: {', '.join(map(str, unexpected))}"
        )