# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the operating
# system / filesystem before the student carries out the assignment
# “Launch a background ‘sleep 180’ job and write its PID / status”.
#
# The tests make sure that:
#   • Required directories and the sample CSV already exist.
#   • /home/user/output is completely empty (no stray files).
#   • transformation.pid and transformation_status.log do NOT yet exist.
#   • No process owned by the current user is already running with the
#     exact command line “sleep 180”.
#
# Only Python’s standard library and pytest are used.

import os
import stat
import getpass
import pytest

HOME = '/home/user'
DATA_DIR = os.path.join(HOME, 'data')
OUTPUT_DIR = os.path.join(HOME, 'output')
CSV_FILE = os.path.join(DATA_DIR, 'quarterly_sales.csv')
PID_FILE = os.path.join(OUTPUT_DIR, 'transformation.pid')
STATUS_FILE = os.path.join(OUTPUT_DIR, 'transformation_status.log')


def _mode_as_octal(path):
    """Return the permission bits of *path* as a zero-prefixed octal string."""
    return oct(stat.S_IMODE(os.lstat(path).st_mode)).replace('0o', '0')


def test_directories_exist_with_correct_permissions():
    # Directories must exist and be readable/executable by the user (0755).
    for d in (DATA_DIR, OUTPUT_DIR):
        assert os.path.isdir(d), f"Required directory {d!r} is missing."
        mode = _mode_as_octal(d)
        assert mode == '0755', (
            f"Directory {d!r} should have permissions 0755, found {mode}."
        )


def test_sample_csv_exists_and_is_readable():
    assert os.path.isfile(CSV_FILE), (
        f"Sample CSV file {CSV_FILE!r} is missing in the initial setup."
    )
    assert os.access(CSV_FILE, os.R_OK), (
        f"Sample CSV file {CSV_FILE!r} is not readable."
    )


def test_output_directory_is_initially_empty():
    contents = os.listdir(OUTPUT_DIR)
    assert contents == [] , (
        f"{OUTPUT_DIR!r} is expected to be empty at start-up, "
        f"but it already contains: {contents}"
    )


def test_transformation_files_do_not_exist_yet():
    for file_path in (PID_FILE, STATUS_FILE):
        assert not os.path.exists(file_path), (
            f"File {file_path!r} must NOT exist before the exercise starts."
        )


def test_no_sleep_180_process_owned_by_user_running():
    """
    Ensure the student hasn't pre-started a ‘sleep 180’ process.
    We only consider processes owned by the current UID.
    """
    current_uid = os.getuid()
    offending_pids = []

    proc_root = '/proc'
    # If /proc is not present (unlikely on a Linux grading box) we skip.
    if not os.path.isdir(proc_root):
        pytest.skip("/proc not present; skipping process check.")

    for pid in os.listdir(proc_root):
        if not pid.isdigit():
            continue
        proc_dir = os.path.join(proc_root, pid)
        status_file = os.path.join(proc_dir, 'status')
        cmdline_file = os.path.join(proc_dir, 'cmdline')

        try:
            with open(status_file, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    if line.startswith('Uid:'):
                        uid_field = int(line.split()[1])
                        break
                else:
                    continue  # No Uid line -> skip

            if uid_field != current_uid:
                continue  # Different user, ignore

            with open(cmdline_file, 'rb') as f:
                raw = f.read()
        except (FileNotFoundError, ProcessLookupError, PermissionError):
            # Process might have ended or be inaccessible; skip it.
            continue

        # cmdline is NUL-separated; decode and join with spaces
        cmdline = raw.replace(b'\x00', b' ').strip().decode(errors='ignore')
        if cmdline == 'sleep 180':
            offending_pids.append(pid)

    assert offending_pids == [], (
        "A ‘sleep 180’ process owned by the current user is already running "
        f"(PIDs: {', '.join(offending_pids)}). The initial state must not "
        "contain such a process."
    )