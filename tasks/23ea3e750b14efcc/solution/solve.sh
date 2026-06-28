#!/bin/bash
set -euo pipefail

src=/home/user/ledger/source
backup=/home/user/ledger/backups
snapshot="$backup/ledger.snar"

mkdir -p "$backup"

tar --listed-incremental="$snapshot" \
    --exclude='./logs/*' \
    --exclude='./tmp/*' \
    -czf "$backup/ledger-full.tar.gz" \
    -C "$src" .

sed -i 's/^retention_days=30$/retention_days=60/' "$src/configs/app.ini"
printf '4001,Deferred Revenue,active\n' >> "$src/data/accounts.csv"
rm -f "$src/data/transactions/jan.csv"
cat > "$src/data/transactions/feb.csv" <<'EOF'
txn_id,account_id,amount
FEB-001,1001,800.00
FEB-002,4001,-800.00
EOF
mkdir -p "$src/notes"
cat > "$src/notes/release.txt" <<'EOF'
retention updated to 60 days
january extract superseded by february
EOF
touch -d '2026-01-16 00:00:00 UTC' \
    "$src/configs/app.ini" \
    "$src/data/accounts.csv" \
    "$src/data/transactions" \
    "$src/data/transactions/feb.csv" \
    "$src/notes" \
    "$src/notes/release.txt"

tar --listed-incremental="$snapshot" \
    --exclude='./logs/*' \
    --exclude='./tmp/*' \
    -czf "$backup/ledger-incremental.tar.gz" \
    -C "$src" .

cat > "$backup/manifest.txt" <<'EOF'
full=ledger-full.tar.gz
incremental=ledger-incremental.tar.gz
snapshot=ledger.snar
EOF
