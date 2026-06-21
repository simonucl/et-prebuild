# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem **before**
# the student performs any synchronisation work for the “configuration-manager”
# assignment.  These tests confirm that the initial trees under
# /home/user/config_manager/workdir  and  /home/user/remote_configs
# have the correct shape and file contents.
#
# IMPORTANT:
#   • We intentionally do NOT test for the presence (or absence) of the
#     post-task output artefacts such as `cache.conf` inside workdir or
#     the `sync_report.log`.  The checker will look at those later.
#   • Only the standard library + pytest are used.

import pathlib
import pytest

HOME = pathlib.Path("/home/user")
LOCAL_WORKDIR = HOME / "config_manager" / "workdir"
REMOTE_DIR = HOME / "remote_configs"


def _read(path: pathlib.Path) -> str:
    """Convenience helper – read a text file, return stripped contents."""
    return path.read_text(encoding="utf-8").strip()


# ---------- Directory existence ------------------------------------------------


def test_required_directories_exist():
    assert LOCAL_WORKDIR.is_dir(), (
        f"Expected directory {LOCAL_WORKDIR} is missing.\n"
        "Create it before running your synchronisation script."
    )
    assert REMOTE_DIR.is_dir(), (
        f"Remote directory {REMOTE_DIR} is missing.\n"
        "This should already be staged for you."
    )


# ---------- Local files --------------------------------------------------------


def test_local_app_conf_present_with_version_1_0():
    app_conf = LOCAL_WORKDIR / "app.conf"
    assert app_conf.is_file(), (
        f"Initial local file {app_conf} is missing. "
        "It must exist with version=1.0 before you start."
    )
    expected = "version=1.0"
    actual = _read(app_conf)
    assert actual == expected, (
        f"{app_conf} contents are incorrect.\n"
        f"Expected: {expected!r}\n"
        f"Got:      {actual!r}"
    )


def test_local_db_conf_present_with_expected_lines():
    db_conf = LOCAL_WORKDIR / "db.conf"
    assert db_conf.is_file(), (
        f"Initial local file {db_conf} is missing. "
        "It must contain database connection settings."
    )
    expected_lines = ["host=localhost", "port=5432"]
    actual_lines = _read(db_conf).splitlines()
    assert actual_lines == expected_lines, (
        f"{db_conf} contents are incorrect.\n"
        f"Expected lines: {expected_lines}\n"
        f"Got:            {actual_lines}"
    )


# ---------- Remote files -------------------------------------------------------


@pytest.mark.parametrize(
    "relative_path, expected_content",
    [
        ("app.conf", "version=1.1"),
        ("db.conf", "host=localhost\nport=5432"),
        ("cache.conf", "enabled=true"),
    ],
)
def test_remote_files_present_with_expected_content(relative_path, expected_content):
    """Ensure the staged 'remote' tree contains the authoritative files."""
    remote_file = REMOTE_DIR / relative_path
    assert remote_file.is_file(), (
        f"Remote file {remote_file} is missing; "
        "the assignment expects it to be present before synchronisation."
    )
    actual = _read(remote_file)
    assert actual == expected_content, (
        f"Content mismatch in remote file {remote_file}.\n"
        f"Expected:\n{expected_content!r}\n"
        f"Got:\n{actual!r}"
    )