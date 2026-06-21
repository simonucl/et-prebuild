# test_initial_state.py
#
# Pytest suite that validates the **initial** filesystem state for the
# Kubernetes-manifest counting exercise.  These tests intentionally check
# only the pre-existing inputs; they do **not** look for, nor care about,
# any output artefacts the student will later create.
#
# The tests will fail fast and with clear messages if:
#   • the expected /home/user/k8s-configs/ directory is missing,
#   • any of the 7 *.yaml files is missing or an unexpected file is present,
#   • a YAML file lacks a single “kind:” entry or that entry’s value deviates
#     from the canonical expectation.
#
# Requirements:
#   • stdlib + pytest only
#   • no checks for the eventual `kind_frequency.txt`

import os
import re
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constants describing the canonical initial state.                           #
# --------------------------------------------------------------------------- #
CONFIG_DIR = Path("/home/user/k8s-configs")

EXPECTED_FILES = {
    "backend-deploy.yaml":     "Deployment",
    "backend-service.yaml":    "Service",
    "cache-configmap.yaml":    "ConfigMap",
    "frontend-deploy.yaml":    "Deployment",
    "frontend-service.yaml":   "Service",
    "redis-service.yaml":      "Service",
    "redis-stateful.yaml":     "StatefulSet",
}


# --------------------------------------------------------------------------- #
# Helper functions                                                            #
# --------------------------------------------------------------------------- #
KIND_RE = re.compile(r"^\s*kind:\s*(\S+)\s*$", re.IGNORECASE)


def extract_kind(file_path: Path) -> str:
    """
    Returns the value that follows the first (and only) 'kind:' key
    in the given YAML file.  Raises AssertionError if zero or multiple
    kinds are found.
    """
    kinds_found = []
    with file_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            m = KIND_RE.match(line)
            if m:
                kinds_found.append(m.group(1))

    assert kinds_found, f"File '{file_path}' contains no 'kind:' entry."
    assert len(kinds_found) == 1, (
        f"File '{file_path}' contains multiple 'kind:' entries: {kinds_found}"
    )
    return kinds_found[0]


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
def test_config_directory_exists():
    assert CONFIG_DIR.is_dir(), (
        f"Expected directory '{CONFIG_DIR}' does not exist. "
        "Have the manifests been moved or deleted?"
    )


def test_expected_yaml_files_present_and_only_them():
    actual_files = {p.name for p in CONFIG_DIR.glob("*.yaml")}
    missing = EXPECTED_FILES.keys() - actual_files
    unexpected = actual_files - EXPECTED_FILES.keys()

    assert not missing, (
        "The following expected YAML files are missing from "
        f"'{CONFIG_DIR}': {sorted(missing)}"
    )
    assert not unexpected, (
        "Found unexpected YAML files in "
        f"'{CONFIG_DIR}': {sorted(unexpected)}"
    )


@pytest.mark.parametrize("filename, expected_kind", EXPECTED_FILES.items())
def test_each_yaml_contains_correct_kind(filename, expected_kind):
    file_path = CONFIG_DIR / filename
    assert file_path.is_file(), (
        f"Cannot locate expected file '{file_path}'."
    )
    actual_kind = extract_kind(file_path)
    assert actual_kind == expected_kind, (
        f"File '{filename}' has kind '{actual_kind}', "
        f"but expected '{expected_kind}'."
    )