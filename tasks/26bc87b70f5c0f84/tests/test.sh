#!/bin/bash
set -u

mkdir -p /logs/verifier
reward=0

fail() {
  echo "FAIL: $*" >&2
  echo "$reward" > /logs/verifier/reward.txt
  exit 1
}

db=/home/user/support_lab/output/support.sqlite
summary=/home/user/support_lab/output/summary.json

[ -f "$db" ] || fail "missing support.sqlite"
[ -f "$summary" ] || fail "missing summary.json"

python3 - "$db" "$summary" <<'PY' || fail "database or summary content is incorrect"
import json
import sqlite3
import sys
from pathlib import Path

db_path = Path(sys.argv[1])
summary_path = Path(sys.argv[2])

raw_summary = summary_path.read_bytes()
if raw_summary.count(b"\n") != 1 or not raw_summary.endswith(b"\n"):
    raise SystemExit("summary must have exactly one trailing newline")
if b" " in raw_summary.strip() or b"\n" in raw_summary.strip():
    raise SystemExit("summary must be minified")

expected_summary = {
    "database": "/home/user/support_lab/output/support.sqlite",
    "tickets": 5,
    "messages": 11,
    "open_accounts": ["ACME", "CYGNUS", "ORION"],
    "tickets_by_status": {"open": 2, "pending": 1, "resolved": 2},
    "fts_probe": ["TCK-1001", "TCK-1002"],
    "rejected_ticket_rows": 2,
    "rejected_message_rows": 2,
}
summary = json.loads(raw_summary)
if summary != expected_summary:
    raise SystemExit(f"summary differs: {summary!r}")
if list(summary.keys()) != list(expected_summary.keys()):
    raise SystemExit("summary top-level key order is wrong")
if list(summary["tickets_by_status"].keys()) != ["open", "pending", "resolved"]:
    raise SystemExit("tickets_by_status key order is wrong")

con = sqlite3.connect(db_path)
con.execute("PRAGMA foreign_keys = ON")

if con.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
    raise SystemExit("sqlite integrity_check failed")
if con.execute("PRAGMA user_version").fetchone()[0] != 7:
    raise SystemExit("user_version is not 7")
fk_rows = con.execute("PRAGMA foreign_key_check").fetchall()
if fk_rows:
    raise SystemExit(f"foreign key violations: {fk_rows!r}")

tables = dict(con.execute("SELECT name, sql FROM sqlite_master WHERE type IN ('table','index') AND name NOT LIKE 'sqlite_%'"))
required_names = {
    "tickets",
    "messages",
    "idx_tickets_status_priority",
    "idx_messages_ticket_time",
    "idx_one_active_ticket_per_account",
    "ticket_search",
}
if not required_names.issubset(tables):
    raise SystemExit(f"missing schema objects: {sorted(required_names - set(tables))}")
if "STRICT" not in tables["tickets"].upper() or "STRICT" not in tables["messages"].upper():
    raise SystemExit("tickets and messages must be STRICT tables")
if "WHERE status IN ('open','pending')" not in tables["idx_one_active_ticket_per_account"]:
    raise SystemExit("partial active-ticket index is wrong")
if "tokenize='porter unicode61'" not in tables["ticket_search"]:
    raise SystemExit("FTS5 tokenizer is wrong")

expected_tickets = [
    ("TCK-1001", "ACME", "ops@acme.test", "open", 2, "API timeout after deploy", "2026-06-20T13:00:00Z", "2026-06-20T19:45:00Z", '["api","timeout"]', 17, None),
    ("TCK-1002", "BETA", "billing@beta.test", "resolved", 5, "Duplicate invoice generated", "2026-06-21T10:15:00Z", "2026-06-21T12:45:00Z", '["billing","invoice"]', 45, 150),
    ("TCK-1003", "CYGNUS", "help@cygnus.test", "pending", 3, "MFA code delayed", "2026-06-22T06:00:00Z", "2026-06-22T07:30:00Z", '["login","mfa"]', 70, None),
    ("TCK-1004", "DELTA", "reports@delta.test", "resolved", 1, "CSV export missing rows", "2026-06-23T01:00:00Z", "2026-06-24T01:00:00Z", '["export","csv"]', 150, 1440),
    ("TCK-1005", "ORION", "hooks@orion.test", "open", 4, "Webhook retry storm", "2026-06-24T16:30:00Z", "2026-06-24T17:05:00Z", '["webhook","retry"]', 20, None),
]
actual_tickets = con.execute(
    "SELECT ticket_id,account,requester_email,status,priority,subject,created_at_utc,updated_at_utc,tags_json,first_response_minutes,resolution_minutes FROM tickets ORDER BY ticket_id"
).fetchall()
if actual_tickets != expected_tickets:
    raise SystemExit(f"ticket rows differ: {actual_tickets!r}")

expected_messages = [
    ("MSG-1", "TCK-1001", "customer", "2026-06-20T13:05:00Z", "API times out on every request"),
    ("MSG-2", "TCK-1001", "agent", "2026-06-20T13:17:00Z", "Rolling back the deploy and checking timeout traces"),
    ("MSG-3", "TCK-1002", "customer", "2026-06-21T10:20:00Z", "Invoice was duplicated"),
    ("MSG-4", "TCK-1002", "agent", "2026-06-21T11:00:00Z", "Removed duplicate invoice from billing queue"),
    ("MSG-5", "TCK-1003", "customer", "2026-06-22T06:20:00Z", "MFA code arrives after it expires"),
    ("MSG-6", "TCK-1003", "agent", "2026-06-22T07:10:00Z", "Adjusted SMS provider routing"),
    ("MSG-7", "TCK-1004", "system", "2026-06-23T01:05:00Z", "Export job started"),
    ("MSG-8", "TCK-1004", "customer", "2026-06-23T02:00:00Z", "CSV export is missing rows for region west"),
    ("MSG-9", "TCK-1004", "agent", "2026-06-23T03:30:00Z", "Rebuilt export index and requeued CSV"),
    ("MSG-10", "TCK-1005", "customer", "2026-06-24T16:31:00Z", "Webhook retry storm after 503 responses"),
    ("MSG-11", "TCK-1005", "agent", "2026-06-24T16:50:00Z", "Disabled failing webhook endpoint"),
]
actual_messages = con.execute("SELECT message_id,ticket_id,author,created_at_utc,body FROM messages ORDER BY created_at_utc, message_id").fetchall()
if actual_messages != expected_messages:
    raise SystemExit(f"message rows differ: {actual_messages!r}")

probe = [r[0] for r in con.execute("SELECT ticket_id FROM ticket_search WHERE ticket_search MATCH ? ORDER BY ticket_id", ("timeout OR invoice",))]
if probe != ["TCK-1001", "TCK-1002"]:
    raise SystemExit(f"FTS probe failed: {probe!r}")
webhook = [r[0] for r in con.execute("SELECT ticket_id FROM ticket_search WHERE ticket_search MATCH ? ORDER BY ticket_id", ("webhook",))]
if webhook != ["TCK-1005"]:
    raise SystemExit(f"FTS webhook probe failed: {webhook!r}")

plan = [row[3] for row in con.execute("EXPLAIN QUERY PLAN SELECT * FROM tickets WHERE status='open' ORDER BY priority DESC, updated_at_utc")]
if not any("idx_tickets_status_priority" in item for item in plan):
    raise SystemExit("status/priority query does not use the required index")

con.close()
PY

reward=1
echo "$reward" > /logs/verifier/reward.txt
echo "all checks passed"
