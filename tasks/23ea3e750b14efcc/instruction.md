# Create a GNU Tar Incremental Backup Pair

You are preparing an offline backup rehearsal for a small ledger export. The live source tree is:

`/home/user/ledger/source`

Create all backup output under:

`/home/user/ledger/backups`

Required work:

1. Create the backup directory if it does not exist.
2. Before changing the source tree, create a gzip-compressed level-0 GNU tar archive:

   `/home/user/ledger/backups/ledger-full.tar.gz`

   Use GNU tar's `--listed-incremental` snapshot file:

   `/home/user/ledger/backups/ledger.snar`

   Archive the tree relative to `/home/user/ledger/source` so restored paths are relative entries like `./configs/app.ini`, not absolute paths.
3. Exclude the runtime-only paths `./logs/*` and `./tmp/*` from both the full and incremental archives.
4. Apply these source changes exactly:

   - In `configs/app.ini`, change `retention_days=30` to `retention_days=60`.
   - Append this line to `data/accounts.csv`:

     `4001,Deferred Revenue,active`

   - Remove `data/transactions/jan.csv`.
   - Create `data/transactions/feb.csv` with exactly:

     ```text
     txn_id,account_id,amount
     FEB-001,1001,800.00
     FEB-002,4001,-800.00
     ```

   - Create `notes/release.txt` with exactly:

     ```text
     retention updated to 60 days
     january extract superseded by february
     ```

5. After those changes, create a gzip-compressed incremental archive using the same snapshot file:

   `/home/user/ledger/backups/ledger-incremental.tar.gz`

6. Write `/home/user/ledger/backups/manifest.txt` with exactly these three lines:

   ```text
   full=ledger-full.tar.gz
   incremental=ledger-incremental.tar.gz
   snapshot=ledger.snar
   ```

Do not use network access. Do not place backup output outside `/home/user/ledger/backups`.
