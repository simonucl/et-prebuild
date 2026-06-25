#!/bin/bash
set -euo pipefail

python3 <<'PY'
import csv
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

root = Path("/home/user/support_lab")
incoming = root / "incoming"
out = root / "output"
out.mkdir(parents=True, exist_ok=True)
db_path = out / "support.sqlite"
summary_path = out / "summary.json"
if db_path.exists():
    db_path.unlink()

def parse_time(value):
    dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    return dt.astimezone(timezone.utc).replace(microsecond=0)

def fmt_time(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

def normalize_tags(values):
    seen = set()
    result = []
    for raw in values:
        tag = str(raw).strip().lower()
        if tag and tag not in seen:
            seen.add(tag)
            result.append(tag)
    return result

valid_by_id = {}
rejected_ticket_rows = 0
for line in (incoming / "tickets.jsonl").read_text(encoding="utf-8").splitlines():
    obj = json.loads(line)
    try:
        ticket_id = str(obj["ticket_id"]).strip()
        email = str(obj["requester_email"]).strip()
        status = str(obj["status"]).strip().lower()
        priority = int(obj["priority"])
        created = parse_time(obj["created_at"])
        updated = parse_time(obj["updated_at"])
        if not ticket_id or "@" not in email or status not in {"open", "pending", "resolved"}:
            raise ValueError
        if priority < 1 or priority > 5:
            raise ValueError
    except Exception:
        rejected_ticket_rows += 1
        continue
    row = {
        "ticket_id": ticket_id,
        "account": str(obj["account"]).strip().upper(),
        "requester_email": email,
        "status": status,
        "priority": priority,
        "subject": str(obj["subject"]),
        "created": created,
        "updated": updated,
        "tags": normalize_tags(obj.get("tags", [])),
    }
    old = valid_by_id.get(ticket_id)
    if old is None or row["updated"] > old["updated"]:
        valid_by_id[ticket_id] = row

messages = []
rejected_message_rows = 0
with (incoming / "messages.csv").open(newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        ticket_id = row["ticket_id"].strip()
        author = row["author"].strip()
        if ticket_id not in valid_by_id or author not in {"customer", "agent", "system"}:
            rejected_message_rows += 1
            continue
        messages.append({
            "message_id": row["message_id"].strip(),
            "ticket_id": ticket_id,
            "author": author,
            "created": parse_time(row["created_at"]),
            "body": row["body"],
        })

messages_by_ticket = {ticket_id: [] for ticket_id in valid_by_id}
for msg in messages:
    messages_by_ticket[msg["ticket_id"]].append(msg)
for bucket in messages_by_ticket.values():
    bucket.sort(key=lambda m: (m["created"], m["message_id"]))

for ticket in valid_by_id.values():
    first_agent = next((m for m in messages_by_ticket[ticket["ticket_id"]] if m["author"] == "agent"), None)
    ticket["first_response_minutes"] = None if first_agent is None else int((first_agent["created"] - ticket["created"]).total_seconds() // 60)
    ticket["resolution_minutes"] = None if ticket["status"] != "resolved" else int((ticket["updated"] - ticket["created"]).total_seconds() // 60)

con = sqlite3.connect(db_path)
con.execute("PRAGMA foreign_keys = ON")
con.executescript("""
CREATE TABLE tickets (
  ticket_id TEXT PRIMARY KEY,
  account TEXT NOT NULL,
  requester_email TEXT NOT NULL,
  status TEXT NOT NULL CHECK(status IN ('open','pending','resolved')),
  priority INTEGER NOT NULL CHECK(priority BETWEEN 1 AND 5),
  subject TEXT NOT NULL,
  created_at_utc TEXT NOT NULL,
  updated_at_utc TEXT NOT NULL,
  tags_json TEXT NOT NULL CHECK(json_valid(tags_json)),
  first_response_minutes INTEGER,
  resolution_minutes INTEGER
) STRICT;

CREATE TABLE messages (
  message_id TEXT PRIMARY KEY,
  ticket_id TEXT NOT NULL REFERENCES tickets(ticket_id) ON DELETE CASCADE,
  author TEXT NOT NULL CHECK(author IN ('customer','agent','system')),
  created_at_utc TEXT NOT NULL,
  body TEXT NOT NULL
) STRICT;

CREATE INDEX idx_tickets_status_priority
  ON tickets(status, priority DESC, updated_at_utc);

CREATE INDEX idx_messages_ticket_time
  ON messages(ticket_id, created_at_utc);

CREATE UNIQUE INDEX idx_one_active_ticket_per_account
  ON tickets(account) WHERE status IN ('open','pending');

CREATE VIRTUAL TABLE ticket_search USING fts5(
  ticket_id UNINDEXED,
  subject,
  body,
  tags,
  tokenize='porter unicode61'
);
""")

for ticket_id in sorted(valid_by_id):
    t = valid_by_id[ticket_id]
    con.execute(
        """INSERT INTO tickets VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
        (
            t["ticket_id"], t["account"], t["requester_email"], t["status"], t["priority"],
            t["subject"], fmt_time(t["created"]), fmt_time(t["updated"]),
            json.dumps(t["tags"], separators=(",", ":")),
            t["first_response_minutes"], t["resolution_minutes"],
        ),
    )
for msg in sorted(messages, key=lambda m: m["message_id"]):
    con.execute(
        "INSERT INTO messages VALUES (?,?,?,?,?)",
        (msg["message_id"], msg["ticket_id"], msg["author"], fmt_time(msg["created"]), msg["body"]),
    )
for ticket_id in sorted(valid_by_id):
    t = valid_by_id[ticket_id]
    body = "\n".join(m["body"] for m in messages_by_ticket[ticket_id])
    con.execute(
        "INSERT INTO ticket_search(ticket_id, subject, body, tags) VALUES (?,?,?,?)",
        (ticket_id, t["subject"], body, " ".join(t["tags"])),
    )

con.execute("PRAGMA user_version = 7")
con.commit()

fts_probe = [
    row[0]
    for row in con.execute(
        "SELECT ticket_id FROM ticket_search WHERE ticket_search MATCH ? ORDER BY ticket_id",
        ("timeout OR invoice",),
    )
]
counts = dict(con.execute("SELECT status, count(*) FROM tickets GROUP BY status"))
summary = {
    "database": str(db_path),
    "tickets": len(valid_by_id),
    "messages": len(messages),
    "open_accounts": sorted(t["account"] for t in valid_by_id.values() if t["status"] in {"open", "pending"}),
    "tickets_by_status": {
        "open": counts.get("open", 0),
        "pending": counts.get("pending", 0),
        "resolved": counts.get("resolved", 0),
    },
    "fts_probe": fts_probe,
    "rejected_ticket_rows": rejected_ticket_rows,
    "rejected_message_rows": rejected_message_rows,
}
summary_path.write_text(json.dumps(summary, separators=(",", ":")) + "\n", encoding="utf-8")
con.close()
PY
