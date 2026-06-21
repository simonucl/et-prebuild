# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the operating system
# BEFORE the student starts working on the “pkgdb” ticket-processing task.
#
# What we expect to be present right now:
#   • /home/user/tickets/ticket_queue.csv    — containing the 5 exact lines
#   • /home/user/pkgdb/alpha-1.0.0           — empty directory
#   • /home/user/pkgdb/beta-2.3.4            — empty directory
#   • /home/user/pkgdb/gamma-0.9.8           — empty directory
#
# What must *not* be present yet:
#   • /home/user/tickets/resolution_log.csv
#   • Any other directories under /home/user/pkgdb/
#
# If any of these expectations are violated, the test suite will fail with an
# explanatory message.

import pathlib
import csv
import pytest

HOME = pathlib.Path("/home/user")
PKGDB_DIR = HOME / "pkgdb"
TICKETS_DIR = HOME / "tickets"

# --------------------------------------------------------------------------- #
# Helper utilities                                                            #
# --------------------------------------------------------------------------- #

def read_csv_as_rows(csv_path):
    """Return the list of raw rows (strings) from a CSV file, preserving LF."""
    with csv_path.open("r", encoding="utf-8", newline="") as fp:
        return fp.read().splitlines()


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #

def test_ticket_queue_exists_with_expected_content():
    """
    Ensure the ticket queue CSV exists *and* has exactly the five required lines.
    """
    csv_path = TICKETS_DIR / "ticket_queue.csv"
    assert csv_path.exists(), (
        f"Expected ticket queue file '{csv_path}' is missing."
    )
    assert csv_path.is_file(), (
        f"Path '{csv_path}' exists but is not a regular file."
    )

    expected_lines = [
        "TicketID,Package,RequiredVersion,Action",
        "101,alpha,1.2.0,upgrade",
        "102,beta,N/A,remove",
        "103,delta,4.5.6,install",
        "104,gamma,0.9.0,downgrade",
    ]

    actual_lines = read_csv_as_rows(csv_path)
    assert actual_lines == expected_lines, (
        "ticket_queue.csv content does not match expected lines.\n\n"
        f"Expected ({len(expected_lines)} lines):\n{expected_lines}\n\n"
        f"Found ({len(actual_lines)} lines):\n{actual_lines}"
    )


def test_pkgdb_contains_only_expected_initial_directories():
    """
    Verify that /home/user/pkgdb/ exists and contains exactly the three
    expected version-directories, each empty.
    """
    assert PKGDB_DIR.exists(), (
        f"Required directory '{PKGDB_DIR}' is missing."
    )
    assert PKGDB_DIR.is_dir(), (
        f"Path '{PKGDB_DIR}' exists but is not a directory."
    )

    expected_dirs = {
        "alpha-1.0.0",
        "beta-2.3.4",
        "gamma-0.9.8",
    }

    actual_entries = {p.name for p in PKGDB_DIR.iterdir() if p.is_dir()}
    missing = expected_dirs - actual_entries
    extra = actual_entries - expected_dirs

    assert not missing, (
        f"The following expected directories are missing from {PKGDB_DIR}: "
        f"{', '.join(sorted(missing))}"
    )
    assert not extra, (
        f"The following unexpected directories are present in {PKGDB_DIR}: "
        f"{', '.join(sorted(extra))}"
    )

    # Ensure each expected directory is empty.
    for dirname in expected_dirs:
        dirpath = PKGDB_DIR / dirname
        assert dirpath.is_dir(), (
            f"Expected directory '{dirpath}' is not present or not a directory."
        )
        contents = list(dirpath.iterdir())
        assert not contents, (
            f"Directory '{dirpath}' is expected to be empty but contains: "
            f"{', '.join(p.name for p in contents)}"
        )


def test_resolution_log_not_yet_created():
    """
    The student has not yet processed the tickets, so the resolution log
    must *not* exist at this point.
    """
    log_path = TICKETS_DIR / "resolution_log.csv"
    assert not log_path.exists(), (
        f"Resolution log '{log_path}' should NOT exist before any processing."
    )