# test_initial_state.py
#
# Pytest suite that verifies the expected, pre-existing state of the
# filesystem **before** the student executes any commands.
#
# What we check:
# 1. The directory /home/user/manifests exists and has the correct mode.
# 2. Exactly three *.yaml files are present in that directory.
# 3. Each expected file exists, has the right permissions, and contains
#    the correct Kubernetes “kind”.
#
# NOTE:
# • We explicitly do *not* test for /home/user/manifest_report.log or any
#   other output artifacts​—​those belong to the student solution.
# • Only the Python standard library and pytest are used.

import os
import stat
from pathlib import Path

import pytest


MANIFEST_DIR = Path("/home/user/manifests")

EXPECTED_MANIFESTS = {
    "nginx-deployment.yaml": "Deployment",
    "nginx-service.yaml": "Service",
    "nginx-ingress.yaml": "Ingress",
}

DIR_MODE_EXPECTED = 0o755
FILE_MODE_EXPECTED = 0o644


def _mode(path: Path) -> int:
    """Return the permission bits (e.g. 0o755) of a file or directory."""
    return stat.S_IMODE(path.stat().st_mode)


def test_manifest_directory_exists_and_mode():
    assert MANIFEST_DIR.exists(), (
        f"Expected directory {MANIFEST_DIR} to exist, but it does not."
    )
    assert MANIFEST_DIR.is_dir(), (
        f"Expected {MANIFEST_DIR} to be a directory, but it is not."
    )

    mode = _mode(MANIFEST_DIR)
    assert mode == DIR_MODE_EXPECTED, (
        f"Directory {MANIFEST_DIR} should have mode {oct(DIR_MODE_EXPECTED)}, "
        f"but its mode is {oct(mode)}."
    )


def test_exact_yaml_file_set_present():
    yaml_files = {p.name for p in MANIFEST_DIR.glob("*.yaml")}
    assert yaml_files == set(EXPECTED_MANIFESTS.keys()), (
        "The manifests directory must contain exactly these files:\n"
        f"  {', '.join(EXPECTED_MANIFESTS.keys())}\n"
        f"Found instead:\n"
        f"  {', '.join(sorted(yaml_files)) or '(none)'}"
    )


@pytest.mark.parametrize("filename,expected_kind", EXPECTED_MANIFESTS.items())
def test_each_manifest_file_properties_and_contents(filename, expected_kind):
    file_path = MANIFEST_DIR / filename
    assert file_path.is_file(), (
        f"Expected file {file_path} to exist, but it is missing."
    )

    # Permissions
    mode = _mode(file_path)
    assert mode == FILE_MODE_EXPECTED, (
        f"File {file_path} should have mode {oct(FILE_MODE_EXPECTED)}, "
        f"but its mode is {oct(mode)}."
    )

    # Contents
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        pytest.fail(f"Could not read {file_path}: {exc}")

    kind_line = f"kind: {expected_kind}"
    assert kind_line in content, (
        f"File {file_path} does not appear to describe a Kubernetes "
        f"{expected_kind}. Expected to find the line '{kind_line}'."
    )