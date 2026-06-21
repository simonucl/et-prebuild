# test_initial_state.py
#
# This pytest file validates that the *initial* filesystem state is exactly
# what the assignment description promises—before the student executes any
# commands.  If any check fails the error message pin-points what is wrong
# so that the learner immediately knows what part of the starting point is
# missing or corrupted.

import io
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Canonical paths used throughout the checks
# --------------------------------------------------------------------------- #
BASE_DIR = Path("/home/user/mlops")
CONFIG_DIR = BASE_DIR / "configs"
REGISTRY_DIR = BASE_DIR / "registry"
LOGS_DIR = BASE_DIR / "logs"

YAML_FILE = CONFIG_DIR / "experiments.yaml"
TOML_FILE = REGISTRY_DIR / "artifacts.toml"
LOG_FILE = LOGS_DIR / "experiment_registration.log"


# --------------------------------------------------------------------------- #
# Expected *initial* file contents (including trailing newline)
# --------------------------------------------------------------------------- #
EXPECTED_YAML = """\
experiments:
  - id: 1
    name: baseline_cnn
    dataset: mnist
    accuracy: 0.975
    artifact_uri: s3://ml-bucket/experiments/1
  - id: 2
    name: mobilenet_v2
    dataset: cifar10
    accuracy: 0.855
    artifact_uri: s3://ml-bucket/experiments/2
"""

EXPECTED_TOML = """\
# MLOps experiment artifact registry
[baseline_cnn]
uri = "s3://ml-bucket/experiments/1"

[mobilenet_v2]
uri = "s3://ml-bucket/experiments/2"
"""


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def read_text(path: Path) -> str:
    """
    Read a file as UTF-8 text while explicitly raising an error if binary data
    or decoding issues are encountered.
    """
    # Using TextIOWrapper so we get the same behavior on all platforms
    with path.open("rb") as fh:
        data = fh.read()
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise AssertionError(f"File {path} is not valid UTF-8 text") from exc


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_directory_structure_exists():
    """
    Verify that the required directory hierarchy already exists.
    """
    for d in (BASE_DIR, CONFIG_DIR, REGISTRY_DIR, LOGS_DIR):
        assert d.is_dir(), (
            f"Expected directory {d} to exist before the task starts, "
            f"but it is missing."
        )


def test_experiments_yaml_content_pristine():
    """
    The YAML file must exist and contain the two original experiment entries
    only (no resnet50_cifar10 yet).
    """
    assert YAML_FILE.is_file(), (
        f"{YAML_FILE} is missing.  The starter repository should contain this "
        f"file with the two baseline experiments."
    )

    content = read_text(YAML_FILE)
    # Confirm *exact* byte-to-byte match including final newline.
    assert content == EXPECTED_YAML, (
        "The contents of experiments.yaml do not match the expected initial "
        "state.  The file should contain ONLY the two baseline experiment "
        "blocks and nothing else:\n"
        f"--- expected ---\n{EXPECTED_YAML}\n"
        f"--- found ---\n{content}"
    )


def test_artifacts_toml_content_pristine():
    """
    The TOML registry file must exist with only the two original tables.
    """
    assert TOML_FILE.is_file(), (
        f"{TOML_FILE} is missing.  The starter repository should provide this "
        "file containing the artifact registry header and two tables."
    )

    content = read_text(TOML_FILE)
    assert content == EXPECTED_TOML, (
        "The contents of artifacts.toml do not match the expected initial "
        "state.  The file should contain ONLY the header comment and the two "
        "baseline tables:\n"
        f"--- expected ---\n{EXPECTED_TOML}\n"
        f"--- found ---\n{content}"
    )


def test_log_file_absent_initially():
    """
    The audit log file must NOT exist before the student performs the task.
    """
    assert not LOG_FILE.exists(), (
        f"The file {LOG_FILE} already exists.  The initial state should have "
        f"no audit log; the student will create it as part of the exercise."
    )


def test_new_experiment_not_registered_anywhere_yet():
    """
    Sanity check that the string 'resnet50_cifar10' does not yet appear in
    either configuration file.
    """
    yaml_text = read_text(YAML_FILE)
    toml_text = read_text(TOML_FILE)

    assert "resnet50_cifar10" not in yaml_text, (
        "The experiment 'resnet50_cifar10' already appears in experiments.yaml. "
        "This should NOT be the case before the student starts."
    )
    assert "resnet50_cifar10" not in toml_text, (
        "The experiment 'resnet50_cifar10' already appears in artifacts.toml. "
        "This should NOT be the case before the student starts."
    )