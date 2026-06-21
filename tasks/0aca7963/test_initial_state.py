# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system / filesystem
# conditions for the “network flow column-manipulation” exercise.
#
# It confirms that:
#   • The working directory and the source data file exist.
#   • Exactly four correctly-formatted TAB-separated rows are present.
#   • No derived output artefacts are present yet.
#
# Only stdlib + pytest are used.

from pathlib import Path
import pytest

FLOW_DIR = Path("/home/user/projects/flowdata")
FLOW_FILE = FLOW_DIR / "flows.log"

# Expected absolute paths for artefacts that must *not* exist initially.
ARTEFACTS = [
    FLOW_DIR / "host_ports.csv",
    FLOW_DIR / "protocol_bytes.tsv",
    FLOW_DIR / "combined.tsv",
]

# Ground-truth content of flows.log (⇥ represents a literal TAB).
EXPECTED_LINES = [
    "2023-05-01T10:00:01Z\t192.168.1.10\tTCP\t10.0.0.5\t443\t1024",
    "2023-05-01T10:00:02Z\t192.168.1.11\tUDP\t10.0.0.6\t53\t512",
    "2023-05-01T10:00:03Z\t192.168.1.12\tTCP\t10.0.0.7\t22\t2048",
    "2023-05-01T10:00:04Z\t192.168.1.13\tUDP\t10.0.0.8\t161\t256",
]

def _read_flow_lines():
    """
    Helper that returns flows.log content stripped of its trailing newlines.
    The function fails early with a descriptive assertion if the file is missing.
    """
    assert FLOW_FILE.is_file(), (
        f"Required source file not found: {FLOW_FILE}. "
        "The assignment must begin with this file in place."
    )
    with FLOW_FILE.open("r", encoding="utf-8") as fh:
        # keepends=False => lines without trailing newline characters
        return fh.read().splitlines()

def test_flow_directory_exists():
    assert FLOW_DIR.is_dir(), (
        f"Directory {FLOW_DIR} does not exist. "
        "The initial project tree is missing."
    )

def test_flows_log_content_and_format():
    lines = _read_flow_lines()

    # 1) Exactly four non-empty lines.
    assert len(lines) == 4, (
        f"flows.log should contain exactly 4 data rows; found {len(lines)}."
    )
    assert all(lines), "flows.log contains blank lines, which is not allowed."

    # 2) Verify each line has six TAB-separated columns.
    for idx, raw in enumerate(lines, 1):
        cols = raw.split("\t")
        assert len(cols) == 6, (
            f"Line {idx} in flows.log has {len(cols)} columns; "
            "expected 6 TAB-separated fields."
        )

    # 3) Ensure the entire content matches the provided truth exactly.
    assert lines == EXPECTED_LINES, (
        "flows.log does not match the expected ground-truth content.\n"
        "If the file was modified, restore it to the original state shown "
        "in the assignment description."
    )

@pytest.mark.parametrize("path", ARTEFACTS)
def test_output_artefacts_do_not_yet_exist(path):
    assert not path.exists(), (
        f"Output artefact {path} is present before the exercise begins. "
        "The student must create this file *during* the task, not beforehand."
    )