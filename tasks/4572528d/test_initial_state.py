# test_initial_state.py
#
# Pytest suite that validates the OS / filesystem **before** the student
# performs any action for the “deterministic Kubernetes operator benchmark”.
# We confirm that the provided test-harness is present and behaves as
# expected, and that none of the artefacts the student must create exist yet.
#
# NOTE: Do **not** modify this file.  Grading depends on these assertions.

import os
import stat
import subprocess
import sys
from pathlib import Path

# Static paths used throughout the assignment
HOME = Path("/home/user")
MANIFEST_DIR = HOME / "k8s_operator" / "manifests"
DEPLOYMENT_YAML = MANIFEST_DIR / "deployment.yaml"
SERVICE_YAML = MANIFEST_DIR / "service.yaml"
CONFIGMAP_YAML = MANIFEST_DIR / "configmap.yaml"
HARNESS = HOME / "benchmark_scripts" / "apply_manifest.sh"

RESULTS_DIR = HOME / "benchmark_results"
RESULT_LOG = RESULTS_DIR / "operator_benchmark.log"


def _is_executable(path: Path) -> bool:
    """Return True if the given path is executable by the current user."""
    st = path.stat()
    return bool(st.st_mode & stat.S_IXUSR)


def test_manifest_files_exist():
    """All manifest YAML files must exist prior to running the benchmark."""
    for manifest in (DEPLOYMENT_YAML, SERVICE_YAML, CONFIGMAP_YAML):
        assert manifest.is_file(), (
            f"Required manifest file missing:\n  {manifest}\n"
            "The exercise cannot proceed without this file."
        )


def test_apply_manifest_script_exists_and_executable():
    """The harness script must be present and executable."""
    assert HARNESS.is_file(), (
        f"Harness script not found at expected location:\n  {HARNESS}"
    )
    assert _is_executable(HARNESS), (
        f"Harness script exists but is not executable:\n  {HARNESS}\n"
        "Run `chmod +x` on the script or fix permissions."
    )


def test_harness_deterministic_output():
    """
    Invoking the harness on each manifest should yield the exact,
    deterministic output as described in the specification.
    """
    expected_outputs = {
        DEPLOYMENT_YAML: "Applied deployment.yaml in 12ms\n",
        SERVICE_YAML: "Applied service.yaml in 8ms\n",
        CONFIGMAP_YAML: "Applied configmap.yaml in 5ms\n",
    }

    for manifest_path, expected_stdout in expected_outputs.items():
        # Use str() so subprocess can handle the Path object
        proc = subprocess.run(
            [str(HARNESS), str(manifest_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        assert proc.stdout == expected_stdout, (
            f"Unexpected harness output for {manifest_path.name}.\n"
            f"Expected: {expected_stdout!r}\n"
            f"Got:      {proc.stdout!r}"
        )
        # Harness must not emit anything on stderr for valid inputs
        assert proc.stderr == "", (
            f"Harness wrote to stderr for {manifest_path.name}:\n{proc.stderr}"
        )


def test_results_directory_does_not_exist_yet():
    """
    The student has not yet created the results directory; it should be absent
    before the task begins.
    """
    assert not RESULTS_DIR.exists(), (
        f"Results directory already exists at {RESULTS_DIR}.\n"
        "The directory should be created by the student during the exercise, "
        "not before it starts."
    )


def test_benchmark_log_does_not_exist_yet():
    """
    The final report file should not exist before the student runs the
    benchmarking workflow.
    """
    assert not RESULT_LOG.exists(), (
        f"Benchmark log already exists at {RESULT_LOG}.\n"
        "This file must be created by the student as part of the task."
    )