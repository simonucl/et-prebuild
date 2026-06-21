# test_initial_state.py
#
# This test-suite validates that the **input** area of the filesystem
# is exactly as expected *before* the student performs any action.
#
# • It checks that the three expected version folders exist under
#   /home/user/releases.
# • It checks that each folder contains the required `artifacts.txt`
#   and `release_notes.txt` files.
# • It verifies that the contents of those files match the reference
#   data given in the assignment statement.
#
# NOTE:
#   – No assertions are made about the (yet-to-be-generated) output
#     directory /home/user/deployment/summary or its files.
#   – Only stdlib + pytest are used.


import os
import pytest

ROOT = "/home/user/releases"

EXPECTED_VERSIONS = {
    "1.2.0": {
        "artifacts": [
            "app-1.2.0.jar",
            "lib-1.2.0.so",
            "docs-1.2.0.zip",
        ],
        "note": "Bug fixes and performance improvements.",
    },
    "1.3.0": {
        "artifacts": [
            "app-1.3.0.jar",
            "lib-1.3.0.so",
            "docs-1.3.0.zip",
            "cli-1.3.0.tar.gz",
        ],
        "note": "Added new CLI support and minor enhancements.",
    },
    "2.0.0-beta": {
        "artifacts": [
            "app-2.0.0-beta.jar",
            "lib-2.0.0-beta.so",
            "docs-2.0.0-beta.zip",
            "cli-2.0.0-beta.tar.gz",
            "migrator-2.0.0-beta.sh",
        ],
        "note": "Major release beta featuring new architecture overhaul.",
    },
}


def _artifact_path(version: str) -> str:
    return os.path.join(ROOT, version, "artifacts.txt")


def _notes_path(version: str) -> str:
    return os.path.join(ROOT, version, "release_notes.txt")


def test_release_root_exists():
    assert os.path.isdir(
        ROOT
    ), f"Expected release root directory {ROOT!r} to exist."


@pytest.mark.parametrize("version", EXPECTED_VERSIONS.keys())
def test_release_directory_exists(version):
    path = os.path.join(ROOT, version)
    assert os.path.isdir(
        path
    ), f"Expected release directory {path!r} to exist."


@pytest.mark.parametrize("version,data", EXPECTED_VERSIONS.items())
def test_artifacts_file_exists_and_contents(version, data):
    path = _artifact_path(version)
    assert os.path.isfile(
        path
    ), f"Missing artifacts file for version {version}: {path}"

    with open(path, "r", encoding="utf-8") as fh:
        # Strip only the *newline* from each line, preserve internal spacing.
        observed = [line.rstrip("\n") for line in fh]

    expected = data["artifacts"]

    assert (
        observed == expected
    ), (
        f"Contents of {path!r} do not match expected list.\n"
        f"Expected: {expected!r}\n"
        f"Observed: {observed!r}"
    )


@pytest.mark.parametrize("version,data", EXPECTED_VERSIONS.items())
def test_release_notes_file_exists_and_contents(version, data):
    path = _notes_path(version)
    assert os.path.isfile(
        path
    ), f"Missing release notes file for version {version}: {path}"

    with open(path, "r", encoding="utf-8") as fh:
        # Read the entire file, strip the trailing newline (if any)
        observed = fh.read().rstrip("\n")

    expected = data["note"]

    assert (
        observed == expected
    ), (
        f"Release notes in {path!r} do not match expected text.\n"
        f"Expected: {expected!r}\n"
        f"Observed: {observed!r}"
    )