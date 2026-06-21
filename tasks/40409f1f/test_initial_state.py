# test_initial_state.py
#
# Pytest suite that validates the _initial_ state of the operating-system /
# filesystem **before** the student starts working on the “network_lab”
# exercise.  None of the artefacts that the final grader will look for
# should exist yet.  If any of them are already present, the environment is
# not clean and the test must fail with a clear, actionable message.
#
# NOTE:  A **separate** “post-work” test-suite will later verify that the
# same paths do exist and match the required permissions / contents.  This
# file is only concerned with the pristine starting point.

import os
import stat
import pytest

# Full paths that must NOT exist at the start of the assignment.
EXPECTED_FUTURE_PATHS = [
    "/home/user/network_lab",
    "/home/user/network_lab/configs",
    "/home/user/network_lab/configs/vlan10.conf",
    "/home/user/network_lab/configs/vlan20.conf",
    "/home/user/network_lab/scripts",
    "/home/user/network_lab/scripts/check_connectivity.sh",
    "/home/user/network_lab/logs",
    "/home/user/network_lab/logs/connectivity-report.log",
    "/home/user/network_lab/NETOPS_GROUP_PRESENT",
]

@pytest.mark.parametrize("path", EXPECTED_FUTURE_PATHS)
def test_path_absent_initially(path):
    """
    Ensure that none of the deliverable paths are present before the student
    begins working.  A pre-existing file or directory would indicate that the
    environment is not pristine and could invalidate the assessment.
    """
    assert not os.path.exists(path), (
        f"Unexpected pre-existing path detected:\n"
        f"    {path}\n"
        f"This path should NOT exist before the student performs the task. "
        f"Please start from a clean environment."
    )

def test_home_directory_exists_and_is_writable():
    """
    Sanity check: /home/user itself MUST exist and be writable for the student.
    This test is defensive—it verifies the baseline environment rather than the
    absence of deliverables; the assignment cannot proceed without it.
    """
    home = "/home/user"
    assert os.path.isdir(home), (
        "Baseline environment error: expected /home/user to exist as a "
        "directory, but it is missing."
    )

    # The user must have write permission to their home directory.  A simple
    # stat-based check is sufficient; we do not attempt an actual write.
    st_mode = os.stat(home).st_mode
    assert bool(st_mode & stat.S_IWUSR), (
        "/home/user exists but is not writable by the user.  The exercise "
        "requires write access to create the lab area."
    )