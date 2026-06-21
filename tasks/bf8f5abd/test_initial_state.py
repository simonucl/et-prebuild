# test_initial_state.py
"""
Pytest suite that validates the initial operating-system / filesystem
state before the student performs any action.

Requirements being verified (initial state):
1. Release directories for v1.2.0 and v1.2.1 must exist.
2. Each release directory must contain a build.txt file with exact
   expected contents.
3. Symlink /home/user/edge_app/current must exist and point to
   /home/user/edge_app/releases/v1.2.0.
4. Symlink /home/user/edge_app/previous must NOT exist yet.
5. Directory /home/user/deployment_logs must NOT exist yet.

If any of these assertions fail, the accompanying error message will
clearly indicate what is missing or incorrect.
"""

import os
import stat
import pytest

HOME = "/home/user"
EDGE_APP_DIR = os.path.join(HOME, "edge_app")
RELEASES_DIR = os.path.join(EDGE_APP_DIR, "releases")

V120_DIR = os.path.join(RELEASES_DIR, "v1.2.0")
V121_DIR = os.path.join(RELEASES_DIR, "v1.2.1")

CURRENT_LINK = os.path.join(EDGE_APP_DIR, "current")
PREVIOUS_LINK = os.path.join(EDGE_APP_DIR, "previous")

DEPLOYMENT_LOGS_DIR = os.path.join(HOME, "deployment_logs")
DEPLOYMENT_LOG_FILE = os.path.join(DEPLOYMENT_LOGS_DIR, "symlink_update.log")


@pytest.mark.parametrize(
    "path, description",
    [
        (V120_DIR, "release directory v1.2.0"),
        (V121_DIR, "release directory v1.2.1"),
    ],
)
def test_release_directories_exist(path, description):
    assert os.path.isdir(path), f"Expected {description} at {path} to exist."


@pytest.mark.parametrize(
    "dir_path, expected_content",
    [
        (V120_DIR, "v1.2.0 build completed\n"),
        (V121_DIR, "v1.2.1 build completed\n"),
    ],
)
def test_build_txt_contents(dir_path, expected_content):
    build_txt = os.path.join(dir_path, "build.txt")
    assert os.path.isfile(build_txt), f"Expected build.txt to exist in {dir_path}."
    with open(build_txt, "r", encoding="utf-8") as fh:
        contents = fh.read()
    assert (
        contents == expected_content
    ), f"Incorrect contents in {build_txt!r}. Expected {expected_content!r}."


def test_current_symlink_points_to_v120():
    assert os.path.islink(
        CURRENT_LINK
    ), f"Expected {CURRENT_LINK} to be a symbolic link."
    target = os.readlink(CURRENT_LINK)
    expected = V120_DIR
    assert (
        target == expected
    ), f"{CURRENT_LINK} should point to {expected}, but points to {target}."


def test_previous_symlink_does_not_exist():
    assert not os.path.lexists(
        PREVIOUS_LINK
    ), f"Symlink {PREVIOUS_LINK} should not exist yet."


def test_deployment_logs_directory_does_not_exist():
    assert not os.path.exists(
        DEPLOYMENT_LOGS_DIR
    ), f"Directory {DEPLOYMENT_LOGS_DIR} should not exist before deployment."
    # The log file must also be absent.
    assert not os.path.exists(
        DEPLOYMENT_LOG_FILE
    ), f"Log file {DEPLOYMENT_LOG_FILE} should not exist before deployment."