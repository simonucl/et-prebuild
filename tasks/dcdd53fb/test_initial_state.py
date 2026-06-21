# test_initial_state.py
#
# This test-suite asserts that the workstation is in the expected
# *initial* state before the student carries out the backup task.
# If any of the following tests fail, the workstation has been
# modified or provisioned incorrectly and the exercise cannot be
# graded reliably.
#
# Tested truths
# 1. /home/user/data/            : directory exists (0755)
# 2. /home/user/data/alpha.txt   : file exists (0644) with exact   "Hello Alpha\n"
# 3. /home/user/data/beta.txt    : file exists (0644) with exactly "Beta line1\nBeta line2\n"
# 4. /home/user/archive/         : DOES NOT exist
# 5. /home/user/archive/data_backup.tar.gz  : DOES NOT exist
# 6. /home/user/archive/backup_record.log   : DOES NOT exist
#
# Only the Python stdlib and pytest are used.

import os
import stat
from pathlib import Path

DATA_DIR = Path("/home/user/data")
ARCHIVE_DIR = Path("/home/user/archive")
ARCHIVE_FILE = ARCHIVE_DIR / "data_backup.tar.gz"
LOG_FILE = ARCHIVE_DIR / "backup_record.log"


def _octal_mode(path: Path) -> int:
    """
    Return the permission bits as an octal integer, e.g. 0o644.
    """
    return stat.S_IMODE(path.stat().st_mode)


def test_data_directory_exists_and_permissions():
    assert DATA_DIR.is_dir(), f"Required directory {DATA_DIR} is missing."
    expected_mode = 0o755
    actual_mode = _octal_mode(DATA_DIR)
    assert (
        actual_mode == expected_mode
    ), f"{DATA_DIR} should have permissions {oct(expected_mode)}, found {oct(actual_mode)}."


def test_source_files_exist_with_correct_contents_and_permissions():
    # alpha.txt
    alpha = DATA_DIR / "alpha.txt"
    assert alpha.is_file(), f"Missing source file {alpha}."
    alpha_expected_mode = 0o644
    alpha_mode = _octal_mode(alpha)
    assert (
        alpha_mode == alpha_expected_mode
    ), f"{alpha} should have permissions {oct(alpha_expected_mode)}, found {oct(alpha_mode)}."
    with alpha.open("rb") as fh:
        alpha_content = fh.read()
    assert (
        alpha_content == b"Hello Alpha\n"
    ), f"{alpha} content is incorrect. Expected exactly 'Hello Alpha\\n'."

    # beta.txt
    beta = DATA_DIR / "beta.txt"
    assert beta.is_file(), f"Missing source file {beta}."
    beta_expected_mode = 0o644
    beta_mode = _octal_mode(beta)
    assert (
        beta_mode == beta_expected_mode
    ), f"{beta} should have permissions {oct(beta_expected_mode)}, found {oct(beta_mode)}."
    with beta.open("rb") as fh:
        beta_content = fh.read()
    expected_beta = b"Beta line1\nBeta line2\n"
    assert (
        beta_content == expected_beta
    ), (
        f"{beta} content is incorrect.\n"
        f"Expected exactly:\n{expected_beta!r}\nGot:\n{beta_content!r}"
    )


def test_archive_directory_absent():
    assert not ARCHIVE_DIR.exists(), (
        f"{ARCHIVE_DIR} should NOT exist in the initial state. "
        "It will be created by the student's solution."
    )


def test_archive_and_log_files_absent():
    assert not ARCHIVE_FILE.exists(), (
        f"{ARCHIVE_FILE} must NOT exist before the student runs the backup."
    )
    assert not LOG_FILE.exists(), (
        f"{LOG_FILE} must NOT exist before the student runs the backup."
    )