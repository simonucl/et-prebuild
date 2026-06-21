# test_initial_state.py
#
# Pytest suite that validates the operating-system state **before** the
# learner begins work on the “collection-download log” exercise.
#
# It checks only the prerequisites that must already be present and **does
# not** look for any artefacts that the learner is expected to create
# later (e.g. summary_report.csv or errors.log).

from pathlib import Path
import pytest

DATASETS_DIR = Path("/home/user/datasets")
LOG_FILE = DATASETS_DIR / "download.log"

EXPECTED_LINES = [
    "[2023-06-01 10:15:23] OK imagenet_1 152.3MB",
    "[2023-06-01 10:16:05] OK imagenet_2 153.1MB",
    "[2023-06-01 10:16:45] FAIL coco_2017 -",
    "[2023-06-01 10:17:12] OK voc_2012 2.1MB",
    "[2023-06-01 10:18:01] FAIL places365_basic -",
    "[2023-06-01 10:18:34] OK cifar10 0.16MB",
    "[2023-06-01 10:19:10] OK cifar100 0.19MB",
    "[2023-06-01 10:20:22] OK mnist 0.05MB",
    "[2023-06-01 10:21:55] OK fashion_mnist 0.06MB",
    "[2023-06-01 10:22:26] FAIL kitti -",
    "[2023-06-02 09:12:05] OK lsun 34.2MB",
    "[2023-06-02 09:13:11] OK cityscapes 11.3MB",
    "[2023-06-02 09:14:49] OK sun397 23.5MB",
    "[2023-06-02 09:15:30] OK camvid 2.4MB",
    "[2023-06-02 09:16:10] FAIL imagenet21k -",
]


def test_datasets_directory_exists():
    """
    The base directory /home/user/datasets must already exist and be writable.
    """
    assert DATASETS_DIR.exists(), f"Required directory {DATASETS_DIR} is missing."
    assert DATASETS_DIR.is_dir(), f"{DATASETS_DIR} exists but is not a directory."


def test_download_log_exists_and_is_file():
    """
    The raw log file download.log must be present and be a regular file.
    """
    assert LOG_FILE.exists(), f"Required file {LOG_FILE} is missing."
    assert LOG_FILE.is_file(), f"{LOG_FILE} exists but is not a regular file."


def test_download_log_contents_are_exact():
    """
    The log file must contain exactly the 15 expected lines, in order and
    without any extra or missing characters (aside from the terminating
    newline which is optional on the last line in Unix).
    """
    raw_text = LOG_FILE.read_text(encoding="utf-8").rstrip("\n")
    actual_lines = raw_text.split("\n")

    assert actual_lines == EXPECTED_LINES, (
        "The contents of download.log do not match the expected initial "
        "state.\n\n"
        "Expected lines:\n"
        + "\n".join(EXPECTED_LINES)
        + "\n\nActual lines:\n"
        + "\n".join(actual_lines)
    )

    assert len(actual_lines) == 15, (
        f"download.log should contain exactly 15 lines, found {len(actual_lines)}."
    )