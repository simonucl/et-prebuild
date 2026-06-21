# test_initial_state.py
#
# Pytest suite that validates the initial filesystem state **before**
# the student executes the task.  These tests assert the exact structure
# and contents that subsequent grading relies on.
#
# Rules checked:
#   1. /home/user/k8s-manifests exists and is a directory
#   2. It contains *exactly* the three YAML files listed in the task
#   3. Each file has the precise byte-size expected
#   4. The report file (`usage_report.log`) must NOT exist yet
#
# Any deviation will fail the test with a clear, descriptive message.

import os
import stat
import pytest

MANIFEST_DIR = "/home/user/k8s-manifests"
EXPECTED_FILES = {
    "deployment.yaml": 25,
    "service.yaml": 29,
    "configmap.yaml": 31,
}
REPORT_FILE = "usage_report.log"
SEPARATOR_LINE_LENGTH = 35  # for completeness, though not checked here


def test_manifest_directory_exists_and_is_dir():
    assert os.path.exists(MANIFEST_DIR), (
        f"Required directory {MANIFEST_DIR!r} is missing."
    )
    assert stat.S_ISDIR(os.stat(MANIFEST_DIR).st_mode), (
        f"{MANIFEST_DIR!r} exists but is not a directory."
    )


def test_expected_yaml_files_exist_with_correct_sizes():
    for filename, expected_size in EXPECTED_FILES.items():
        path = os.path.join(MANIFEST_DIR, filename)
        assert os.path.exists(path), (
            f"Expected file {path!r} is missing."
        )
        assert stat.S_ISREG(os.stat(path).st_mode), (
            f"{path!r} exists but is not a regular file."
        )
        actual_size = os.path.getsize(path)
        assert actual_size == expected_size, (
            f"{path!r} has size {actual_size} bytes, expected {expected_size} bytes."
        )


def test_no_additional_files_present():
    present = sorted(os.listdir(MANIFEST_DIR))
    expected = sorted(list(EXPECTED_FILES.keys()))
    extras = [f for f in present if f not in expected]
    missing = [f for f in expected if f not in present]
    assert not missing, (
        f"Missing expected file(s): {', '.join(missing)}"
    )
    assert not extras, (
        "Unexpected extra file(s) present in directory "
        f"{MANIFEST_DIR!r}: {', '.join(extras)}"
    )


def test_report_file_does_not_exist_yet():
    report_path = os.path.join(MANIFEST_DIR, REPORT_FILE)
    assert not os.path.exists(report_path), (
        f"Report file {report_path!r} should NOT exist before the task is completed."
    )