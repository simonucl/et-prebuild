# test_initial_state.py
#
# This pytest suite verifies the *initial* filesystem state that must be
# present **before** the student performs the patch-level version bump
# (1.2.3 → 1.2.4).  If any of these tests fail, the workspace does not
# match the expected starting conditions.

from pathlib import Path
import textwrap
import pytest


HOME = Path("/home/user")
DEPLOYMENT_YAML = HOME / "manifests" / "deployment.yaml"
CHANGELOG_MD = HOME / "CHANGELOG.md"
LOG_FILE = HOME / "version_bump.log"


@pytest.fixture(scope="module")
def deployment_contents():
    """Return the raw text contents of deployment.yaml."""
    if not DEPLOYMENT_YAML.exists():
        pytest.fail(
            f"Expected {DEPLOYMENT_YAML} to exist, but it does not.",
            pytrace=False,
        )
    return DEPLOYMENT_YAML.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def changelog_contents():
    """Return the raw text contents of CHANGELOG.md."""
    if not CHANGELOG_MD.exists():
        pytest.fail(
            f"Expected {CHANGELOG_MD} to exist, but it does not.",
            pytrace=False,
        )
    return CHANGELOG_MD.read_text(encoding="utf-8")


def test_manifests_directory_exists():
    manifests_dir = HOME / "manifests"
    assert manifests_dir.is_dir(), (
        f"Directory {manifests_dir} must exist before the version bump."
    )


def test_deployment_yaml_exact_contents(deployment_contents):
    """
    deployment.yaml must contain the exact initial definition with the
    1.2.3 tag and must *not* yet reference 1.2.4.
    """
    # Expected text exactly as provided in the task description
    expected = textwrap.dedent(
        """\
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: example-operator
        spec:
          replicas: 1
          template:
            spec:
              containers:
              - name: operator
                image: ghcr.io/org/example-operator:1.2.3
        """
    )
    # We allow for (optional) trailing newline(s) at EOF.
    assert deployment_contents.rstrip("\n") == expected.rstrip(
        "\n"
    ), (
        f"{DEPLOYMENT_YAML} contents differ from the expected initial "
        f"state.  The file must exactly match the 1.2.3 version shown in "
        f"the task description."
    )

    # Safety check: make sure the new version is NOT yet present.
    assert "1.2.4" not in deployment_contents, (
        f"{DEPLOYMENT_YAML} already references 1.2.4; this should only "
        f"appear *after* the student performs the bump."
    )


def test_changelog_md_exact_contents(changelog_contents):
    """
    CHANGELOG.md must contain only the initial [1.2.3] entry and *not*
    yet have a [1.2.4] section.
    """
    expected = textwrap.dedent(
        """\
        # Changelog

        All notable changes to this project will be documented in this file.

        ## [1.2.3] - 2024-05-01
        ### Added
        - Initial release of example-operator
        """
    )
    assert changelog_contents.rstrip("\n") == expected.rstrip(
        "\n"
    ), (
        f"{CHANGELOG_MD} does not match the expected initial contents. "
        f"Ensure the file has the unmodified 1.2.3 section only."
    )

    assert "## [1.2.4]" not in changelog_contents, (
        f"{CHANGELOG_MD} already contains a 1.2.4 section; this should "
        f"be added only after completing the task."
    )


def test_log_file_absent_at_start():
    """
    The version_bump.log file must *not* exist before the student begins
    the exercise.
    """
    assert not LOG_FILE.exists(), (
        f"{LOG_FILE} should not be present at the beginning of the task."
    )