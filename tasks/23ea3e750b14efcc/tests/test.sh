#!/bin/bash
set -u

mkdir -p /logs/verifier

fail() {
  echo 0 > /logs/verifier/reward.txt
  exit 0
}

backup=/home/user/ledger/backups
full="$backup/ledger-full.tar.gz"
inc="$backup/ledger-incremental.tar.gz"
snapshot="$backup/ledger.snar"
manifest="$backup/manifest.txt"

[ -d "$backup" ] || fail
[ -f "$full" ] || fail
[ -f "$inc" ] || fail
[ -s "$snapshot" ] || fail
[ -f "$manifest" ] || fail

expected_manifest="$(mktemp)"
cat > "$expected_manifest" <<'EOF'
full=ledger-full.tar.gz
incremental=ledger-incremental.tar.gz
snapshot=ledger.snar
EOF
cmp -s "$expected_manifest" "$manifest" || fail

gzip -t "$full" || fail
gzip -t "$inc" || fail

if tar -tzf "$full" | grep -Eq '(^|/)(logs|tmp)/[^/]+$'; then fail; fi
if tar -tzf "$inc" | grep -Eq '(^|/)(logs|tmp)/[^/]+$'; then fail; fi
if tar -tzf "$full" | grep -q '^/'; then fail; fi
if tar -tzf "$inc" | grep -q '^/'; then fail; fi

full_restore="$(mktemp -d)"
final_restore="$(mktemp -d)"

tar --listed-incremental=/dev/null -xzf "$full" -C "$full_restore" || fail
tar --listed-incremental=/dev/null -xzf "$full" -C "$final_restore" || fail
tar --listed-incremental=/dev/null -xzf "$inc" -C "$final_restore" || fail

cat > /tmp/env000_expected_full_app.ini <<'EOF'
[ledger]
currency=USD
retention_days=30
mode=batch
EOF
cat > /tmp/env000_expected_full_accounts.csv <<'EOF'
account_id,name,status
1001,Cash,active
2001,Accounts Receivable,active
3001,Revenue,active
EOF
cat > /tmp/env000_expected_jan.csv <<'EOF'
txn_id,account_id,amount
JAN-001,1001,1250.00
JAN-002,3001,-1250.00
EOF

cmp -s /tmp/env000_expected_full_app.ini "$full_restore/configs/app.ini" || fail
cmp -s /tmp/env000_expected_full_accounts.csv "$full_restore/data/accounts.csv" || fail
cmp -s /tmp/env000_expected_jan.csv "$full_restore/data/transactions/jan.csv" || fail
[ ! -e "$full_restore/data/transactions/feb.csv" ] || fail
[ ! -e "$full_restore/notes/release.txt" ] || fail
[ ! -e "$full_restore/logs/runtime.log" ] || fail
[ ! -e "$full_restore/tmp/cache.bin" ] || fail

cat > /tmp/env000_expected_final_app.ini <<'EOF'
[ledger]
currency=USD
retention_days=60
mode=batch
EOF
cat > /tmp/env000_expected_final_accounts.csv <<'EOF'
account_id,name,status
1001,Cash,active
2001,Accounts Receivable,active
3001,Revenue,active
4001,Deferred Revenue,active
EOF
cat > /tmp/env000_expected_feb.csv <<'EOF'
txn_id,account_id,amount
FEB-001,1001,800.00
FEB-002,4001,-800.00
EOF
cat > /tmp/env000_expected_release.txt <<'EOF'
retention updated to 60 days
january extract superseded by february
EOF

cmp -s /tmp/env000_expected_final_app.ini "$final_restore/configs/app.ini" || fail
cmp -s /tmp/env000_expected_final_accounts.csv "$final_restore/data/accounts.csv" || fail
cmp -s /tmp/env000_expected_feb.csv "$final_restore/data/transactions/feb.csv" || fail
cmp -s /tmp/env000_expected_release.txt "$final_restore/notes/release.txt" || fail
[ ! -e "$final_restore/data/transactions/jan.csv" ] || fail
[ ! -e "$final_restore/logs/runtime.log" ] || fail
[ ! -e "$final_restore/tmp/cache.bin" ] || fail

grep -a -q 'GNU tar' "$snapshot" || fail

echo 1 > /logs/verifier/reward.txt
