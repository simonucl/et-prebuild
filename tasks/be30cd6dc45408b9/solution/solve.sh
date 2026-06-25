#!/bin/bash
set -euo pipefail

APP_ROOT="${APP_ROOT:-/app}"

python3 - <<'PY'
import csv
import json
import sqlite3
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from pathlib import Path

root = Path(__import__("os").environ.get("APP_ROOT", "/app"))
raw_dir = root / "raw"
out_dir = root / "out"
out_dir.mkdir(parents=True, exist_ok=True)
db_path = out_dir / "acme-ledger.sqlite"
csv_path = out_dir / "merchant_daily_net.csv"

if db_path.exists():
    db_path.unlink()
if csv_path.exists():
    csv_path.unlink()

status_map = json.loads((root / "config" / "status-map.json").read_text(encoding="utf-8"))
accepted = {}
errors = []

def cents(value: str) -> int:
    cleaned = value.strip().replace("$", "").replace(",", "")
    dec = Decimal(cleaned)
    return int((dec * Decimal("100")).quantize(Decimal("1"), rounding=ROUND_HALF_UP))

for source in sorted(raw_dir.glob("*.csv")):
    with source.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for line_no, row in enumerate(reader, start=2):
            pid = (row.get("payment_id") or "").strip()
            status_raw = (row.get("status") or "").strip()
            currency = (row.get("currency") or "").strip()
            reason = None
            amount_cents = None

            if not pid:
                reason = "blank payment_id"
            elif status_raw not in status_map:
                reason = "unmapped status"
            elif currency not in {"USD", "EUR"}:
                reason = "unsupported currency"
            else:
                try:
                    amount_cents = cents(row.get("amount") or "")
                except (InvalidOperation, ValueError):
                    reason = "invalid amount"

            if reason is not None:
                errors.append((source.name, line_no, pid, reason))
                continue

            record = {
                "payment_id": pid,
                "merchant": (row.get("merchant") or "").strip(),
                "amount_cents": amount_cents,
                "currency": currency,
                "status": status_map[status_raw],
                "event_time": (row.get("event_time") or "").strip(),
                "settled_at": (row.get("settled_at") or "").strip() or None,
                "source_file": source.name,
                "source_line": line_no,
            }
            prior = accepted.get(pid)
            if prior is None or record["event_time"] > prior["event_time"]:
                accepted[pid] = record

con = sqlite3.connect(db_path)
con.executescript(
    """
    PRAGMA application_id = 0x41434D45;
    PRAGMA user_version = 20260625;

    CREATE TABLE payments (
      payment_id TEXT PRIMARY KEY,
      merchant TEXT NOT NULL,
      amount_cents INTEGER NOT NULL,
      currency TEXT NOT NULL CHECK(currency IN ('USD','EUR')),
      status TEXT NOT NULL CHECK(status IN ('settled','refunded','failed')),
      event_time TEXT NOT NULL,
      settled_at TEXT,
      source_file TEXT NOT NULL,
      source_line INTEGER NOT NULL,
      net_cents INTEGER GENERATED ALWAYS AS (
        CASE
          WHEN status='refunded' THEN -abs(amount_cents)
          WHEN status='failed' THEN 0
          ELSE abs(amount_cents)
        END
      ) STORED
    ) STRICT;

    CREATE TABLE import_errors (
      source_file TEXT,
      source_line INTEGER,
      raw_payment_id TEXT,
      reason TEXT
    ) STRICT;

    CREATE INDEX payments_merchant_time_idx ON payments(merchant, event_time);
    CREATE INDEX payments_refunds_idx ON payments(merchant, event_time) WHERE status = 'refunded';

    CREATE VIEW merchant_daily_net AS
      SELECT substr(event_time, 1, 10) AS day,
             merchant,
             currency,
             sum(net_cents) AS total_cents,
             count(*) AS payment_count
        FROM payments
       GROUP BY day, merchant, currency;
    """
)
con.executemany(
    """
    INSERT INTO payments(payment_id, merchant, amount_cents, currency, status, event_time, settled_at, source_file, source_line)
    VALUES(:payment_id, :merchant, :amount_cents, :currency, :status, :event_time, :settled_at, :source_file, :source_line)
    """,
    [accepted[k] for k in sorted(accepted)],
)
con.executemany(
    "INSERT INTO import_errors(source_file, source_line, raw_payment_id, reason) VALUES(?, ?, ?, ?)",
    errors,
)
con.commit()

rows = con.execute(
    "SELECT day, merchant, currency, total_cents, payment_count FROM merchant_daily_net ORDER BY day, merchant, currency"
).fetchall()
with csv_path.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.writer(handle, lineterminator="\n")
    writer.writerow(["day", "merchant", "currency", "total_cents", "payment_count"])
    writer.writerows(rows)

con.close()
PY
