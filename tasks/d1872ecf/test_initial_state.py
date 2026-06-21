# test_initial_state.py
#
# Pytest suite that validates the initial filesystem state *before*
# the student performs any actions required by the assignment.
#
# The checks purposely avoid looking for, or at, any artefacts that the
# student is expected to create (e.g. changelog.log, update_actions.log).
# Only the pre-existing files and their contents are verified.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
DEPLOYMENT = HOME / "deployment"
RELEASES = DEPLOYMENT / "releases"
CONFIG = DEPLOYMENT / "config" / "app.conf"

# Map of release version → expected (feature_count, fix_count)
EXPECTED_COUNTS = {
    "v1.0.0": (2, 1),
    "v1.1.0": (1, 0),
    "v1.2.0": (3, 2),
}


@pytest.mark.parametrize("version", EXPECTED_COUNTS.keys())
def test_release_directory_exists(version):
    """Each release directory must be present."""
    release_dir = RELEASES / version
    assert release_dir.is_dir(), (
        f"Expected release directory {release_dir} to exist, "
        "but it is missing."
    )


@pytest.mark.parametrize(
    "version,expected",
    [(v, EXPECTED_COUNTS[v]) for v in EXPECTED_COUNTS],
)
def test_notes_md_counts(version, expected):
    """
    NOTES.md for every release must exist and contain the expected number
    of FEATURE:/FIX: lines.
    """
    notes_path = RELEASES / version / "NOTES.md"
    assert notes_path.is_file(), (
        f"Expected NOTES.md at {notes_path} to exist, but it is missing."
    )

    feature_count = 0
    fix_count = 0

    with notes_path.open(encoding="utf-8") as fp:
        for line in fp:
            if line.startswith("FEATURE:"):
                feature_count += 1
            elif line.startswith("FIX:"):
                fix_count += 1

    exp_features, exp_fixes = expected
    assert feature_count == exp_features, (
        f"{notes_path} should contain {exp_features} lines starting with "
        f"'FEATURE:' but found {feature_count}."
    )
    assert fix_count == exp_fixes, (
        f"{notes_path} should contain {exp_fixes} lines starting with "
        f"'FIX:' but found {fix_count}."
    )


def test_app_conf_initial_state():
    """
    app.conf must exist with the expected pre-deployment contents:
    - It should include 'environment=staging'.
    - It must NOT yet contain any line beginning with 'version='.
    """
    assert CONFIG.is_file(), f"Configuration file {CONFIG} is missing."

    with CONFIG.open(encoding="utf-8") as fp:
        lines = fp.readlines()

    assert any(
        line.strip() == "environment=staging" for line in lines
    ), (
        f"{CONFIG} should contain the line 'environment=staging' "
        "but it is absent."
    )

    versions = [ln for ln in lines if ln.lstrip().startswith("version=")]
    assert not versions, (
        f"{CONFIG} should not contain a 'version=' entry yet, "
        f"but found: {versions!r}"
    )