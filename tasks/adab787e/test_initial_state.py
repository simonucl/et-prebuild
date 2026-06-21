# test_initial_state.py
"""
pytest validation of the **initial** operating-system / filesystem state
BEFORE the student performs the ETL assignment.

The tests intentionally fail if any part of the expected clean slate is
missing *or* if artefacts from a previous (or incorrect) run are already
present.

Only the Python standard library and pytest are used.
"""

from pathlib import Path
import pytest

# --- CONSTANTS ---------------------------------------------------------------

HOME = Path("/home/user")

RAW_DATA_DIR = HOME / "raw_data"

RAW_CUSTOMERS = RAW_DATA_DIR / "customers.csv"
RAW_ORDERS = RAW_DATA_DIR / "orders.csv"
RAW_PRODUCTS = RAW_DATA_DIR / "products.csv"

ETL_ARCHIVES_DIR = HOME / "etl_archives"
ETL_STAGING_DIR = HOME / "etl_staging"
ETL_NEW_LOAD_DIR = ETL_STAGING_DIR / "new_load"
ETL_LOGS_DIR = HOME / "etl_logs"

TARBALL = ETL_ARCHIVES_DIR / "data_dump_2023_01_15.tar.gz"
LOG_FILE = ETL_LOGS_DIR / "2023_01_15_compression.log"


# --- HELPER ------------------------------------------------------------------

def read_text(path: Path) -> str:
    """Return UTF-8 text, failing with a helpful message if not readable."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        pytest.fail(f"Required file missing: {path}", pytrace=False)  # pragma: no cover
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {path}: {exc}", pytrace=False)


# --- TESTS -------------------------------------------------------------------

def test_raw_data_directory_exists():
    assert RAW_DATA_DIR.is_dir(), (
        f"Directory {RAW_DATA_DIR} is expected to exist before the task starts."
    )


@pytest.mark.parametrize(
    "path,expected_lines,expected_content",
    [
        (
            RAW_CUSTOMERS,
            3,
            "customer_id,customer_name\n"
            "1,John Doe\n"
            "2,Jane Doe\n",
        ),
        (
            RAW_ORDERS,
            4,
            "order_id,customer_id,amount\n"
            "1001,1,250.50\n"
            "1002,2,450.00\n"
            "1003,1,125.75\n",
        ),
        (
            RAW_PRODUCTS,
            3,
            "product_id,product_name\n"
            "2001,Widget\n"
            "2002,Gadget\n",
        ),
    ],
)
def test_raw_csv_files(path: Path, expected_lines: int, expected_content: str):
    assert path.is_file(), f"Required CSV file is missing: {path}"

    text = read_text(path)
    actual_lines = text.count("\n")
    assert actual_lines == expected_lines, (
        f"{path} should have {expected_lines} lines including header; "
        f"found {actual_lines}."
    )

    assert text == expected_content, (
        f"Unexpected contents in {path}. Ensure the file has exactly:\n"
        f"{expected_content!r}\n\nFound:\n{text!r}"
    )


def test_no_extra_csv_files():
    """Verify that only the three expected CSVs exist in the raw_data directory."""
    csv_files = sorted(p.name for p in RAW_DATA_DIR.glob("*.csv"))
    expected = sorted([RAW_CUSTOMERS.name, RAW_ORDERS.name, RAW_PRODUCTS.name])
    assert csv_files == expected, (
        f"raw_data directory should contain only {expected}, "
        f"but actually contains {csv_files}."
    )


@pytest.mark.parametrize(
    "path_description,path_object",
    [
        ("ETL archives directory", ETL_ARCHIVES_DIR),
        ("ETL staging directory", ETL_STAGING_DIR),
        ("ETL staging/new_load directory", ETL_NEW_LOAD_DIR),
        ("ETL logs directory", ETL_LOGS_DIR),
    ],
)
def test_etl_target_directories_do_not_exist_yet(path_description, path_object: Path):
    assert not path_object.exists(), (
        f"{path_description} ({path_object}) should NOT exist before the student "
        f"runs their commands."
    )


def test_tarball_and_logfile_do_not_exist_yet():
    assert not TARBALL.exists(), (
        f"Tarball {TARBALL} must not exist before the student creates it."
    )
    assert not LOG_FILE.exists(), (
        f"Log file {LOG_FILE} must not exist before the student creates it."
    )