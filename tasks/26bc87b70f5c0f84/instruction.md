# Build the Support Ticket SQLite Index

You are preparing an offline support-search handoff. The raw inputs are already staged at:

- `/home/user/support_lab/incoming/tickets.jsonl`
- `/home/user/support_lab/incoming/messages.csv`

Create these two deliverables:

- `/home/user/support_lab/output/support.sqlite`
- `/home/user/support_lab/output/summary.json`

Do not use the network. Do not modify the files under `/home/user/support_lab/incoming`.

## Ticket normalization

Read every JSON object in `tickets.jsonl`.

- A ticket row is valid only when it has a non-empty `ticket_id`, an email containing `@`, a status of `open`, `pending`, or `resolved` after lowercasing, and an integer priority from 1 through 5.
- If the same `ticket_id` appears more than once, keep only the valid row with the newest normalized `updated_at` timestamp.
- Normalize `account` by trimming whitespace and uppercasing it.
- Normalize `status` to lowercase.
- Normalize `created_at` and `updated_at` to UTC in `YYYY-MM-DDTHH:MM:SSZ` form.
- Normalize `tags` to a minified JSON array of lowercase, trimmed strings, preserving first-seen order and removing duplicates.

## Message normalization

Read `messages.csv` with normal CSV quoting rules.

- Import only messages whose `ticket_id` belongs to a kept ticket.
- Import only authors `customer`, `agent`, and `system`.
- Normalize message timestamps to UTC in `YYYY-MM-DDTHH:MM:SSZ` form.
- Keep message bodies byte-for-byte after CSV parsing.

## SQLite database

Create `/home/user/support_lab/output/support.sqlite` as a SQLite database with these tables and indexes:

```sql
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
```

`first_response_minutes` is the whole number of minutes from ticket creation to the first imported `agent` message for that ticket, or `NULL` when no agent message exists. `resolution_minutes` is the whole number of minutes from creation to update for resolved tickets, and `NULL` for other statuses.

Populate `ticket_search` with one row per kept ticket. Its `body` column must be all imported message bodies for that ticket, ordered by `created_at_utc` then `message_id`, joined by newline characters. Its `tags` column must be the normalized tags joined by single spaces.

Set `PRAGMA user_version = 7` in the final database.

## Summary JSON

Create `/home/user/support_lab/output/summary.json` as minified JSON on one line with exactly one trailing newline. Use this top-level key order:

```json
{"database":"/home/user/support_lab/output/support.sqlite","tickets":0,"messages":0,"open_accounts":[],"tickets_by_status":{"open":0,"pending":0,"resolved":0},"fts_probe":[],"rejected_ticket_rows":0,"rejected_message_rows":0}
```

Required values:

- `tickets` is the number of kept tickets.
- `messages` is the number of imported messages.
- `open_accounts` is the sorted list of accounts whose kept ticket status is `open` or `pending`.
- `tickets_by_status` has keys in the order `open`, `pending`, `resolved`.
- `fts_probe` is the sorted list of `ticket_id` values returned by this FTS5 query: `timeout OR invoice`.
- `rejected_ticket_rows` counts invalid ticket rows only; older duplicate valid rows are superseded, not rejected.
- `rejected_message_rows` counts messages not imported because of an unknown ticket or invalid author.
