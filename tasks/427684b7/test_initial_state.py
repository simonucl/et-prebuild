# test_initial_state.py
#
# This pytest suite validates that the operating-system / filesystem
# starts in a *clean* state **before** the student performs any actions
# for the “UTC sanity-check” task.  In particular, we make sure that
#
#   • /home/user/logs/utc_check.log does NOT yet exist **with the final,
#     correct 4-byte payload "UTC\n"**.
#   • If the parent directory (/home/user/logs) happens to exist for any
#     unrelated reason, that is acceptable provided the final file is
#     absent or wrong.
#
# The intent is to guarantee that the learner really has work to do.
# Should the file already be present *and* correct, the test fails with
# an explanatory message.
#
# Only Python’s standard library plus pytest is used, as required.

from pathlib import Path
import pytest

LOG_DIR = Path("/home/user/logs")
LOG_FILE = LOG_DIR / "utc_check.log"
EXPECTED_PAYLOAD = b"UTC\n"


def _file_has_expected_payload(path: Path) -> bool:
    """
    Helper: return True iff <path> exists, is a regular file, is 4 bytes
    long, and its exact byte sequence is b"UTC\\n".
    Any I/O issues are treated as “not correct yet”.
    """
    try:
        if not path.is_file():
            return False
        data = path.read_bytes()
        return data == EXPECTED_PAYLOAD
    except Exception:
        # Permissions or other I/O errors mean the file is not in the
        # final, correct state we are guarding against.
        return False


def test_utc_check_log_not_already_finished():
    """
    The deliverable /home/user/logs/utc_check.log must *not* already be
    present with the final, correct content **before** the student
    starts.  If it is, the exercise would be meaningless, so we fail
    loudly with guidance.
    """
    assert not _file_has_expected_payload(LOG_FILE), (
        f"The file {LOG_FILE} already exists with the exact expected "
        f"content {EXPECTED_PAYLOAD!r}.  The environment should start in "
        f"a clean state so the learner can create it themselves; please "
        f"remove or rename this file before running the exercise."
    )