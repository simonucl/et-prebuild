# Rebuild the ACME payment ledger

The raw gateway exports in `/app/raw` need to be converted into a canonical SQLite ledger for an offline audit.

Create these two derived artifacts, and leave the raw inputs unchanged:

- `/app/out/acme-ledger.sqlite`
- `/app/out/merchant_daily_net.csv`

Use `/app/config/status-map.json` to map gateway statuses into the canonical statuses `settled`, `refunded`, and `failed`.

Database requirements:

1. Set `PRAGMA application_id` to `0x41434D45` and `PRAGMA user_version` to `20260625`.
2. Create a STRICT table named `payments` with these columns:
   - `payment_id TEXT PRIMARY KEY`
   - `merchant TEXT NOT NULL`
   - `amount_cents INTEGER NOT NULL`
   - `currency TEXT NOT NULL CHECK(currency IN ('USD','EUR'))`
   - `status TEXT NOT NULL CHECK(status IN ('settled','refunded','failed'))`
   - `event_time TEXT NOT NULL`
   - `settled_at TEXT`
   - `source_file TEXT NOT NULL`
   - `source_line INTEGER NOT NULL`
   - `net_cents INTEGER GENERATED ALWAYS AS (CASE WHEN status='refunded' THEN -abs(amount_cents) WHEN status='failed' THEN 0 ELSE abs(amount_cents) END) STORED`
3. Create a STRICT table named `import_errors` with columns `source_file TEXT`, `source_line INTEGER`, `raw_payment_id TEXT`, and `reason TEXT`.
4. Create an index `payments_merchant_time_idx` on `(merchant, event_time)`.
5. Create a partial index `payments_refunds_idx` on `(merchant, event_time)` for rows where `status = 'refunded'`.
6. Create a view `merchant_daily_net` with columns `day`, `merchant`, `currency`, `total_cents`, and `payment_count`, grouping valid payments by UTC date, merchant, and currency.

Import rules:

- Parse the CSV files in filename order and record the original source filename and 1-based CSV line number for every accepted payment.
- Convert amounts to integer cents using decimal arithmetic, rounding half up to the nearest cent.
- Strip `$` and `,` thousands separators from amounts before conversion.
- If the same `payment_id` appears more than once, keep only the row with the latest `event_time`.
- Reject rows with a blank payment id, unmapped status, unsupported currency, or an amount that cannot be parsed. Record each rejected row in `import_errors` using the reason strings `blank payment_id`, `unmapped status`, `unsupported currency`, and `invalid amount`.

CSV export requirements:

- Write `/app/out/merchant_daily_net.csv` from the `merchant_daily_net` view.
- Include the header `day,merchant,currency,total_cents,payment_count`.
- Sort rows by `day`, then `merchant`, then `currency`.
- End the file with exactly one trailing newline.
