# test_initial_state.py
#
# This test-suite validates the **initial** state of the operating system
# *before* the student runs their solution.  It makes sure that:
#
#   • The directory /home/user/backups exists and contains the fourteen
#     nightly CSV files that the assignment depends on.
#   • The nightly CSV files have the correct headers, data lines,
#     line-counts, trailing newlines, and filenames.
#   • No deliverables under /home/user/reports exist yet
#     (so the student really has to create them).
#
# Only the Python standard library and pytest are used.

from pathlib import Path
import pytest

BACKUPS_DIR = Path("/home/user/backups")
REPORTS_DIR = Path("/home/user/reports")

# --------------------------------------------------------------------------- #
# Expected backup metadata (date-keyed so we can build expectations programmatically)
# --------------------------------------------------------------------------- #
DATE_INFO = {
    "20230618": dict(tables="83",  size="1225", duration="17m50s",
                     start="00:15:10", end="00:37:01", status="SUCCESS"),
    "20230619": dict(tables="84",  size="1230", duration="18m02s",
                     start="00:15:15", end="00:37:10", status="SUCCESS"),
    "20230620": dict(tables="85",  size="1240", duration="18m15s",
                     start="00:15:18", end="00:37:20", status="SUCCESS"),
    "20230621": dict(tables="86",  size="1248", duration="18m18s",
                     start="00:15:20", end="00:37:25", status="SUCCESS"),
    "20230622": dict(tables="85",  size="1245", duration="18m19s",
                     start="00:15:22", end="00:37:30", status="SUCCESS"),
    "20230623": dict(tables="85",  size="1249", duration="18m20s",
                     start="00:15:24", end="00:37:35", status="SUCCESS"),
    "20230624": dict(tables="85",  size="1250", duration="18m23s",
                     start="00:15:26", end="00:37:45", status="SUCCESS"),
}

PRIMARY_HEADER  = "Date,Hostname,Tables_Backup,Size_MB,Duration"
REPLICA_HEADER  = "Date,Hostname,Copy_Start,Copy_End,Status"
PRIMARY_PREFIX  = "primary_backup_"
REPLICA_PREFIX  = "replica_backup_"

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def build_primary_line(date_key, info):
    """Return the *exact* data line expected in a primary_*.csv file."""
    date_fmt = f"{date_key[:4]}-{date_key[4:6]}-{date_key[6:]}"
    return f"{date_fmt},primary-db,{info['tables']},{info['size']},{info['duration']}"

def build_replica_line(date_key, info):
    """Return the *exact* data line expected in a replica_*.csv file."""
    date_fmt = f"{date_key[:4]}-{date_key[4:6]}-{date_key[6:]}"
    return f"{date_fmt},replica-db,{info['start']},{info['end']},{info['status']}"

def collect_expected_filenames():
    """Return a list with the fourteen filenames we expect inside BACKUPS_DIR."""
    names = []
    for date_key in DATE_INFO:
        names.append(f"{PRIMARY_PREFIX}{date_key}.csv")
        names.append(f"{REPLICA_PREFIX}{date_key}.csv")
    return sorted(names)  # alphabetical for nicer diff messages

# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_backups_directory_present():
    assert BACKUPS_DIR.is_dir(), (
        f"Required directory {BACKUPS_DIR} is missing. "
        "It should contain the nightly CSV backups."
    )

def test_expected_backup_files_exist():
    expected_files = collect_expected_filenames()
    missing = [name for name in expected_files
               if not (BACKUPS_DIR / name).is_file()]
    assert not missing, (
        "The following expected backup CSV files are missing under "
        f"{BACKUPS_DIR}:\n  " + "\n  ".join(missing)
    )

def test_backup_file_contents_and_structure():
    """
    Every CSV file must:
      • be UTF-8 text
      • end with exactly one '\n'
      • contain exactly two lines (header + one data line)
      • have the correct header
      • have the correct data line
    """
    # Build dictionaries keyed by filename -> expected (header, data_line)
    expectations = {}
    for date_key, info in DATE_INFO.items():
        expectations[f"{PRIMARY_PREFIX}{date_key}.csv"] = (
            PRIMARY_HEADER,
            build_primary_line(date_key, info),
        )
        expectations[f"{REPLICA_PREFIX}{date_key}.csv"] = (
            REPLICA_HEADER,
            build_replica_line(date_key, info),
        )

    # Validate each file
    for filename, (expected_header, expected_data_line) in expectations.items():
        path = BACKUPS_DIR / filename
        assert path.is_file(), f"File {path} is unexpectedly missing."

        # Read as binary to check trailing newline; decode afterwards
        raw = path.read_bytes()
        assert raw.endswith(b"\n"), (
            f"File {path} must end with exactly one UNIX newline '\\n'."
        )

        # Splitlines without keeping '\n' so we can count logical lines
        lines = raw.decode("utf-8").splitlines()
        assert len(lines) == 2, (
            f"File {path} should have exactly 2 lines "
            f"(found {len(lines)} lines)."
        )

        header, data_line = lines
        assert header == expected_header, (
            f"Header mismatch in {path}.\n"
            f"Expected: {expected_header!r}\n"
            f"Found:    {header!r}"
        )
        assert data_line == expected_data_line, (
            f"Data line mismatch in {path}.\n"
            f"Expected: {expected_data_line!r}\n"
            f"Found:    {data_line!r}"
        )

def test_reports_not_yet_generated():
    """
    Nothing under /home/user/reports should exist yet.
    The directory may or may not be present, but the final deliverables
    certainly must NOT pre-exist.
    """
    report_csv = REPORTS_DIR / "weekly_backup_status_20230618-20230624.csv"
    log_file   = REPORTS_DIR / "weekly_backup_status_generation.log"

    assert not report_csv.exists(), (
        f"Report '{report_csv}' already exists. "
        "The student task is expected to create it."
    )
    assert not log_file.exists(), (
        f"Log file '{log_file}' already exists. "
        "The student task is expected to create it."
    )