# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state that must be
# present before the learner begins the task.  It deliberately checks ONLY
# the provided sample resources and never looks for (or at) any output that
# the learner is expected to create later.

import hashlib
from pathlib import Path

import pytest

HOME = Path("/home/user")
SAMPLE_DIR = HOME / "sample_queries"
ORDERS_SQL = SAMPLE_DIR / "orders.sql"
INVENTORY_SQL = SAMPLE_DIR / "inventory.sql"

ORDERS_SQL_CONTENT = "SELECT * FROM orders WHERE order_date > '2023-01-01';\n"
INVENTORY_SQL_CONTENT = "SELECT * FROM inventory WHERE quantity < 10;\n"


def sha256_of_file(path: Path) -> str:
    """Return the hex‐digest SHA-256 of the given file."""
    h = hashlib.sha256()
    with path.open("rb") as fp:
        for chunk in iter(lambda: fp.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


@pytest.fixture(scope="module")
def sample_dir_contents():
    """Return a sorted list of entries (files & dirs) directly under SAMPLE_DIR."""
    if not SAMPLE_DIR.exists():
        pytest.skip(f"{SAMPLE_DIR} is missing; skipping further tests.")
    return sorted(p.name for p in SAMPLE_DIR.iterdir())


def test_sample_queries_directory_exists():
    assert SAMPLE_DIR.is_dir(), (
        "Expected the directory "
        f"{SAMPLE_DIR} to exist but it is missing or not a directory."
    )


def test_sample_queries_contains_exactly_two_files(sample_dir_contents):
    expected_files = {"orders.sql", "inventory.sql"}
    actual_files = {name for name in sample_dir_contents if not name.startswith(".")}

    missing = expected_files - actual_files
    unexpected = actual_files - expected_files

    assert not missing, (
        "The following required files are missing from "
        f"{SAMPLE_DIR}: {', '.join(sorted(missing))}"
    )
    assert not unexpected, (
        "Found unexpected files in "
        f"{SAMPLE_DIR}: {', '.join(sorted(unexpected))}. "
        "The directory should contain *only* orders.sql and inventory.sql."
    )


@pytest.mark.parametrize(
    "file_path, expected_content",
    [
        (ORDERS_SQL, ORDERS_SQL_CONTENT),
        (INVENTORY_SQL, INVENTORY_SQL_CONTENT),
    ],
)
def test_sql_file_content_and_line_count(file_path: Path, expected_content: str):
    assert file_path.is_file(), f"Expected file {file_path} does not exist."

    with file_path.open("r", encoding="utf-8") as fh:
        lines = fh.readlines()

    # Ensure single-line file with exact content including LF newline.
    assert (
        len(lines) == 1
    ), f"{file_path} should contain exactly 1 line, found {len(lines)} lines."
    assert (
        lines[0] == expected_content
    ), f"Content of {file_path} does not match the expected SQL statement."


def test_sql_files_are_distinct(sample_dir_contents):
    """Sanity-check that the two SQL files are not identical."""
    orders_hash = sha256_of_file(ORDERS_SQL)
    inventory_hash = sha256_of_file(INVENTORY_SQL)
    assert orders_hash != inventory_hash, (
        "orders.sql and inventory.sql have identical contents, "
        "which should not be the case."
    )