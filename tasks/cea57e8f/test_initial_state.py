# test_initial_state.py
#
# This test-suite verifies the **initial** state of the operating system /
# filesystem before the student performs any action for the compression
# benchmark task.

import os
import stat
import pytest
import re

ARTIFACT_DIR = "/home/user/artifacts"
TAR_PATH = os.path.join(ARTIFACT_DIR, "build_v1.2.3.tar")
OPTIONAL_GZ_PATH = TAR_PATH + ".gz"

BENCHMARK_DIR = "/home/user/benchmark"
BENCHMARK_LOG = os.path.join(BENCHMARK_DIR, "compress_benchmark.log")


def _mode(path):
    """Return the permission bits (e.g. 0o755) for the given filesystem path."""
    return stat.S_IMODE(os.stat(path).st_mode)


def test_artifact_directory_exists_and_has_correct_permissions():
    assert os.path.isdir(ARTIFACT_DIR), (
        f"Required directory {ARTIFACT_DIR} is missing."
    )
    expected_mode = 0o755
    actual_mode = _mode(ARTIFACT_DIR)
    assert actual_mode == expected_mode, (
        f"{ARTIFACT_DIR} should have permissions {oct(expected_mode)}, "
        f"but has {oct(actual_mode)}."
    )


def test_tar_file_exists_with_expected_properties():
    assert os.path.isfile(TAR_PATH), (
        f"Required build artifact {TAR_PATH} is missing."
    )

    # Permission check
    expected_mode = 0o644
    actual_mode = _mode(TAR_PATH)
    assert actual_mode == expected_mode, (
        f"{TAR_PATH} should have permissions {oct(expected_mode)}, "
        f"but has {oct(actual_mode)}."
    )

    # Size sanity-check (~11 KB according to spec)
    size_bytes = os.path.getsize(TAR_PATH)
    lower_bound = 5 * 1024     #  5 KB – loose lower bound
    upper_bound = 50 * 1024    # 50 KB – loose upper bound
    assert lower_bound <= size_bytes <= upper_bound, (
        f"{TAR_PATH} should be roughly 11 KB; detected size {size_bytes} bytes."
    )

    # Basic content check – make sure it contains the expected phrase.
    with open(TAR_PATH, "rb") as fh:
        sample = fh.read(512)  # read a small block
    assert b"Hello Build Engineer" in sample, (
        f"{TAR_PATH} does not appear to contain the expected placeholder content."
    )


def test_optional_gz_not_present_initially():
    # The compressed artifact should NOT exist before the student runs their command.
    assert not os.path.exists(OPTIONAL_GZ_PATH), (
        f"{OPTIONAL_GZ_PATH} should not exist before compression is performed."
    )


@pytest.mark.parametrize("path", [BENCHMARK_DIR, BENCHMARK_LOG])
def test_benchmark_outputs_absent_initially(path):
    # Neither the benchmark directory nor the log file should exist yet.
    assert not os.path.exists(path), (
        f"Output path {path} should not exist before the benchmark is executed."
    )