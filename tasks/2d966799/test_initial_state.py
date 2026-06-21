# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem state
# before the student performs any actions.  It ensures that
#
#   • Only the three expected Kubernetes manifest files are present
#     under /home/user/k8s/manifests.
#   • Each manifest contains the expected header line, kind, name and replicas.
#   • No sub-directories exist inside /home/user/k8s/manifests.
#   • No output artefacts (summary / logs) exist yet.
#
# The tests use only the Python standard library + pytest and will emit clear
# failure messages if the state deviates from the specification.

import os
import pathlib
import re

import pytest

HOME = pathlib.Path("/home/user")
K8S_DIR = HOME / "k8s"
MANIFEST_DIR = K8S_DIR / "manifests"

# --------------------------------------------------------------------------- #
# Expected manifest metadata (filename  ->  dict(kind=…, name=…, replicas=…))
# --------------------------------------------------------------------------- #
EXPECTED_MANIFESTS = {
    "deployment-api.yaml": {
        "kind": "Deployment",
        "name": "api-server",
        "replicas": "2",
    },
    "deployment-web.yaml": {
        "kind": "Deployment",
        "name": "web-frontend",
        "replicas": "3",
    },
    "statefulset-db.yaml": {
        "kind": "StatefulSet",
        "name": "db-storage",
        "replicas": "1",
    },
}


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def _read(path: pathlib.Path) -> str:
    """Read a text file as UTF-8 and return its contents."""
    with path.open("r", encoding="utf-8") as fp:
        return fp.read()


def _assert_file_contains(path: pathlib.Path, needle: str) -> None:
    """Assert that *needle* is present in the file located at *path*."""
    data = _read(path)
    assert (
        needle in data
    ), f"File {path} should contain the line/substring {needle!r} but it was not found."


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_manifest_directory_exists_and_only_expected_files_present() -> None:
    """The manifests directory must exist and contain *exactly* the expected files."""
    assert MANIFEST_DIR.is_dir(), f"Expected directory {MANIFEST_DIR} is missing."

    # Collect directory entries (excluding '.' and '..').
    entries = [e.name for e in MANIFEST_DIR.iterdir()]
    expected_files = set(EXPECTED_MANIFESTS.keys())

    # No extra or missing files.
    assert set(entries) == expected_files, (
        f"{MANIFEST_DIR} should contain exactly the files "
        f"{sorted(expected_files)}, but actually has {sorted(entries)}."
    )

    # Ensure none of the entries is a directory (spec forbids sub-directories).
    for entry in MANIFEST_DIR.iterdir():
        assert entry.is_file(), (
            f"Found sub-directory {entry} inside {MANIFEST_DIR}; "
            "the spec states no sub-directories should be present."
        )


@pytest.mark.parametrize("filename,meta", EXPECTED_MANIFESTS.items())
def test_each_manifest_has_expected_header_and_content(filename: str, meta: dict) -> None:
    """Validate header line, kind, name, replicas and trailing newline."""
    path = MANIFEST_DIR / filename
    assert path.is_file(), f"Expected manifest file {path} does not exist."

    content = _read(path)

    # 1. File must end with exactly one trailing newline.
    assert content.endswith(
        "\n"
    ), f"File {path} must end with a single trailing newline."

    # 2. Header line (“# filename:<exact-file-name>”).
    expected_header = f"# filename:{filename}"
    assert content.splitlines()[0] == expected_header, (
        f"{path} first line should be {expected_header!r} "
        f"but was {content.splitlines()[0]!r}."
    )

    # 3. Verify 'kind', 'metadata.name', 'spec.replicas' fields are present.
    _assert_file_contains(path, f"kind: {meta['kind']}")
    # Use regex to avoid matching container.name lines; restrict to leading spaces.
    name_regex = re.compile(rf"^\s*name:\s*{re.escape(meta['name'])}\s*$", re.MULTILINE)
    assert name_regex.search(
        content
    ), f"{path} does not contain metadata.name = {meta['name']!r}."

    _assert_file_contains(path, f"replicas: {meta['replicas']}")


def test_no_output_artefacts_exist_yet() -> None:
    """Ensure that summary/log directories or files have not yet been created."""
    summary_dir = K8S_DIR / "summary"
    summary_file = summary_dir / "manifest_summary.tsv"
    logs_dir = K8S_DIR / "logs"
    logs_file = logs_dir / "extraction.log"

    # The directories themselves may or may not exist, but the files must not.
    assert not summary_file.exists(), (
        f"{summary_file} should not exist before the student runs their solution."
    )
    assert not logs_file.exists(), (
        f"{logs_file} should not exist before the student runs their solution."
    )