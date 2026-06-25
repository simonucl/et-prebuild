#!/bin/bash
set -u

mkdir -p /logs/verifier
reward=0
APP_ROOT="${APP_ROOT:-/app}"

if APP_ROOT="$APP_ROOT" python3 - <<'PY'
import csv
import hashlib
import json
import sqlite3
import sys
from pathlib import Path

root = Path(__import__("os").environ.get("APP_ROOT", "/app"))
db_path = root / "out" / "acme-ledger.sqlite"
csv_path = root / "out" / "merchant_daily_net.csv"

expected_raw_hashes = {
    "gateway_alpha.csv": "1c55e3c7036eac6cebc66e7a82a745476d7016cc55c73efc83e1c557efe8293c",
    "gateway_beta.csv": "25fd560d7dae45f727eb7a61c8102f22be0680a68c5084b8637d3a893016a46c",
}

expected_payments = [
    ("pay_1001", "Northwind", 125040, "USD", "settled", "2026-06-01T14:15:00Z", "2026-06-01T14:20:00Z", "gateway_alpha.csv", 2, 125040),
    ("pay_1002", "Northwind", 1599, "USD", "refunded", "2026-06-02T09:30:00Z", "2026-06-02T09:35:00Z", "gateway_beta.csv", 6, -1599),
    ("pay_1003", "Contoso", 7310, "EUR", "settled", "2026-06-02T12:45:00Z", "2026-06-02T12:50:00Z", "gateway_beta.csv", 2, 7310),
    ("pay_1004", "Contoso", 1800, "USD", "failed", "2026-06-02T13:00:00Z", None, "gateway_alpha.csv", 5, 0),
    ("pay_1005", "Northwind", 1000, "USD", "settled", "2026-06-03T10:00:00Z", "2026-06-03T10:01:00Z", "gateway_alpha.csv", 6, 1000),
    ("pay_1006", "Tailspin", 250000, "USD", "settled", "2026-06-03T08:00:00Z", "2026-06-03T08:05:00Z", "gateway_beta.csv", 3, 250000),
    ("pay_1008", "Northwind", 350, "USD", "refunded", "2026-06-03T12:00:00Z", None, "gateway_beta.csv", 5, -350),
]

expected_errors = [
    ("gateway_alpha.csv", 7, "", "blank payment_id"),
    ("gateway_beta.csv", 4, "pay_1007", "unsupported currency"),
]

expected_summary_rows = [
    ["2026-06-01", "Northwind", "USD", "125040", "1"],
    ["2026-06-02", "Contoso", "EUR", "7310", "1"],
    ["2026-06-02", "Contoso", "USD", "0", "1"],
    ["2026-06-02", "Northwind", "USD", "-1599", "1"],
    ["2026-06-03", "Northwind", "USD", "650", "2"],
    ["2026-06-03", "Tailspin", "USD", "250000", "1"],
]

def fail(message):
    print(f"FAIL: {message}", file=sys.stderr)
    sys.exit(1)

for name, expected in expected_raw_hashes.items():
    path = root / "raw" / name
    if not path.exists():
        fail(f"missing raw input {name}")
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected:
        fail(f"raw input {name} was modified")

if not db_path.is_file():
    fail("missing /app/out/acme-ledger.sqlite")
if not csv_path.is_file():
    fail("missing /app/out/merchant_daily_net.csv")

con = sqlite3.connect(db_path)

if con.execute("PRAGMA application_id").fetchone()[0] != 0x41434D45:
    fail("wrong SQLite application_id")
if con.execute("PRAGMA user_version").fetchone()[0] != 20260625:
    fail("wrong SQLite user_version")

strict = {row[1]: row[5] for row in con.execute("PRAGMA table_list").fetchall()}
if strict.get("payments") != 1:
    fail("payments table is not STRICT")
if strict.get("import_errors") != 1:
    fail("import_errors table is not STRICT")

payment_cols = [(r[1], r[2], r[3], r[5], r[6]) for r in con.execute("PRAGMA table_xinfo(payments)").fetchall()]
expected_cols = [
    ("payment_id", "TEXT", 1, 1, 0),
    ("merchant", "TEXT", 1, 0, 0),
    ("amount_cents", "INTEGER", 1, 0, 0),
    ("currency", "TEXT", 1, 0, 0),
    ("status", "TEXT", 1, 0, 0),
    ("event_time", "TEXT", 1, 0, 0),
    ("settled_at", "TEXT", 0, 0, 0),
    ("source_file", "TEXT", 1, 0, 0),
    ("source_line", "INTEGER", 1, 0, 0),
    ("net_cents", "INTEGER", 0, 0, 3),
]
if payment_cols != expected_cols:
    fail(f"payments schema mismatch: {payment_cols}")

indexes = {
    row[1]: con.execute(
        "SELECT sql FROM sqlite_master WHERE type='index' AND name=?", (row[1],)
    ).fetchone()[0]
    for row in con.execute("PRAGMA index_list(payments)").fetchall()
}
if "payments_merchant_time_idx" not in indexes:
    fail("missing payments_merchant_time_idx")
if "payments_refunds_idx" not in indexes or "WHERE status = 'refunded'" not in indexes["payments_refunds_idx"]:
    fail("missing or incorrect partial refunds index")

view_sql = con.execute("SELECT sql FROM sqlite_master WHERE type='view' AND name='merchant_daily_net'").fetchone()
if view_sql is None:
    fail("missing merchant_daily_net view")

payments = con.execute(
    """
    SELECT payment_id, merchant, amount_cents, currency, status, event_time,
           settled_at, source_file, source_line, net_cents
      FROM payments
     ORDER BY payment_id
    """
).fetchall()
if payments != expected_payments:
    fail(f"payments rows are incorrect: {payments}")

errors = con.execute(
    "SELECT source_file, source_line, raw_payment_id, reason FROM import_errors ORDER BY source_file, source_line"
).fetchall()
if errors != expected_errors:
    fail(f"import_errors rows are incorrect: {errors}")

summary = con.execute(
    "SELECT day, merchant, currency, total_cents, payment_count FROM merchant_daily_net ORDER BY day, merchant, currency"
).fetchall()
if [[str(x) for x in row] for row in summary] != expected_summary_rows:
    fail(f"merchant_daily_net view rows are incorrect: {summary}")

csv_bytes = csv_path.read_bytes()
if not csv_bytes.endswith(b"\n") or csv_bytes.endswith(b"\n\n"):
    fail("summary CSV must end with exactly one trailing newline")
csv_rows = list(csv.reader(csv_bytes.decode("utf-8").splitlines()))
expected_csv = [["day", "merchant", "currency", "total_cents", "payment_count"], *expected_summary_rows]
if csv_rows != expected_csv:
    fail(f"summary CSV rows are incorrect: {csv_rows}")

try:
    con.execute(
        "INSERT INTO payments(payment_id, merchant, amount_cents, currency, status, event_time, settled_at, source_file, source_line) "
        "VALUES('bad','Bad',1,'GBP','settled','2026-06-04T00:00:00Z',NULL,'x',1)"
    )
except sqlite3.IntegrityError:
    pass
else:
    fail("payments currency CHECK constraint is not enforced")

con.close()
print("ok")
PY
then
  reward=1
fi

echo "$reward" > /logs/verifier/reward.txt
