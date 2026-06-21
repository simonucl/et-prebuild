# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state for the
# “CI/CD diagnostics” exercise.  These tests run *before* the student
# performs any actions and confirm that the required input material is
# present and correct.  No assertions are made about the output files
# that the student will create later.

import pathlib
import textwrap
import pytest

HOME = pathlib.Path("/home/user")
RAW_DIR = HOME / "ci_cd_diagnostics" / "raw"
SNAPSHOT = RAW_DIR / "snapshot.txt"


def read_snapshot_lines():
    try:
        return SNAPSHOT.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:   # pragma: no cover
        return []


def test_raw_directory_exists():
    """
    The raw diagnostics directory must exist *before* the exercise starts.
    """
    assert RAW_DIR.exists(), (
        f"Required directory missing: {RAW_DIR}\n"
        "Create it with:  mkdir -p /home/user/ci_cd_diagnostics/raw/"
    )
    assert RAW_DIR.is_dir(), f"{RAW_DIR} exists but is not a directory."


def test_snapshot_file_exists():
    """
    The static file snapshot.txt must be present so that students can read it.
    """
    assert SNAPSHOT.exists(), (
        f"Required file missing: {SNAPSHOT}\n"
        "Ensure the fixture that provides the snapshot data is in place."
    )
    assert SNAPSHOT.is_file(), f"{SNAPSHOT} exists but is not a regular file."


def test_snapshot_file_has_two_blocks_and_required_keys():
    """
    Validate that snapshot.txt contains exactly two blocks separated by
    a single blank line, and that each block has the keys required for
    the downstream computations.
    """
    lines = read_snapshot_lines()
    assert lines, f"{SNAPSHOT} is empty."

    # Split on blank lines to obtain the two blocks.
    blocks = []
    current = []
    for line in lines:
        if line.strip() == "":
            if current:
                blocks.append(current)
                current = []
        else:
            current.append(line.rstrip("\n"))
    if current:
        blocks.append(current)

    assert len(blocks) == 2, (
        f"{SNAPSHOT} must contain exactly two blocks separated by one blank line; "
        f"found {len(blocks)}."
    )

    required_keys = {
        "CPU_USER",
        "DISK_ROOT_USED_PCT",
        "DISK_VAR_USED_PCT",
        "DISK_HOME_USED_PCT",
        "NET_RX_KBPS",
        "NET_TX_KBPS",
    }

    for idx, block in enumerate(blocks, start=1):
        keys_in_block = {line.split("=", 1)[0] for line in block}
        missing = required_keys - keys_in_block
        assert not missing, (
            f"Block #{idx} in {SNAPSHOT} is missing required keys: {', '.join(sorted(missing))}"
        )


def _parse_block(block):
    """
    Helper: convert KEY=VALUE lines into a dict with numeric values where possible.
    """
    data = {}
    for line in block:
        key, value = line.split("=", 1)
        try:
            data[key] = float(value)
        except ValueError:
            data[key] = value
    return data


def test_computed_metrics_match_expected_truth():
    """
    Re-compute the expected metrics from snapshot.txt and compare them
    against the hard-coded truth values.  This guarantees the fixture
    content is exactly the one described in the exercise text.
    """
    truth_avg_cpu_user = 14.15
    truth_peak_disk_usage = 70  # percentage, no %
    truth_total_net_kbps = 480.4

    lines = read_snapshot_lines()
    # Reuse the splitting logic from the previous test without duplicating code.
    blocks = []
    current = []
    for line in lines:
        if line.strip() == "":
            if current:
                blocks.append(current)
                current = []
        else:
            current.append(line.rstrip("\n"))
    if current:
        blocks.append(current)

    # Parse both blocks into dicts.
    d1, d2 = map(_parse_block, blocks)

    # AVG_CPU_USER
    avg_cpu_user = round((d1["CPU_USER"] + d2["CPU_USER"]) / 2, 2)
    assert avg_cpu_user == truth_avg_cpu_user, (
        f"AVG_CPU_USER computed from {SNAPSHOT} is {avg_cpu_user}, "
        f"but the exercise expects {truth_avg_cpu_user}.  "
        "Ensure snapshot.txt matches the specification."
    )

    # PEAK_DISK_USAGE
    disks = (
        d1["DISK_ROOT_USED_PCT"],
        d1["DISK_VAR_USED_PCT"],
        d1["DISK_HOME_USED_PCT"],
        d2["DISK_ROOT_USED_PCT"],
        d2["DISK_VAR_USED_PCT"],
        d2["DISK_HOME_USED_PCT"],
    )
    peak_disk_usage = int(max(disks))
    assert peak_disk_usage == truth_peak_disk_usage, (
        f"PEAK_DISK_USAGE computed from {SNAPSHOT} is {peak_disk_usage}%, "
        f"but the exercise expects {truth_peak_disk_usage}%."
    )

    # TOTAL_NET_TRAFFIC_KBPS
    total_net = round(
        d1["NET_RX_KBPS"] + d1["NET_TX_KBPS"] + d2["NET_RX_KBPS"] + d2["NET_TX_KBPS"],
        1,
    )
    assert total_net == truth_total_net_kbps, (
        f"TOTAL_NET_TRAFFIC_KBPS computed from {SNAPSHOT} is {total_net}, "
        f"but the exercise expects {truth_total_net_kbps}."
    )