# test_initial_state.py
#
# This pytest suite validates the *initial* state of the workspace **before**
# the student has performed any action.  It asserts that:
#
# 1. Both existing configuration files are present at the expected absolute
#    paths and still contain their original content (no “staging” additions
#    yet).
# 2. The audit log **must not** exist at this point.
#
# If any of these assertions fail, the accompanying error message pinpoints
# exactly what is missing or unexpectedly present.
#
# NOTE: These tests purposefully check that the “staging” blocks and the audit
#       log are **absent**, because they are expected to be created/added by
#       the student in a later task.

import pathlib
import textwrap
import pytest

HOME = pathlib.Path("/home/user")
RELEASES_DIR = HOME / "releases"

# Absolute paths to the artefacts involved in the assignment
DEPLOYMENT_YAML = RELEASES_DIR / "apps" / "service_a" / "deployment.yaml"
RELEASE_TOML = RELEASES_DIR / "apps" / "service_b" / "release.toml"
AUDIT_LOG = RELEASES_DIR / "edit_audit.log"


@pytest.fixture(scope="module")
def deployment_content():
    """Return the text content of deployment.yaml as a single string."""
    try:
        return DEPLOYMENT_YAML.read_text(encoding="utf-8")
    except FileNotFoundError:
        pytest.fail(f"Expected file not found: {DEPLOYMENT_YAML}")


@pytest.fixture(scope="module")
def release_toml_content():
    """Return the text content of release.toml as a single string."""
    try:
        return RELEASE_TOML.read_text(encoding="utf-8")
    except FileNotFoundError:
        pytest.fail(f"Expected file not found: {RELEASE_TOML}")


def test_deployment_yaml_exists_and_has_original_content(deployment_content):
    """
    The original deployment.yaml must exist and *must not* yet contain the
    'environments:' block for staging.
    """
    # Basic sanity checks for original content
    required_snippets = [
        "apiVersion: apps/v1",
        "kind: Deployment",
        "metadata:",
        "name: service-a",
        "replicas: 3",
        "image: registry.example.com/service-a:1.4.2",
    ]
    for snippet in required_snippets:
        assert snippet in deployment_content, (
            f"deployment.yaml is missing expected original line: '{snippet}'"
        )

    # Ensure the staging environment has NOT been appended yet
    unexpected_staging_block = textwrap.dedent(
        """
        environments:
          staging:
            replicas: 1
        """
    ).strip()
    assert "environments:" not in deployment_content, (
        "deployment.yaml already contains an 'environments:' block—"
        "the staging block should not exist before the student edits the file."
    )
    assert "registry.example.com/service-a:1.5.0-rc" not in deployment_content, (
        "deployment.yaml already contains the staging image tag—"
        "this should only be added by the student."
    )


def test_release_toml_exists_and_has_original_content(release_toml_content):
    """
    The original release.toml must exist and *must not* yet contain the
    '[release.staging]' table.
    """
    # Basic sanity checks for original content
    required_snippets = [
        "[package]",
        'name = "service_b"',
        'version = "2.0.0"',
        "[dependencies]",
        'logger = "1.0"',
        'database = "3.2"',
    ]
    for snippet in required_snippets:
        assert snippet in release_toml_content, (
            f"release.toml is missing expected original line: '{snippet}'"
        )

    # Ensure the staging table has NOT been appended yet
    assert "[release.staging]" not in release_toml_content, (
        "release.toml already contains a '[release.staging]' table—"
        "this should only be added by the student."
    )
    assert 'version = "2.1.0-rc"' not in release_toml_content, (
        "release.toml already contains the staging version—"
        "this should only be added by the student."
    )


def test_audit_log_does_not_exist_yet():
    """
    The audit log should **not** exist before the student makes any edits.
    """
    assert not AUDIT_LOG.exists(), (
        f"Unexpected audit log found at {AUDIT_LOG}. "
        "The file should be created only after the student performs the edits."
    )