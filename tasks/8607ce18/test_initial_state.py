# test_initial_state.py
#
# Pytest suite that validates the INITIAL filesystem state for the
# “netdiag” assignment *before* the student performs any actions.
#
# Rules (from the task description, paraphrased):
#   • Only the directories /home/user/netdiag/configs and
#     /home/user/netdiag/logs should exist under /home/user/netdiag.
#   • The configs directory must contain the two plain-text files
#       router.conf   and   switch.conf
#   • The logs directory must be empty.
#   • No other files, directories, or symbolic links are present.
#
# NOTE:  We deliberately do *not* test for the presence (or absence)
#        of any OUTPUT artifacts such as “live_configs/” or the audit
#        log, per the grading-harness rules.

import os
import stat
from pathlib import Path


HOME = Path("/home/user")
NETDIAG_ROOT = HOME / "netdiag"
CONFIGS_DIR = NETDIAG_ROOT / "configs"
LOGS_DIR = NETDIAG_ROOT / "logs"

ROUTER_CONF = CONFIGS_DIR / "router.conf"
SWITCH_CONF = CONFIGS_DIR / "switch.conf"


def _fmt_mode(path: Path) -> str:
    """Helper: return octal permission string (e.g. '0755')."""
    return oct(path.stat().st_mode & 0o777)


def test_expected_directories_exist_and_are_directories():
    assert NETDIAG_ROOT.exists(), (
        f"Expected directory {NETDIAG_ROOT} is missing."
    )
    assert NETDIAG_ROOT.is_dir(), (
        f"{NETDIAG_ROOT} exists but is not a directory."
    )

    for d in (CONFIGS_DIR, LOGS_DIR):
        assert d.exists(), f"Expected directory {d} is missing."
        assert d.is_dir(), f"{d} exists but is not a directory."

        # Directory permissions should be at least 0755 (not world-writable)
        mode = d.stat().st_mode
        is_world_writable = bool(mode & stat.S_IWOTH)
        assert not is_world_writable, (
            f"Directory {d} is world-writable (mode {_fmt_mode(d)}); "
            "it must not be."
        )


def test_only_expected_top_level_entries_exist():
    expected = {"configs", "logs"}
    actual = {p.name for p in NETDIAG_ROOT.iterdir()}
    unexpected = actual - expected
    missing = expected - actual

    assert not missing, (
        f"Missing expected entries in {NETDIAG_ROOT}: {sorted(missing)}"
    )
    assert not unexpected, (
        f"Unexpected entries found in {NETDIAG_ROOT}: {sorted(unexpected)}"
    )


def test_logs_directory_is_empty():
    contents = list(LOGS_DIR.iterdir())
    assert not contents, (
        f"Directory {LOGS_DIR} is expected to be empty but contains: "
        f"{[p.name for p in contents]}"
    )


def test_required_config_files_exist_and_are_plain_text():
    for cfg in (ROUTER_CONF, SWITCH_CONF):
        assert cfg.exists(), f"Required file {cfg} is missing."
        assert cfg.is_file(), f"{cfg} exists but is not a regular file."
        assert not cfg.is_symlink(), f"{cfg} should be a plain file, not a symlink."

        # Size sanity check: non-empty files
        assert cfg.stat().st_size > 0, f"{cfg} is empty."

    # Optional: lightweight content verification of the first line.
    with ROUTER_CONF.open("r", encoding="utf-8") as fh:
        first = fh.readline().strip()
        assert first.startswith("#"), (
            f"{ROUTER_CONF} should start with a comment line. "
            f"Found: {first!r}"
        )

    with SWITCH_CONF.open("r", encoding="utf-8") as fh:
        first = fh.readline().strip()
        assert first.startswith("#"), (
            f"{SWITCH_CONF} should start with a comment line. "
            f"Found: {first!r}"
        )