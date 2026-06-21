# test_initial_state.py
#
# This pytest file validates the *initial* state of the operating‐system /
# file‐system before the learner performs any action.
#
# The exercise states that *after* completion there should be a directory
#   /home/user/iot_metrics
# containing a file
#   /home/user/iot_metrics/heartbeat.log
# whose exact byte-for-byte contents are
#   b"heartbeat: alive\n"
#
# In the initial state, however, that file must **not** yet exist *with the
# correct final contents*.  It is permissible if the directory does not exist
# at all, or if a file by that name exists but is **not** already correct.
#
# These tests therefore ENSURE that:
#   • Either the file is absent, **or**
#   • The file’s contents differ from the required final bytes.
#
# If the file is already present with the exact required contents, the test
# suite fails with a clear, actionable message—preventing the learner from
# receiving unwarranted credit for work they have not done.


import pathlib
import stat
import pytest


EXPECTED_BYTES = b"heartbeat: alive\n"
LOG_PATH = pathlib.Path("/home/user/iot_metrics/heartbeat.log")


def _file_has_correct_contents(path: pathlib.Path) -> bool:
    """
    Helper: return True if `path` exists, is a regular file,
    and its contents match EXPECTED_BYTES exactly.
    """
    if not path.exists():
        return False
    if not path.is_file():
        return False
    try:
        data = path.read_bytes()
    except Exception:
        # If the file cannot be read for any reason, treat as incorrect.
        return False
    return data == EXPECTED_BYTES


def test_heartbeat_log_not_already_finalised():
    """
    Verify that the heartbeat log is *not* already present with its final,
    byte-exact contents.  This ensures the learner actually performs the task.
    """
    assert not _file_has_correct_contents(
        LOG_PATH
    ), (
        "The file '/home/user/iot_metrics/heartbeat.log' already exists with the "
        "exact required contents (15 bytes: 'heartbeat: alive\\n').\n\n"
        "Initial-state validation failed: the workspace should *not* be pre-populated "
        "with the finished output.  Please remove or modify the file so that learners "
        "can complete the exercise themselves."
    )