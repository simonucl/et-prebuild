# test_initial_state.py
#
# This test-suite validates the **starting** filesystem state that
# students are given _before_ they attempt the exercise.  If any of
# these tests fail it means the template VM / container is not in the
# expected “clean slate” configuration.
#
# DO NOT modify this file in the learner’s solution; it is executed by
# the autograder only.

import os
import re
import stat
import pytest
from pathlib import Path


HOME = Path("/home/user")
MANIFEST_DIR = HOME / "manifests"
OUTPUT_DIR = HOME / "output"

DEPLOYMENT = MANIFEST_DIR / "deployment.yaml"
SERVICE = MANIFEST_DIR / "service.yaml"
CONFIGMAP = MANIFEST_DIR / "configmap.yaml"

CSV_FILE = OUTPUT_DIR / "manifest_summary.csv"
LOG_FILE = OUTPUT_DIR / "update.log"


# --------------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------------
def read_text(path: Path) -> str:
    """Return file content as text, fail with readable error if missing."""
    if not path.exists():
        pytest.fail(f"Expected file missing: {path}")
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {path}: {exc}")


def has_permission_644(path: Path) -> bool:
    """Return True if path has mode 0o644 (regular file, rw-r--r--)."""
    mode = path.stat().st_mode
    return stat.S_ISREG(mode) and (mode & 0o777) == 0o644


# --------------------------------------------------------------------
# Tests for manifest directory and basic files
# --------------------------------------------------------------------
def test_manifest_directory_present_and_readable():
    assert MANIFEST_DIR.is_dir(), f"Directory {MANIFEST_DIR} is missing."
    assert os.access(MANIFEST_DIR, os.R_OK), f"Directory {MANIFEST_DIR} is not readable."


@pytest.mark.parametrize(
    "path",
    [DEPLOYMENT, SERVICE, CONFIGMAP],
)
def test_each_manifest_file_exists(path: Path):
    assert path.is_file(), f"Required manifest file is missing: {path}"
    assert os.access(path, os.R_OK), f"Manifest file is not readable: {path}"


# --------------------------------------------------------------------
# Validate contents of deployment.yaml
# --------------------------------------------------------------------
def test_deployment_contains_initial_image_only():
    text = read_text(DEPLOYMENT)
    assert "image: nginx:1.19" in text, (
        "deployment.yaml should start with image nginx:1.19 but it is missing."
    )
    assert "nginx:1.20" not in text, (
        "deployment.yaml already contains nginx:1.20; the starting state must still be 1.19."
    )


def test_deployment_kind_and_name():
    """
    Confirm the YAML header contains the expected `kind` and `metadata.name`.
    Simple regex parsing is enough; PyYAML is intentionally avoided.
    """
    text = read_text(DEPLOYMENT)
    kind_match = re.search(r"^\s*kind:\s*Deployment\s*$", text, re.MULTILINE)
    name_match = re.search(r"^\s*name:\s*webserver\s*$", text, re.MULTILINE)
    assert kind_match, "deployment.yaml should declare kind: Deployment."
    assert name_match, "deployment.yaml should declare metadata.name: webserver."


# --------------------------------------------------------------------
# Validate contents of service.yaml and configmap.yaml
# --------------------------------------------------------------------
@pytest.mark.parametrize(
    "path,expected_kind,expected_name",
    [
        (SERVICE, "Service", "web-svc"),
        (CONFIGMAP, "ConfigMap", "web-config"),
    ],
)
def test_other_manifests_kind_and_name(path: Path, expected_kind: str, expected_name: str):
    text = read_text(path)
    kind_match = re.search(rf"^\s*kind:\s*{re.escape(expected_kind)}\s*$", text, re.MULTILINE)
    name_match = re.search(rf"^\s*name:\s*{re.escape(expected_name)}\s*$", text, re.MULTILINE)
    assert kind_match, f"{path.name} should declare kind: {expected_kind}."
    assert name_match, f"{path.name} should declare metadata.name: {expected_name}."


# --------------------------------------------------------------------
# Output directory must be clean in the initial state
# --------------------------------------------------------------------
def test_output_directory_absence_or_clean():
    """
    The /home/user/output directory should either not exist yet or be empty.
    In particular, the files that the learner is supposed to create must NOT
    exist in the initial snapshot.
    """
    if not OUTPUT_DIR.exists():
        pytest.skip(f"{OUTPUT_DIR} does not exist yet — this is allowed in the initial state.")

    # Directory exists: make sure the specific target files are absent.
    unexpected = []
    for path in (CSV_FILE, LOG_FILE):
        if path.exists():
            unexpected.append(str(path))
    if unexpected:
        pytest.fail(
            "Output directory already contains files that should be created by the learner later: "
            + ", ".join(unexpected)
        )


# --------------------------------------------------------------------
# Sanity: ensure no accidental 644 files pre-created
# --------------------------------------------------------------------
def test_no_preexisting_csv_or_log():
    assert not CSV_FILE.exists(), f"{CSV_FILE} must NOT exist before the task begins."
    assert not LOG_FILE.exists(), f"{LOG_FILE} must NOT exist before the task begins."