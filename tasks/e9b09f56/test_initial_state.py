# test_initial_state.py
#
# This pytest file validates the *initial* operating-system / filesystem
# state before the student begins the exercise.
#
# What we assert:
#   • The diagnostic artefact file that the student is asked to create
#     (/home/user/incidents/network_diagnostics.log) must **not** be present
#     yet.  The student’s job is to create it.
#   • If the parent directory (/home/user/incidents) does exist already,
#     that is fine; we merely make sure the required file is not lurking
#     inside it with the final expected content.
#
# Any failure message will clearly tell the learner what preliminary
# condition is violated.

import os
from pathlib import Path

ARTIFACT_PATH = Path("/home/user/incidents/network_diagnostics.log")
EXPECTED_CONTENT = (
    "PING_CHECK: PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.\n"
    "DNS_CHECK: 93.184.216.34, 2606:2800:220:1:248:1893:25c8:1946\n"
)

def test_network_diagnostics_log_absent_or_empty():
    """
    The artefact file must NOT exist yet.  If it does exist for any reason
    (e.g., leftover from a previous run), its content must not already be
    correct—otherwise the exercise would be moot.
    """
    if not ARTIFACT_PATH.exists():
        # Ideal, nothing to clean up.
        return

    # File exists: make sure it does NOT already contain the final answer.
    assert ARTIFACT_PATH.is_file(), (
        f"Expected {ARTIFACT_PATH} to be a regular file "
        "if it exists at all."
    )

    current = ARTIFACT_PATH.read_text(encoding="utf-8", errors="replace")
    assert current != EXPECTED_CONTENT, (
        f"The file {ARTIFACT_PATH} already contains the final expected "
        "content, but the learner has not yet performed the task. "
        "Please remove the file so the exercise starts from a clean slate."
    )