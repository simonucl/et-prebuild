# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system state
# before the student performs any action.
#
# The checks confirm the presence, type and permissions of the directory
# tree rooted at /home/user/app.  They also verify that the only
# world-writable regular file is /home/user/app/db.sqlite.
#
# IMPORTANT:  We intentionally do *not* test for the presence of the
#             eventual output file /home/user/world_writable_report.txt,
#             per the grading-suite specification.

import os
import stat
from pathlib import Path

APP_ROOT = Path("/home/user/app")
CONFIG_YML = APP_ROOT / "config.yml"
DB_SQLITE = APP_ROOT / "db.sqlite"
SCRIPT_SH = APP_ROOT / "script.sh"


def _is_world_writable(path: Path) -> bool:
    """
    Return True if the 'other write' bit (octal 0002) is set on the path.
    Only meaningful for regular files; callers should filter as needed.
    """
    return bool(path.stat().st_mode & stat.S_IWOTH)


def test_app_root_exists_and_is_directory():
    assert APP_ROOT.exists(), f"Required directory {APP_ROOT} is missing."
    assert APP_ROOT.is_dir(), f"{APP_ROOT} exists but is not a directory."

    # Mode should be 0755 (drwxr-xr-x).  Mask with 0o777 to ignore file type.
    mode = APP_ROOT.stat().st_mode & 0o777
    expected = 0o755
    assert (
        mode == expected
    ), f"{APP_ROOT} should have mode 0o{expected:03o} but is 0o{mode:03o}."


def test_required_files_exist_and_are_regular():
    for p in (CONFIG_YML, DB_SQLITE, SCRIPT_SH):
        assert p.exists(), f"Required file {p} is missing."
        assert p.is_file(), f"{p} exists but is not a regular file."


def test_individual_file_permissions():
    # config.yml — 0644 (rw-r--r--)
    mode_cfg = CONFIG_YML.stat().st_mode & 0o777
    assert (
        mode_cfg == 0o644
    ), f"{CONFIG_YML} should have mode 0o644 but is 0o{mode_cfg:03o}."
    assert not _is_world_writable(
        CONFIG_YML
    ), f"{CONFIG_YML} must NOT be world-writable."

    # db.sqlite — 0666 (rw-rw-rw-)  -> world-writable
    mode_db = DB_SQLITE.stat().st_mode & 0o777
    expected_db_mode = 0o666
    assert (
        mode_db == expected_db_mode
    ), f"{DB_SQLITE} should have mode 0o{expected_db_mode:03o} but is 0o{mode_db:03o}."
    assert _is_world_writable(
        DB_SQLITE
    ), f"{DB_SQLITE} is expected to be world-writable but is not."

    # script.sh — 0755 (rwxr-xr-x)
    mode_sh = SCRIPT_SH.stat().st_mode & 0o777
    expected_sh_mode = 0o755
    assert (
        mode_sh == expected_sh_mode
    ), f"{SCRIPT_SH} should have mode 0o{expected_sh_mode:03o} but is 0o{mode_sh:03o}."
    assert not _is_world_writable(
        SCRIPT_SH
    ), f"{SCRIPT_SH} must NOT be world-writable."


def test_only_one_world_writable_regular_file_under_app():
    """
    Recursively walk /home/user/app and ensure that exactly one regular file
    (db.sqlite) has the 'others write' permission bit set.
    """
    world_writable_files = []

    for dirpath, dirnames, filenames in os.walk(APP_ROOT):
        for name in filenames:
            path = Path(dirpath) / name
            try:
                st = path.stat(follow_symlinks=False)
            except FileNotFoundError:
                # File disappeared between walk and stat; treat as error.
                assert False, f"File {path} disappeared during walk."

            if stat.S_ISREG(st.st_mode) and (st.st_mode & stat.S_IWOTH):
                world_writable_files.append(path.resolve())

    # There must be exactly one world-writable regular file.
    assert (
        len(world_writable_files) == 1
    ), f"Expected exactly one world-writable regular file, found {len(world_writable_files)}: {world_writable_files}"

    # It must be /home/user/app/db.sqlite.
    expected_path = DB_SQLITE.resolve()
    found_path = world_writable_files[0]
    assert (
        found_path == expected_path
    ), f"World-writable file should be {expected_path}, but found {found_path!s}."