# test_initial_state.py
#
# This pytest suite validates the *initial* state of the filesystem
# before the student carries out any actions.  It checks that the
# “current” dashboard is the *old* version, the “proposed” dashboard is
# the *new* version, and that neither the patch nor the verification log
# exists yet.

from pathlib import Path
import pytest

HOME = Path("/home/user")
CURRENT_JSON = HOME / "dashboards/current/k8s_nodes.json"
PROPOSED_JSON = HOME / "dashboards/proposed/k8s_nodes.json"
PATCH_FILE = HOME / "dashboards/patches/k8s_nodes.patch"
LOG_FILE = HOME / "dashboards/logs/patch_apply.log"


@pytest.fixture(scope="module")
def current_text():
    assert CURRENT_JSON.is_file(), (
        f"Expected the *current* dashboard file at {CURRENT_JSON} to exist "
        "before any action is taken."
    )
    return CURRENT_JSON.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def proposed_text():
    assert PROPOSED_JSON.is_file(), (
        f"Expected the *proposed* dashboard file at {PROPOSED_JSON} to exist "
        "before any action is taken."
    )
    return PROPOSED_JSON.read_text(encoding="utf-8")


def test_current_file_is_old_version(current_text):
    """
    The current file must be the *old* version:
      • It must *not* contain the new 'Disk usage' panel
      • It must refresh every 5 seconds
    """
    assert '"Disk usage"' not in current_text, (
        "The current dashboard already contains 'Disk usage'; it should be "
        "the *old* version before the student patches it."
    )
    assert '"refresh": "5s"' in current_text, (
        "The current dashboard should refresh every 5 seconds before being "
        "updated."
    )


def test_proposed_file_is_new_version(proposed_text):
    """
    The proposed file must be the *new* version:
      • It must contain the new 'Disk usage' panel
      • It must refresh every 10 seconds
      • It must be exactly 21 lines long
    """
    lines = proposed_text.splitlines()
    assert len(lines) == 21, (
        f"The proposed dashboard should be exactly 21 lines long, "
        f"found {len(lines)}."
    )
    assert '"Disk usage"' in proposed_text, (
        "The proposed dashboard should contain the new 'Disk usage' panel."
    )
    assert '"refresh": "10s"' in proposed_text, (
        "The proposed dashboard should refresh every 10 seconds."
    )


def test_current_and_proposed_files_differ(current_text, proposed_text):
    """
    Before the student acts, the current and proposed files must differ.
    """
    assert current_text != proposed_text, (
        "The current and proposed dashboard files are already identical; "
        "the patch would have nothing to do."
    )


def test_patch_and_log_do_not_exist_yet():
    """
    Neither the patch file nor the verification log should exist yet.
    """
    assert not PATCH_FILE.exists(), (
        f"Patch file {PATCH_FILE} should not exist before the student "
        "creates it."
    )
    assert not LOG_FILE.exists(), (
        f"Log file {LOG_FILE} should not exist before the student "
        "applies the patch."
    )