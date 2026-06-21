# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the OS / filesystem
# before the student performs any action for the “update the symlink” task.
#
# The ground-truth “initial state” that must already exist:
#   /home/user/k8s/manifests/
#   ├── deployment-v1.yaml  (regular file, content: "version: v1\n")
#   ├── deployment-v2.yaml  (regular file, content: "version: v2\n")
#   ├── service.yaml        (regular file, content irrelevant)
#   └── current             (symbolic link → deployment-v1.yaml)
#
# If any of these pre-conditions are missing or incorrect, the tests will fail
# with a clear, actionable message.

import os
import stat
from pathlib import Path

MANIFEST_DIR = Path("/home/user/k8s/manifests")
V1_FILE = MANIFEST_DIR / "deployment-v1.yaml"
V2_FILE = MANIFEST_DIR / "deployment-v2.yaml"
SERVICE_FILE = MANIFEST_DIR / "service.yaml"
CURRENT_LINK = MANIFEST_DIR / "current"

# ---------------------------------------------------------------------------


def _assert_regular_file(path: Path, expected_content: str | None = None) -> None:
    """Helper: assert that `path` is a regular file (not a symlink) and,
    optionally, that its exact content matches `expected_content`.
    """
    assert path.exists(), f"Expected regular file {path} to exist."
    # It must be a *regular* file, not a symlink.
    st = path.lstat()
    assert stat.S_ISREG(st.st_mode), f"{path} exists but is not a regular file."
    if expected_content is not None:
        data = path.read_text(encoding="utf-8")
        assert (
            data == expected_content
        ), f"{path} content mismatch:\n  expected: {expected_content!r}\n  actual:   {data!r}"


# ---------------------------------------------------------------------------


def test_manifest_directory_exists_and_permissions():
    """Directory /home/user/k8s/manifests/ must exist with mode 755 (rwxr-xr-x)."""
    assert MANIFEST_DIR.exists(), f"Directory {MANIFEST_DIR} does not exist."
    assert MANIFEST_DIR.is_dir(), f"{MANIFEST_DIR} exists but is not a directory."
    mode = MANIFEST_DIR.stat().st_mode & 0o777
    expected_mode = 0o755
    assert (
        mode == expected_mode
    ), f"{MANIFEST_DIR} permissions are {oct(mode)}, expected {oct(expected_mode)}."


def test_required_regular_files_exist_with_correct_content():
    """Verify deployment files are present, regular, and contain the expected content."""
    _assert_regular_file(V1_FILE, expected_content="version: v1\n")
    _assert_regular_file(V2_FILE, expected_content="version: v2\n")
    _assert_regular_file(SERVICE_FILE)  # content is not validated for service.yaml


def test_current_is_symlink_pointing_to_v1():
    """The symbolic link 'current' must resolve to deployment-v1.yaml (initial state)."""
    assert CURRENT_LINK.exists(), f"Symbolic link {CURRENT_LINK} does not exist."
    assert CURRENT_LINK.is_symlink(), f"{CURRENT_LINK} exists but is not a symlink."

    # Resolve symlink to an absolute, real path (follows any intermediate links).
    resolved = Path(os.path.realpath(CURRENT_LINK))
    expected = V1_FILE
    assert (
        resolved == expected
    ), f"'current' symlink resolves to {resolved}, expected {expected}."


def test_no_extra_files_inside_manifest_directory():
    """Ensure that no unexpected files are present in /home/user/k8s/manifests/."""
    # Allowed entries (basenames)
    allowed = {"deployment-v1.yaml", "deployment-v2.yaml", "service.yaml", "current"}
    actual = {p.name for p in MANIFEST_DIR.iterdir()}

    extras = actual - allowed
    missing = allowed - actual

    assert (
        not missing
    ), f"Missing expected entries in {MANIFEST_DIR}: {', '.join(sorted(missing))}"
    assert (
        not extras
    ), f"Unexpected extra entries in {MANIFEST_DIR}: {', '.join(sorted(extras))}"