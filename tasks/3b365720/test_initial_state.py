# test_initial_state.py
#
# This test-suite verifies that the machine is in the expected “clean”
# state *before* the student performs any actions for the assignment
# “system-snapshot & CSV business summary”.
#
# It checks:
#   1. The bundled CSV dataset exists and has the correct basic statistics.
#   2. Neither of the two target log files already exists.
#   3. Essential Linux utilities that the student must use are available.
#
# Only Python stdlib + pytest are used.

import csv
import os
import pathlib
import shutil
import subprocess

import pytest


HOME = pathlib.Path("/home/user").expanduser().resolve()
DATASET = HOME / "data" / "transactions.csv"

# Target paths the student will create
DIAGNOSTICS_DIR = HOME / "diagnostics"
SNAPSHOT_FILE = DIAGNOSTICS_DIR / "system_snapshot.log"

ANALYSIS_DIR = HOME / "analysis"
SUMMARY_FILE = ANALYSIS_DIR / "transactions_summary.log"


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def cmd_exists(cmd: str) -> bool:
    """Return True iff `cmd` is resolvable in $PATH."""
    return shutil.which(cmd) is not None


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_dataset_presence_and_basic_stats():
    """Ensure the sample CSV exists, is readable and contains the expected stats."""
    # 1. File exists
    assert DATASET.is_file(), (
        f"Required dataset not found: {DATASET}. "
        "It must exist *before* the student script runs."
    )

    # 2. Read content
    with DATASET.open(newline="") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)

    # 3. Structure checks
    expected_fieldnames = ["transaction_id", "customer_id", "amount", "currency"]
    assert reader.fieldnames == expected_fieldnames, (
        f"CSV header mismatch.\nExpected: {expected_fieldnames}\n"
        f"Found   : {reader.fieldnames}"
    )

    # 4. Statistical expectations
    amounts = [int(r["amount"]) for r in rows]
    total_transactions = len(rows)
    total_amount = sum(amounts)
    average_amount = round(total_amount / total_transactions, 2) if amounts else None

    assert total_transactions == 5, (
        f"CSV should contain 5 data rows, found {total_transactions}."
    )
    assert total_amount == 875, (
        f"Sum of 'amount' column should be 875, found {total_amount}."
    )
    assert average_amount == 175.00, (
        f"Average amount should be 175.00, found {average_amount:.2f}."
    )


@pytest.mark.parametrize(
    "path_",
    [
        SNAPSHOT_FILE,
        SUMMARY_FILE,
    ],
)
def test_target_files_do_not_exist_yet(path_: pathlib.Path):
    """The log files must NOT exist before the student starts the task."""
    assert not path_.exists(), (
        f"File {path_} already exists, but the assignment requires the "
        "student to create it from scratch."
    )


@pytest.mark.parametrize(
    "cmd",
    ["date", "hostname", "uname", "free", "df"],
)
def test_required_commands_available(cmd):
    """The system must provide the basic Linux utilities the student will call."""
    assert cmd_exists(cmd), f"Required command '{cmd}' is not available in PATH."


def test_free_command_outputs_mem_line():
    """Sanity-check that `free -m | grep Mem` returns a line with at least two columns."""
    try:
        output = subprocess.check_output(["free", "-m"], text=True)
    except FileNotFoundError:
        pytest.skip("`free` command not present (checked in previous test).")

    mem_line = next((ln for ln in output.splitlines() if ln.lower().startswith("mem")), None)
    assert mem_line, "`free -m` did not produce a 'Mem' line."

    cols = mem_line.split()
    assert len(cols) >= 2 and cols[1].isdigit(), (
        "Unexpected format from `free -m`.\n"
        f"Line: {mem_line}\nExpected at least two columns with the second column "
        "being the total memory in MB."
    )


def test_df_home_user_outputs_expected_columns():
    """`df -h /home/user` should yield a line with at least five columns."""
    result = subprocess.check_output(["df", "-h", str(HOME)], text=True)
    lines = result.strip().splitlines()
    assert len(lines) >= 2, "`df -h /home/user` did not return the expected two lines."

    data_line = lines[-1]
    cols = data_line.split()
    assert len(cols) >= 5, (
        "Unexpected column count from `df -h /home/user`.\n"
        f"Line: {data_line}"
    )
    used_pct = cols[4].rstrip("%")
    assert used_pct.isdigit(), (
        "The 5th column of `df -h /home/user` should be a percentage like '37%'.\n"
        f"Found: {cols[4]}"
    )