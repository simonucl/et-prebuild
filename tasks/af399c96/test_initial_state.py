# test_initial_state.py
#
# Pytest suite that validates the ORIGINAL state of the filesystem
# before the student performs any action on the Kubernetes manifests.
#
# Assumptions (truth):
#   • Only /home/user/k8s/manifests/ exists (not the _utf8 dir).
#   • Three manifests are present, encoded in ISO-8859-1 **with CRLF**.
#   • deployment.yaml still uses apiVersion extensions/v1beta1
#     and has NO selector block.
#   • conversion.log does NOT exist yet.
#
# Any deviation from this baseline must fail with a clear message.

import os
import re
import pytest
from pathlib import Path

HOME = Path("/home/user")
K8S_DIR = HOME / "k8s"
MANIFESTS_DIR = K8S_DIR / "manifests"
MANIFESTS_UTF8_DIR = K8S_DIR / "manifests_utf8"
LOG_FILE = K8S_DIR / "conversion.log"

FILES = {
    "deployment.yaml": {
        "must_contain": [
            "apiVersion: extensions/v1beta1",
            "kind: Deployment",
        ],
        "must_not_contain": [
            "apiVersion: apps/v1",
            "selector:",
        ],
    },
    "service.yaml": {
        "must_contain": [
            "apiVersion: v1",
            "kind: Service",
        ],
        "must_not_contain": [
            "apiVersion: apps/v1",
        ],
    },
    "ingress.yaml": {
        "must_contain": [
            "apiVersion: networking.k8s.io/v1",
            "kind: Ingress",
        ],
        "must_not_contain": [
            "apiVersion: apps/v1",
        ],
    },
}


def read_binary(path: Path) -> bytes:
    with path.open("rb") as fh:
        return fh.read()


def assert_crlf_only(data: bytes, file_path: Path):
    """
    Ensure *every* newline in `data` is CRLF, i.e. the sequence b'\\r\\n'.
    Fail if we find a bare LF or a bare CR.
    """
    # Quick sanity: we must see at least one CRLF
    assert b"\r\n" in data, f"{file_path} does not contain CRLF new-lines."

    # Reject bare LF not preceded by CR
    bare_lf = re.search(rb"(?<!\r)\n", data)
    assert (
        bare_lf is None
    ), f"{file_path} contains bare LF characters; expected only CRLF endings."

    # Reject bare CR not followed by LF
    bare_cr = re.search(rb"\r(?!\n)", data)
    assert (
        bare_cr is None
    ), f"{file_path} contains bare CR characters; expected only CRLF endings."


def assert_decodable_as_latin1(data: bytes, file_path: Path):
    """
    ISO-8859-1 can decode any 0x00–0xFF byte, so decoding will never fail.
    Nevertheless, we purposely attempt decode and ensure it round-trips.
    """
    text = data.decode("latin-1")  # should never raise
    # Re-encode and compare to original bytes to confirm *nothing* changed.
    assert (
        text.encode("latin-1") == data
    ), f"{file_path} is not clean Latin-1 encodable."


@pytest.fixture(scope="module")
def manifest_paths():
    return {name: MANIFESTS_DIR / name for name in FILES}


def test_required_directories_and_files_exist(manifest_paths):
    # k8s/ directory must exist
    assert K8S_DIR.is_dir(), f"Missing directory: {K8S_DIR}"
    # manifests directory must exist
    assert MANIFESTS_DIR.is_dir(), f"Missing directory: {MANIFESTS_DIR}"
    # manifests_utf8 directory MUST NOT exist yet
    assert (
        not MANIFESTS_UTF8_DIR.exists()
    ), f"Directory {MANIFESTS_UTF8_DIR} should not exist before conversion."
    # conversion.log must not exist yet
    assert (
        not LOG_FILE.exists()
    ), f"{LOG_FILE} should not exist prior to running the conversion task."

    # All three manifest files must be present
    for name, path in manifest_paths.items():
        assert path.is_file(), f"Expected manifest file is missing: {path}"


@pytest.mark.parametrize("filename", sorted(FILES.keys()))
def test_each_manifest_is_latin1_with_crlf_and_expected_content(manifest_paths, filename):
    path = manifest_paths[filename]
    data = read_binary(path)

    # Encoding & EOL checks
    assert_crlf_only(data, path)
    assert_decodable_as_latin1(data, path)

    text = data.decode("latin-1")

    # Content checks: must_contain
    for expected in FILES[filename]["must_contain"]:
        assert (
            expected in text
        ), f"{path} is missing expected line: '{expected}'"

    # Content checks: must_not_contain
    for forbidden in FILES[filename]["must_not_contain"]:
        assert (
            forbidden not in text
        ), f"{path} unexpectedly already contains '{forbidden}' (should be introduced only after conversion)."


def test_deployment_lacks_selector_block(manifest_paths):
    """
    Guard clause: The original deployment.yaml must NOT have a spec.selector
    block, otherwise the student would have nothing to fix.
    """
    path = manifest_paths["deployment.yaml"]
    text = read_binary(path).decode("latin-1")

    assert (
        "selector:" not in text
    ), f"{path} already contains a 'selector:' block; expected it to be missing pre-conversion."