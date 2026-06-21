# test_initial_state.py
"""
Pytest suite that validates the starting filesystem state *before* the student
creates any firewall-related artefacts.

None of the following must exist yet:

1. /home/user/firewall_configs                  (directory)
2. /home/user/firewall_configs/repo_fw_rules.v4 (file)
3. /home/user/firewall_configs/apply_repo_fw.sh (file)
4. /home/user/firewall_change.log               (file)

If any of these paths already exist, the initial state is incorrect and the
tests must fail with a clear, actionable message.
"""

from pathlib import Path
import pytest

# Absolute paths that must be absent before the student begins work
FIREWALL_DIR = Path("/home/user/firewall_configs")
RULES_FILE = FIREWALL_DIR / "repo_fw_rules.v4"
HELPER_SCRIPT = FIREWALL_DIR / "apply_repo_fw.sh"
OP_LOG = Path("/home/user/firewall_change.log")

ALL_PATHS = [
    FIREWALL_DIR,
    RULES_FILE,
    HELPER_SCRIPT,
    OP_LOG,
]

@pytest.mark.parametrize("path_obj", ALL_PATHS)
def test_path_must_not_exist(path_obj: Path):
    """
    Ensure none of the firewall artefact paths exist prior to task execution.
    This prevents accidental residue from previous runs or manual meddling.
    """
    assert not path_obj.exists(), (
        f"Precondition failed: {path_obj} already exists but should not. "
        "Start with a clean slate."
    )