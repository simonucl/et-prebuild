# test_initial_state.py
#
# Pytest suite that validates the **initial** on-disk state _before_ the
# student’s command is executed.  It purposely does **not** look for the
# eventual output artefact (/home/user/workspace/world_writable_report.log).
#
# Only stdlib + pytest are used.

import os
import stat
from pathlib import Path

import pytest

HOME = Path("/home/user")
WS   = HOME / "workspace"


@pytest.mark.parametrize(
    "path, is_dir, expected_mode",
    [
        (WS,                                   True,  0o755),
        (WS / "confidential.txt",              False, 0o600),
        (WS / "public.log",                    False, 0o666),
        (WS / "script.sh",                     False, 0o755),
        (WS / "temp",                          True,  0o755),
        (WS / "temp" / "temp.db",              False, 0o664),
        (WS / "temp" / "world.sh",             False, 0o777),
    ],
)
def test_paths_exist_with_correct_type_and_mode(path, is_dir, expected_mode):
    """
    Ensure every required file/directory exist with the correct type and mode.
    """
    assert path.exists(), f"Expected path missing: {path}"
    if is_dir:
        assert path.is_dir(), f"{path} should be a directory"
    else:
        assert path.is_file(), f"{path} should be a regular file"

    # Compare permission bits (mask out file type bits).
    mode = stat.S_IMODE(os.stat(path).st_mode)
    assert (
        mode == expected_mode
    ), f"{path} has mode {oct(mode)}, expected {oct(expected_mode)}"


def test_confidential_txt_contents():
    """
    /home/user/workspace/confidential.txt must contain exactly 'TOP SECRET'
    with a trailing newline (one‐line file).
    """
    path = WS / "confidential.txt"
    with path.open("r", encoding="utf-8") as fh:
        data = fh.read().splitlines()
    assert data == ["TOP SECRET"], (
        f"{path} content mismatch. Expected a single line 'TOP SECRET', "
        f"got: {data}"
    )


@pytest.mark.parametrize(
    "path, expected_line_start",
    [
        (WS / "script.sh",             "#!/bin/sh"),
        (WS / "temp" / "world.sh",     "#!/bin/sh"),
    ],
)
def test_shell_scripts_have_shebang(path, expected_line_start):
    """
    The shell scripts should start with the expected shebang.
    """
    with path.open("r", encoding="utf-8") as fh:
        first_line = fh.readline().rstrip("\n")
    assert (
        first_line == expected_line_start
    ), f"{path} should start with '{expected_line_start}', found '{first_line}'"


def test_public_log_content():
    """
    public.log must contain the string 'public info' followed by a newline.
    """
    path = WS / "public.log"
    with path.open("r", encoding="utf-8") as fh:
        data = fh.read().splitlines()
    assert data == ["public info"], (
        f"{path} content mismatch. Expected a single line 'public info', "
        f"got: {data}"
    )


def test_temp_db_is_empty():
    """
    temp.db should be an empty (zero-byte) file.
    """
    path = WS / "temp" / "temp.db"
    size = path.stat().st_size
    assert size == 0, f"{path} should be empty (0 bytes), found {size} bytes"