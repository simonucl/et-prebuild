# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state before the student begins work on:
# “Generate an integrity-verification report by cutting and pasting specific
# columns”.
#
# It checks only the two pre-populated snapshot files that the tasks depend
# upon.  It deliberately does *not* check for any output paths such as
# /home/user/reports or the files that will be produced there.

import pathlib
import pytest

HOME = pathlib.Path("/home/user")
PRIMARY_FILE = HOME / "data" / "primary" / "data_snapshot_20230914.tsv"
BACKUP_FILE = HOME / "data" / "backup"  / "data_snapshot_20230914.tsv"

# --------------------------------------------------------------------------- #
# Helpers                                                                     #
# --------------------------------------------------------------------------- #
def read_tsv_lines(path: pathlib.Path):
    """
    Read a TSV file, return its lines (without trailing newlines).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        pytest.fail(f"Required file not found at {path}")
    except PermissionError:
        pytest.fail(f"Cannot read required file {path}: permission denied")
    return text.splitlines()


def assert_line_has_n_fields(line: str, n: int, path: pathlib.Path, line_no: int):
    """
    Assert that a TSV line contains exactly `n` tab-separated fields.
    """
    fields = line.split("\t")
    assert len(fields) == n, (
        f"{path} line {line_no} is expected to have {n} tab-separated fields, "
        f"but {len(fields)} were found: {line!r}"
    )
    return fields


# --------------------------------------------------------------------------- #
# Expected content                                                            #
# --------------------------------------------------------------------------- #
EXPECTED_HEADER = "id\tfilename\tsha256\tbytes\tmtime"

EXPECTED_PRIMARY_ROWS = [
    ("1", "img001.jpg",
     "d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2",
     "204800", "2023-09-14T08:30:00Z"),
    ("2", "document.pdf",
     "afafafafafafafafafafafafafafafafafafafafafafafafafafafafafafafaf",
     "102400", "2023-09-14T08:31:00Z"),
    ("3", "db_backup.sql.bz2",
     "bbb111bbb111bbb111bbb111bbb111bbb111bbb111bbb111bbb111bbb111bbb1",
     "512000", "2023-09-14T08:32:00Z"),
    ("4", "logs.tar.gz",
     "cccc222cccc222cccc222cccc222cccc222cccc222cccc222cccc222cccc222c",
     "307200", "2023-09-14T08:35:00Z"),
]

EXPECTED_BACKUP_ROWS = [
    ("1", "img001.jpg",
     "d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2",
     "204800", "2023-09-14T08:30:01Z"),
    ("2", "document.pdf",
     "afafafafafafafafafafafafafafafafafafafafafafafafafafafafafafafaf",
     "102400", "2023-09-14T08:31:03Z"),
    ("3", "db_backup.sql.bz2",
     "zzz333zzz333zzz333zzz333zzz333zzz333zzz333zzz333zzz333zzz333z",
     "512000", "2023-09-14T08:32:05Z"),
    ("4", "logs.tar.gz",
     "cccc222cccc222cccc222cccc222cccc222cccc222cccc222cccc222cccc222c",
     "307200", "2023-09-14T08:35:07Z"),
]


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "path,expected_rows",
    [
        (PRIMARY_FILE, EXPECTED_PRIMARY_ROWS),
        (BACKUP_FILE,  EXPECTED_BACKUP_ROWS),
    ],
)
def test_snapshot_file_exists_and_is_well_formed(path, expected_rows):
    """
    1. File must exist and be readable.
    2. Must contain exactly 5 lines (1 header + 4 data lines).
    3. Header must match the specification exactly.
    4. Each data line must have 5 tab-separated fields.
    5. Content of every field must match the pre-populated truth value.
    """
    lines = read_tsv_lines(path)

    # --- 1 & 2: line count -------------------------------------------------- #
    assert len(lines) == 5, (
        f"{path} should contain exactly 5 lines "
        f"(1 header + 4 rows) but has {len(lines)}."
    )

    # --- 3: header content -------------------------------------------------- #
    assert lines[0] == EXPECTED_HEADER, (
        f"{path} header line mismatch.\n"
        f"Expected: {EXPECTED_HEADER!r}\n"
        f"Found:    {lines[0]!r}"
    )

    # --- 4 & 5: data rows --------------------------------------------------- #
    for idx, (line, expected_tuple) in enumerate(zip(lines[1:], expected_rows), start=2):
        fields = assert_line_has_n_fields(line, 5, path, idx)
        assert tuple(fields) == expected_tuple, (
            f"{path} line {idx} content mismatch.\n"
            f"Expected fields: {expected_tuple}\n"
            f"Found fields:    {tuple(fields)}"
        )