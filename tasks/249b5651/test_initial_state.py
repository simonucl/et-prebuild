# test_initial_state.py
#
# Pytest suite that verifies the *initial* state of the operating system /
# filesystem for the “cicd_db_work” task **before** the student’s solution
# is graded.
#
# Only the Python standard library and pytest are used.

import os
import sqlite3
import re
import csv
import io
import pytest

BASE_DIR = "/home/user/cicd_db_work"
DB_PATH = os.path.join(BASE_DIR, "ci_cd_metrics.db")
AVG_PATH = os.path.join(BASE_DIR, "build_time_average.txt")
CSV_EXPORT_PATH = os.path.join(BASE_DIR, "metrics_export.csv")
SQL_AUDIT_PATH = os.path.join(BASE_DIR, "cicd_sql_audit.log")

# ---------------------------------------------------------------------------
# Ground-truth values that the student’s artefacts must contain.
# ---------------------------------------------------------------------------
EXPECTED_ROWS = [
    (1, "web-frontend",        "success", 420, "2023-09-01"),
    (2, "api-service",         "failed",  370, "2023-09-01"),
    (3, "database-migrations", "success", 255, "2023-09-02"),
]

EXPECTED_AVG = 348.33  # Rounded to two decimals from the build_time_seconds column.

EXPECTED_CSV_LINES = [
    "id,pipeline_name,status,build_time_seconds,build_date\n",
    "1,web-frontend,success,420,2023-09-01\n",
    "2,api-service,failed,370,2023-09-01\n",
    "3,database-migrations,success,255,2023-09-02\n",
]

REQUIRED_SQL_STATEMENTS = {
    "CREATE TABLE build_metrics (id INTEGER PRIMARY KEY, pipeline_name TEXT NOT NULL, status TEXT CHECK(status IN ('success','failed')) NOT NULL, build_time_seconds INTEGER NOT NULL, build_date DATE NOT NULL);",
    "INSERT INTO build_metrics (id, pipeline_name, status, build_time_seconds, build_date) VALUES (1,'web-frontend','success',420,'2023-09-01');",
    "INSERT INTO build_metrics (id, pipeline_name, status, build_time_seconds, build_date) VALUES (2,'api-service','failed',370,'2023-09-01');",
    "INSERT INTO build_metrics (id, pipeline_name, status, build_time_seconds, build_date) VALUES (3,'database-migrations','success',255,'2023-09-02');",
}

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def _connect_db():
    """Return a connection to the SQLite DB, raising pytest failure if it cannot be opened."""
    try:
        return sqlite3.connect(DB_PATH)
    except sqlite3.Error as exc:
        pytest.fail(f"Unable to open SQLite file at {DB_PATH}: {exc}")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_directory_exists():
    assert os.path.isdir(
        BASE_DIR
    ), f"Required directory {BASE_DIR} does not exist."


def test_db_file_exists():
    assert os.path.isfile(
        DB_PATH
    ), f"SQLite database file {DB_PATH} is missing."


def test_db_integrity_and_schema():
    con = _connect_db()
    try:
        # 1. Integrity check
        integrity, = con.execute("PRAGMA integrity_check;").fetchone()
        assert integrity == "ok", f"SQLite integrity_check failed: {integrity}"

        # 2. Schema check — verify exact column names / order
        pragma_info = con.execute("PRAGMA table_info(build_metrics);").fetchall()
        expected_cols = [
            (0, "id", "INTEGER", 0, None, 1),
            (1, "pipeline_name", "TEXT", 1, None, 0),
            (2, "status", "TEXT", 1, None, 0),
            (3, "build_time_seconds", "INTEGER", 1, None, 0),
            (4, "build_date", "DATE", 1, None, 0),
        ]
        assert (
            pragma_info == expected_cols
        ), (
            "The schema of build_metrics does not match the specification.\n"
            f"Expected PRAGMA table_info:\n{expected_cols}\nGot:\n{pragma_info}"
        )

        # 3. CHECK constraint on status column
        create_sql, = con.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name='build_metrics';"
        ).fetchone()
        normalized_sql = re.sub(r"\s+", " ", create_sql.strip()).lower()
        expected_check_fragment = "check(status in ('success','failed'))"
        assert (
            expected_check_fragment in normalized_sql
        ), "Missing or malformed CHECK constraint on 'status' column."
    finally:
        con.close()


def test_seed_data():
    con = _connect_db()
    try:
        rows = con.execute(
            "SELECT id, pipeline_name, status, build_time_seconds, build_date "
            "FROM build_metrics ORDER BY id;"
        ).fetchall()
        assert rows == EXPECTED_ROWS, (
            "Seed data inside build_metrics does not match the expected rows.\n"
            f"Expected:\n{EXPECTED_ROWS}\nGot:\n{rows}"
        )
    finally:
        con.close()


def test_average_file():
    assert os.path.isfile(
        AVG_PATH
    ), f"Average file {AVG_PATH} is missing."

    with open(AVG_PATH, "r", encoding="utf-8") as fp:
        content = fp.read()

    # Must end with exactly one trailing newline
    assert content.endswith(
        "\n"
    ), "average_build_time_seconds file must end with a single newline (\\n)."

    # Strip the final newline for further checks
    content_line = content[:-1]

    pattern = r"^average_build_time_seconds:([0-9]+\.[0-9]{2})$"
    match = re.match(pattern, content_line)
    assert match, (
        "average_build_time_seconds file content must match the pattern "
        "'average_build_time_seconds:<value_with_two_decimals>'. "
        f"Got: {content_line}"
    )

    value_str = match.group(1)
    assert float(value_str) == EXPECTED_AVG, (
        f"Average value inside {AVG_PATH} is {value_str} but expected {EXPECTED_AVG:.2f}."
    )


def test_metrics_export_csv():
    assert os.path.isfile(
        CSV_EXPORT_PATH
    ), f"CSV export file {CSV_EXPORT_PATH} is missing."

    with open(CSV_EXPORT_PATH, "r", encoding="utf-8") as fp:
        lines = fp.readlines()

    assert lines == EXPECTED_CSV_LINES, (
        "metrics_export.csv content does not match expected output.\n"
        f"Expected lines:\n{EXPECTED_CSV_LINES}\nGot:\n{lines}"
    )

    # Additional structural CSV validation using csv module (no quotes expected)
    csv_content = "".join(lines)
    reader = csv.reader(io.StringIO(csv_content))
    parsed = list(reader)
    header, *data_rows = parsed

    assert header == [
        "id",
        "pipeline_name",
        "status",
        "build_time_seconds",
        "build_date",
    ], f"CSV header row is incorrect: {header}"

    # Convert numeric fields back to int for comparison
    parsed_rows = [
        (int(r[0]), r[1], r[2], int(r[3]), r[4]) for r in data_rows
    ]
    assert parsed_rows == EXPECTED_ROWS, (
        "Data rows in metrics_export.csv do not match the database rows.\n"
        f"Expected: {EXPECTED_ROWS}\nGot: {parsed_rows}"
    )


def test_sql_audit_log():
    assert os.path.isfile(
        SQL_AUDIT_PATH
    ), f"SQL audit log {SQL_AUDIT_PATH} is missing."

    with open(SQL_AUDIT_PATH, "r", encoding="utf-8") as fp:
        lines = fp.readlines()

    # 1. Each line must end with ';\n' and have no leading/trailing spaces.
    for idx, line in enumerate(lines, start=1):
        assert line.endswith(
            ";\n"
        ), f"Line {idx} of {SQL_AUDIT_PATH} must end with a single semicolon followed by newline."
        stripped = line.rstrip("\n")
        assert stripped == stripped.strip(), (
            f"Line {idx} of {SQL_AUDIT_PATH} has leading or trailing spaces: {repr(line)}"
        )

    # 2. Ensure all required SQL statements are present (order not enforced)
    stripped_lines = {ln.rstrip("\n") for ln in lines}
    missing = REQUIRED_SQL_STATEMENTS - stripped_lines
    assert not missing, (
        f"The following required SQL statements are missing from {SQL_AUDIT_PATH}:\n"
        + "\n".join(missing)
    )