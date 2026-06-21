# test_initial_state.py
#
# Pytest suite to verify that the operating-system / file-system
# is in its pristine, pre-exercise state.
#
# The student *must* create every resource mentioned in the task;
# therefore none of those paths may exist at this point.
#
# If any path below already exists, the test will fail with a clear
# explanation so the learner immediately sees what needs to be fixed.

import os
import pytest

# Absolute paths that must *not* exist before the student starts.
ROOT_DIR = "/home/user/firewall_monitoring"
EXPECTED_PATHS = [
    ROOT_DIR,
    os.path.join(ROOT_DIR, "iptables_sample.log"),
    os.path.join(ROOT_DIR, "alert_firewall.sh"),
    os.path.join(ROOT_DIR, "alert_status.log"),
    os.path.join(ROOT_DIR, "cron_entry.txt"),
    os.path.join(ROOT_DIR, "README.txt"),
]


def _human_type(path: str) -> str:
    """
    Helper that says whether a path currently exists as a file,
    directory, symbolic link, or something else.  Used purely to
    provide clearer assertion messages.
    """
    if os.path.islink(path):
        return "symbolic link"
    if os.path.isdir(path):
        return "directory"
    if os.path.isfile(path):
        return "file"
    if os.path.exists(path):
        return "special file"
    return "non-existent path"


def test_firewall_monitoring_root_absent():
    """
    The working directory for the exercise must *not* exist yet.
    """
    assert not os.path.exists(
        ROOT_DIR
    ), (
        f"The directory '{ROOT_DIR}' already exists "
        f"({ _human_type(ROOT_DIR) }).\n"
        "Start with a clean slate so the exercise can create it."
    )


@pytest.mark.parametrize("path", EXPECTED_PATHS[1:])  # skip ROOT_DIR; already covered above
def test_individual_paths_absent(path):
    """
    None of the task-specific files should be present before the student
    runs their solution.  Each is checked individually so that any
    premature creation is flagged explicitly.
    """
    assert not os.path.exists(
        path
    ), (
        f"Found unexpected { _human_type(path) } at '{path}'.\n"
        "The path must not exist before the monitoring workflow is built."
    )