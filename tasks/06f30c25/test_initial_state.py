# test_initial_state.py
#
# This pytest suite verifies that the initial operating-system / filesystem
# state is exactly as expected *before* the student begins work on the
# “cluster audit” task.  It checks only the prescribed input files and
# directories and deliberately ignores the output artefacts that the student
# will create later.

import pathlib
import pytest

# Base paths
HOME = pathlib.Path("/home/user")
CLUSTER_ROOT = HOME / "cluster" / "nodes"

# Expected user lists for each node.
EXPECTED_USERS = {
    "node1": ["alice", "bob", "charlie", "dave"],
    "node2": ["alice", "charlie", "eve", "frank"],
    "node3": ["alice", "bob", "charlie", "frank"],
}


@pytest.mark.parametrize("node,users", EXPECTED_USERS.items())
def test_users_file_exists_and_contents_are_correct(node: str, users: list[str]) -> None:
    """
    Ensure that each node's users.txt exists at the correct absolute path
    and contains exactly the expected usernames, one per line, in the order
    specified by the specification.
    """
    users_file = CLUSTER_ROOT / node / "users.txt"

    # 1. File existence and type -------------------------------------------------
    assert users_file.exists(), (
        f"Expected file not found: {users_file}. "
        "The cluster input files must be present before the audit starts."
    )
    assert users_file.is_file(), (
        f"Expected a regular file at {users_file}, "
        "but found something else (e.g., directory, symlink, etc.)."
    )

    # 2. File contents -----------------------------------------------------------
    actual_lines = users_file.read_text(encoding="utf-8").splitlines()

    # Helpful error messages
    if actual_lines != users:
        missing = [u for u in users if u not in actual_lines]
        extras = [u for u in actual_lines if u not in users]
        message_lines = [
            f"Contents mismatch in {users_file}:",
            f"  Expected: {users}",
            f"  Actual  : {actual_lines}",
        ]
        if missing:
            message_lines.append(f"  Missing expected usernames: {missing}")
        if extras:
            message_lines.append(f"  Unexpected extra usernames: {extras}")
        pytest.fail("\n".join(message_lines))

    # 3. No blank lines or trailing whitespace -----------------------------------
    with users_file.open("rb") as fh:
        raw = fh.read()
    assert b"\r\n" not in raw, (
        f"{users_file} should use UNIX line endings (LF) only, "
        "but CRLF sequences were detected."
    )
    assert raw.endswith(b"\n"), (
        f"{users_file} must end with a single newline character (LF)."
    )