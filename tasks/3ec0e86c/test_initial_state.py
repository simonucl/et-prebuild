# test_initial_state.py
"""
Pytest test-suite that validates the *initial* operating-system / filesystem
state before the student performs any actions.

It asserts the following:

1.  /home/user/config_repository
        • exists and is a directory (0755, owned by current UID)
        • contains *exactly* the three regular files listed in the task:
              app_alpha.conf
              app_alpha_v2.conf
              app_beta.conf
        • each file is mode 0644, owned by current UID and has the expected
          minimal contents.

2.  /home/user/live_configs  MUST NOT yet exist (neither file nor directory).

3.  /home/user/config_change.log  MUST NOT yet exist.

The tests purposefully do *not* make any assertions on the desired *final*
state (links, log contents, …); they focus solely on the pre-task conditions.
"""

import os
import stat
import pwd
import pytest

HOME = "/home/user"
CONFIG_REPO = os.path.join(HOME, "config_repository")
LIVE_DIR = os.path.join(HOME, "live_configs")
CHANGE_LOG = os.path.join(HOME, "config_change.log")

EXPECTED_FILES = {
    "app_alpha.conf": (
        "version=1.0",
        "name=alpha",
    ),
    "app_alpha_v2.conf": (
        "version=2.0",
        "name=alpha",
    ),
    "app_beta.conf": (
        "version=1.0",
        "name=beta",
    ),
}


def _octal_mode(path):
    """Return the file mode in octal notation, e.g. 0o755, 0o644."""
    return stat.S_IMODE(os.lstat(path).st_mode)


def _owner_uid(path):
    return os.lstat(path).st_uid


def _current_uid():
    return os.getuid()


@pytest.fixture(scope="session")
def repo_contents():
    """Return a mapping of filename -> full path for all entries in CONFIG_REPO."""
    if not os.path.exists(CONFIG_REPO):
        pytest.fail(f"Required directory {CONFIG_REPO!r} is missing.")
    if not os.path.isdir(CONFIG_REPO):
        pytest.fail(f"{CONFIG_REPO!r} exists but is not a directory.")

    entries = os.listdir(CONFIG_REPO)
    return {name: os.path.join(CONFIG_REPO, name) for name in entries}


def test_config_repository_directory_properties():
    assert os.path.isdir(
        CONFIG_REPO
    ), f"{CONFIG_REPO} must be a directory, but is not."

    mode = _octal_mode(CONFIG_REPO)
    assert (
        mode == 0o755
    ), f"{CONFIG_REPO} should have permissions 0755, found {oct(mode)}."

    uid = _owner_uid(CONFIG_REPO)
    assert (
        uid == _current_uid()
    ), f"{CONFIG_REPO} should be owned by the current user (uid {_current_uid()}), found uid {uid}."


def test_config_repository_contains_exact_files(repo_contents):
    expected_set = set(EXPECTED_FILES.keys())
    actual_set = set(repo_contents.keys())

    missing = expected_set - actual_set
    extra = actual_set - expected_set

    assert not missing, (
        f"{CONFIG_REPO} is missing the following expected file(s): "
        + ", ".join(sorted(missing))
    )
    assert not extra, (
        f"{CONFIG_REPO} contains unexpected file(s): " + ", ".join(sorted(extra))
    )


@pytest.mark.parametrize("filename,expected_lines", EXPECTED_FILES.items())
def test_individual_file_properties_and_contents(filename, expected_lines, repo_contents):
    path = repo_contents.get(filename)
    assert path, f"{filename} not found in {CONFIG_REPO}"

    # Must be a regular file, not symlink.
    assert os.path.isfile(
        path
    ) and not os.path.islink(
        path
    ), f"{path} should be a regular file, not a symlink."

    mode = _octal_mode(path)
    assert (
        mode == 0o644
    ), f"{path} should have permissions 0644, found {oct(mode)}."

    uid = _owner_uid(path)
    assert (
        uid == _current_uid()
    ), f"{path} should be owned by current user (uid {_current_uid()}), found uid {uid}."

    # Check that file contains the expected lines (order-agnostic set inclusion).
    with open(path, "r", encoding="utf-8") as fh:
        content = fh.read().splitlines()

    for line in expected_lines:
        assert (
            line in content
        ), f"{path} is expected to contain line {line!r} but it was not found."


def test_live_configs_does_not_exist_yet():
    assert not os.path.exists(
        LIVE_DIR
    ), f"{LIVE_DIR} should NOT exist before the task starts."


def test_change_log_does_not_exist_yet():
    assert not os.path.exists(
        CHANGE_LOG
    ), f"{CHANGE_LOG} should NOT exist before the task starts."