# test_initial_state.py
#
# This pytest file validates the **initial** exercise environment.
# It ONLY checks the pre-existing filesystem contents and never looks
# for the artefacts that the student must create later.
#
# Rules respected:
#   • Uses only stdlib + pytest
#   • Verifies full, absolute paths
#   • Gives clear failure messages
#   • Does NOT test for any of the required output files / directories
#     (e.g. /home/user/report or the CSV file)

import os
import pathlib
import re

MANIFEST_DIR = pathlib.Path("/home/user/manifests").resolve()

# Full, absolute paths of the manifests that must already exist
EXPECTED_MANIFEST_FILES = [
    MANIFEST_DIR / "deployment-frontend.yaml",
    MANIFEST_DIR / "deployment-backend.yaml",
    MANIFEST_DIR / "service-frontend.yaml",
    MANIFEST_DIR / "service-backend.yaml",
    MANIFEST_DIR / "configmap-app.yaml",
]


def read_file(p: pathlib.Path) -> str:
    """Helper that returns the file content as text (utf-8)."""
    with p.open("r", encoding="utf-8") as f:
        return f.read()


def test_manifest_directory_exists():
    assert MANIFEST_DIR.is_dir(), (
        f"Expected directory {MANIFEST_DIR} to exist, "
        "but it is missing or not a directory."
    )


def test_expected_manifest_files_exist():
    missing = [str(p) for p in EXPECTED_MANIFEST_FILES if not p.is_file()]
    assert not missing, (
        "The following required manifest files are missing:\n  - " +
        "\n  - ".join(missing)
    )


def _assert_yaml_value(pattern: str, text: str, file_path: pathlib.Path):
    """
    Assert that a regex pattern exists in the yaml text.

    Parameters
    ----------
    pattern : str
        Regular expression to search for.
    text : str
        File contents.
    file_path : pathlib.Path
        For error reporting.
    """
    if not re.search(pattern, text, flags=re.MULTILINE):
        pytest.fail(
            f"File {file_path} is expected to contain a line matching:\n"
            f"    {pattern!r}\n"
            "but it was not found."
        )


def test_deployment_yaml_basic_structure():
    """
    Make sure the two deployment YAMLs declare kind: Deployment and have
    the four key pieces of data that the student will later have to extract.
    """
    deployments = [
        MANIFEST_DIR / "deployment-frontend.yaml",
        MANIFEST_DIR / "deployment-backend.yaml",
    ]

    for p in deployments:
        text = read_file(p)

        # Basic checks to confirm the YAML has what the later shell
        # pipeline will need.
        _assert_yaml_value(r"^kind:\s*Deployment\b", text, p)
        _assert_yaml_value(r"^metadata:\s*", text, p)
        _assert_yaml_value(r"^\s*name:\s*\w+", text, p)
        _assert_yaml_value(r"^\s*namespace:\s*\w+", text, p)
        _assert_yaml_value(r"^spec:\s*", text, p)
        _assert_yaml_value(r"^\s*replicas:\s*\d+", text, p)
        _assert_yaml_value(r"^\s*containers:\s*", text, p)
        _assert_yaml_value(r"^\s*image:\s*[\w./:-]+", text, p)


def test_only_expected_files_in_manifest_directory():
    """
    Sanity-check that there are no unexpected subdirectories or files that
    could interfere with a simple shell pipeline.
    """
    present_files = sorted(MANIFEST_DIR.iterdir())
    unexpected = [
        str(p) for p in present_files
        if p.is_file() and p not in EXPECTED_MANIFEST_FILES
    ]
    assert not unexpected, (
        "Unexpected files found in /home/user/manifests that are not part of "
        "the baseline exercise:\n  - " + "\n  - ".join(unexpected)
    )