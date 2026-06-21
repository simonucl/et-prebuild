# test_initial_state.py
#
# Pytest suite that validates the expected *initial* filesystem state
# before the student performs any actions.
#
# NOTE:  Per the grading rubric we explicitly DO NOT check for any of the
#        "output" artefacts that the student is expected to create
#        (e.g. bump_audit.txt or a bumped version string of 2.5.4).
#
# Allowed imports: stdlib + pytest only.

import json
from pathlib import Path
import pytest

HOME = Path("/home/user")
WEBSVC_DIR = HOME / "websvc"
PACKAGE_JSON = WEBSVC_DIR / "package.json"
CHANGELOG_MD = WEBSVC_DIR / "CHANGELOG.md"
INCIDENT_FILE = WEBSVC_DIR / "incidents" / "2024-05-17_cpu_spike.txt"

@pytest.fixture(scope="module")
def package_json_data():
    """
    Load and return the parsed JSON data from package.json.
    If the file is missing or invalid JSON, the test will fail
    with a clear message.
    """
    assert PACKAGE_JSON.exists(), (
        f"Expected package.json at {PACKAGE_JSON} but it does not exist."
    )
    assert PACKAGE_JSON.is_file(), (
        f"Expected {PACKAGE_JSON} to be a regular file."
    )
    try:
        return json.loads(PACKAGE_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        pytest.fail(f"package.json is not valid JSON: {exc}")  # pragma: no cover


def test_websvc_directory_exists():
    assert WEBSVC_DIR.exists(), f"Directory {WEBSVC_DIR} does not exist."
    assert WEBSVC_DIR.is_dir(), f"{WEBSVC_DIR} exists but is not a directory."


def test_package_json_version_is_2_5_3(package_json_data):
    assert "version" in package_json_data, (
        '"version" key is missing from package.json.'
    )
    assert (
        package_json_data["version"] == "2.5.3"
    ), (
        'package.json "version" must be "2.5.3" before the bump; '
        f'found "{package_json_data["version"]}".'
    )
    # Sanity-check that the new version string does NOT yet appear.
    assert "2.5.4" not in PACKAGE_JSON.read_text(encoding="utf-8"), (
        'package.json already appears to contain "2.5.4"; '
        "this should only be present after the student performs the bump."
    )


def test_changelog_initial_state():
    assert CHANGELOG_MD.exists(), f"CHANGELOG.md not found at {CHANGELOG_MD}."
    assert CHANGELOG_MD.is_file(), f"{CHANGELOG_MD} exists but is not a file."

    lines = [ln.rstrip("\n") for ln in CHANGELOG_MD.read_text(encoding="utf-8").splitlines()]
    # Strip any leading blank lines/comments to find the first meaningful line.
    first_nonblank = next((ln for ln in lines if ln.strip()), "")
    expected_first_line = "## [2.5.3] - 2024-04-07"
    assert (
        first_nonblank == expected_first_line
    ), (
        "The first entry in CHANGELOG.md should reference version 2.5.3 "
        f"but found: '{first_nonblank}'."
    )
    # Ensure the yet-to-be-added 2.5.4 heading is absent.
    assert not any("## [2.5.4]" in ln for ln in lines), (
        "CHANGELOG.md already contains an entry for 2.5.4; "
        "this should be added only after the student performs the task."
    )


def test_incident_file_exists():
    assert INCIDENT_FILE.exists(), (
        f"Incident report expected at {INCIDENT_FILE} but was not found."
    )
    assert INCIDENT_FILE.is_file(), (
        f"{INCIDENT_FILE} exists but is not a regular file."
    )