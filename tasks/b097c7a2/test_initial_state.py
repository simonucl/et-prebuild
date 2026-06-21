# test_initial_state.py
#
# This test-suite validates that the workstation is in the **expected
# initial state _before_ the student performs any actions**.  It checks:
#   • presence and contents of artefact files
#   • presence and correctness of the release CSV
#   • absence (so far) of the deployment directory
#
# Only stdlib + pytest are used.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")

ARTIFACTS_DIR = HOME / "artifacts"
RELEASES_DIR = HOME / "releases"
DEPLOYMENTS_DIR = HOME / "deployments"
TODAY = "2023-10-15"
DEPLOYMENT_TARGET_DIR = DEPLOYMENTS_DIR / TODAY
RELEASE_CSV = RELEASES_DIR / f"release_{TODAY}.csv"

# --------------------------------------------------------------------------- #
# Helper data derived from the task description
# --------------------------------------------------------------------------- #
ARTIFACT_META = {
    "app1": {
        "version": "1.2.3",
        "filename": "app1_v1.2.3.tar.gz",
        "size": 37,
        "content": b"DUMMY CONTENT FOR app1 version 1.2.3\n",
    },
    "app2": {
        "version": "0.9.8",
        "filename": "app2_v0.9.8.tar.gz",
        "size": 37,
        "content": b"DUMMY CONTENT FOR app2 version 0.9.8\n",
    },
    "app3": {
        "version": "3.4.5",
        "filename": "app3_v3.4.5.tar.gz",
        "size": 37,
        "content": b"DUMMY CONTENT FOR app3 version 3.4.5\n",
    },
}

EXPECTED_CSV_LINES = [
    "app,version,artifact_file\n",
    f"app1,1.2.3,{ARTIFACTS_DIR / ARTIFACT_META['app1']['filename']}\n",
    f"app2,0.9.8,{ARTIFACTS_DIR / ARTIFACT_META['app2']['filename']}\n",
]


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_artifacts_directory_exists_and_is_correct():
    assert ARTIFACTS_DIR.is_dir(), (
        f"Missing artifacts directory: {ARTIFACTS_DIR}. "
        "It should exist and contain the prepared artefacts."
    )

    # Collect actual .tar.gz files (ignore any other potential files)
    actual_files = {p.name for p in ARTIFACTS_DIR.glob("*.tar.gz")}

    expected_files = {meta["filename"] for meta in ARTIFACT_META.values()}
    assert expected_files.issubset(actual_files), (
        "The artifacts directory is missing expected files.\n"
        f"Expected at least: {sorted(expected_files)}\n"
        f"Found:            {sorted(actual_files)}"
    )

    # Check each artefact's size and contents
    for app, meta in ARTIFACT_META.items():
        file_path = ARTIFACTS_DIR / meta["filename"]
        data = file_path.read_bytes()
        assert len(data) == meta["size"], (
            f"{file_path} has unexpected size. "
            f"Expected {meta['size']} bytes, found {len(data)} bytes."
        )
        assert data == meta["content"], (
            f"{file_path} contents differ from the expected dummy payload."
        )


def test_release_csv_exists_and_is_correct():
    assert RELEASE_CSV.is_file(), (
        f"Release CSV {RELEASE_CSV} is missing. "
        "It must be present before any deployment actions are executed."
    )

    with RELEASE_CSV.open("r", newline="") as fh:
        lines = fh.readlines()

    assert lines == EXPECTED_CSV_LINES, (
        "release_2023-10-15.csv does not contain the expected lines.\n"
        "Expected:\n"
        + "".join(EXPECTED_CSV_LINES)
        + "\nFound:\n"
        + "".join(lines)
    )


def test_deployment_directory_not_yet_created():
    assert not DEPLOYMENT_TARGET_DIR.exists(), (
        f"The deployment directory {DEPLOYMENT_TARGET_DIR} already exists. "
        "It should **not** exist before the student runs their commands."
    )