# test_initial_state.py
#
# This pytest suite verifies that the environment is in its **initial**,
# pristine state before the student attempts the task.  In particular,
# it checks that none of the artefacts the student is expected to create
# already exist.  If any of these files are present, the test suite will
# fail with a descriptive message so that the exercise author can reset
# or clean the filesystem before the learner begins.


import os
from pathlib import Path

CRON_DIR = Path("/home/user/cron")
PROFILER_FILE = CRON_DIR / "myapp_profiler.cron"
STATUS_FILE = CRON_DIR / "creation_status.log"


def _pretty_path(path: Path) -> str:
    """
    Return a platform-independent, absolute, user-friendly representation
    of a pathlib.Path object.  This is used only for clearer assertion
    messages.
    """
    return str(path.resolve())


def test_profiler_cron_does_not_exist():
    """
    Ensure that /home/user/cron/myapp_profiler.cron is **absent** before
    the student’s solution runs.  The exercise requires the learner to
    create this file; if it already exists the initial state is invalid.
    """
    assert not PROFILER_FILE.exists(), (
        f"Pre-exercise sanity check failed: '{_pretty_path(PROFILER_FILE)}' "
        "should NOT exist yet.  Delete it before running the learner’s code."
    )


def test_status_log_does_not_exist():
    """
    Ensure that /home/user/cron/creation_status.log is **absent**.  The
    learner is responsible for creating this file, so its pre-existence
    indicates a polluted starting environment.
    """
    assert not STATUS_FILE.exists(), (
        f"Pre-exercise sanity check failed: '{_pretty_path(STATUS_FILE)}' "
        "should NOT exist yet.  Remove it before the student begins."
    )


def test_cron_directory_clean_or_absent():
    """
    The directory /home/user/cron may or may not exist at the start.
    If it *does* exist, confirm that it does not already contain either
    of the target files.  This guards against a scenario where the directory
    is pre-populated, yet the individual file checks above pass because
    the names differ slightly.
    """
    if not CRON_DIR.exists():
        # Directory does not exist — absolutely fine.
        return

    # Directory exists: verify that our two target artefacts are missing.
    unexpected_items = [
        p for p in (PROFILER_FILE, STATUS_FILE) if p.exists()
    ]
    assert not unexpected_items, (
        "Pre-exercise environment check failed: the following file(s) already "
        f"exist inside '{_pretty_path(CRON_DIR)}' but should not:\n"
        + "\n".join(f"  - {_pretty_path(p)}" for p in unexpected_items)
    )