# test_initial_state.py
#
# This pytest suite validates that the *initial* operating-system /
# filesystem state required for the “curl metrics” exercise is present
# and correct *before* the student begins working.
#
# It deliberately does **not** look for any output artefacts the student
# is expected to create (e.g. /home/user/observability/curl_metrics.log),
# only the immutable starting point that must already exist.

import os
import shutil
import subprocess
import textwrap

import pytest

# Constants describing the expected initial state.
METRICS_DIR = "/home/user/observability/metrics"
METRICS_FILE = os.path.join(METRICS_DIR, "exporter_stats.txt")
EXPECTED_FILE_BYTES = (
    b"up 1\n"
    b"scrape_duration_seconds 0.005\n"
    b"scrape_samples_post_metric_relabeling 15\n"
)
EXPECTED_FILE_SIZE = 76  # bytes


@pytest.fixture(scope="module")
def file_bytes():
    """Read and return the raw bytes of the metrics file."""
    if not os.path.isfile(METRICS_FILE):
        pytest.fail(
            f"Required file not found: {METRICS_FILE}\n"
            "Make sure the repository ships with the metrics fixture."
        )
    try:
        with open(METRICS_FILE, "rb") as fh:
            return fh.read()
    except Exception as exc:  # pragma: no cover  (safety net)
        pytest.fail(f"Unable to read {METRICS_FILE}: {exc}")


def test_metrics_directory_exists():
    assert os.path.isdir(
        METRICS_DIR
    ), f"Required directory missing: {METRICS_DIR}"


def test_metrics_file_exists_and_is_file():
    assert os.path.isfile(
        METRICS_FILE
    ), f"Required file missing: {METRICS_FILE}"


def test_metrics_file_size_is_exact():
    actual_size = os.path.getsize(METRICS_FILE)
    assert (
        actual_size == EXPECTED_FILE_SIZE
    ), textwrap.dedent(
        f"""\
        {METRICS_FILE} has wrong size.
        Expected: {EXPECTED_FILE_SIZE} bytes
        Found   : {actual_size} bytes
        """
    )


def test_metrics_file_contents_are_exact(file_bytes):
    assert (
        file_bytes == EXPECTED_FILE_BYTES
    ), textwrap.dedent(
        f"""\
        {METRICS_FILE} contents do not match expected fixture.
        Expected (repr):
        {EXPECTED_FILE_BYTES!r}
        Found (repr):
        {file_bytes!r}
        """
    )


def test_curl_binary_is_available():
    """
    The exercise explicitly instructs students to use curl.
    Ensure the binary is discoverable on PATH so the task is solvable.
    """
    curl_path = shutil.which("curl")
    assert curl_path is not None, "curl executable not found on PATH"
    # Optional sanity check that the binary can at least report its version.
    try:
        subprocess.run(
            [curl_path, "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"curl exists at {curl_path} but could not be executed: {exc}")