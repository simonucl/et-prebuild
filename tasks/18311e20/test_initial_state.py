# test_initial_state.py
#
# This test-suite verifies that the environment is **clean**
# before the student starts working on the assignment.
#
# It passes when *either* the target files do not exist at all,
# or they exist but **do not** yet match the exact, final
# specification.  If the files are already perfect, the test
# fails, signalling that the sandbox was not properly reset.

import os
from pathlib import Path

import pytest

CI_DIR = Path("/home/user/ci")
SCRIPT_PATH = CI_DIR / "firewall_rules.sh"
LOG_PATH = CI_DIR / "firewall_rules.log"

EXPECTED_SCRIPT_CONTENT = (
    "#!/bin/bash\n\n"
    "iptables -A INPUT -p tcp --dport 22 -j ACCEPT\n"
    "iptables -A INPUT -p tcp --dport 8080 -j ACCEPT\n"
    "iptables -A INPUT -p tcp --dport 443 -j ACCEPT\n"
    "iptables -A INPUT -j DROP\n"
)

EXPECTED_LOG_CONTENT = (
    "[RULE] iptables -A INPUT -p tcp --dport 22 -j ACCEPT\n"
    "[RULE] iptables -A INPUT -p tcp --dport 8080 -j ACCEPT\n"
    "[RULE] iptables -A INPUT -p tcp --dport 443 -j ACCEPT\n"
    "[RULE] iptables -A INPUT -j DROP\n"
)


def _file_matches(path: Path, expected: str) -> bool:
    """
    Return True if `path` exists, is a regular file, and its byte-for-byte
    content matches `expected`.
    """
    try:
        data = path.read_text(encoding="utf-8")
    except (FileNotFoundError, IsADirectoryError):
        return False
    return data == expected


@pytest.mark.parametrize(
    "file_path, expected_content",
    [
        (SCRIPT_PATH, EXPECTED_SCRIPT_CONTENT),
        (LOG_PATH, EXPECTED_LOG_CONTENT),
    ],
)
def test_files_not_already_in_final_state(file_path: Path, expected_content: str):
    """
    The firewall script and log file should *not* already be present
    with their final, correct contents before the student starts.

    The test passes if:
      • the file does not exist, OR
      • the file exists but its content differs from the required final content.

    The test fails (environment is dirty) if:
      • the file exists AND its content is already perfect.
    """
    assert not _file_matches(
        file_path, expected_content
    ), (
        f"Pre-existing file detected: {file_path}\n"
        "It already contains exactly the expected final content. "
        "Please reset the environment so the student can carry out the task."
    )