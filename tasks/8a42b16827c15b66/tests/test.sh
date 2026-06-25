#!/bin/bash
set -u

mkdir -p /logs/verifier
echo 0 > /logs/verifier/reward.txt

fail() {
  echo "FAIL: $*" >&2
  echo 0 > /logs/verifier/reward.txt
  exit 0
}

SITE=/etc/nginx/sites-available/release-console.conf
LINK=/etc/nginx/sites-enabled/release-console.conf

[ -f "$SITE" ] || fail "missing site config"
[ -L "$LINK" ] || fail "enabled site is not a symlink"
[ "$(readlink "$LINK")" = "$SITE" ] || fail "enabled symlink points to the wrong target"
[ ! -e /etc/nginx/sites-enabled/default ] || fail "default enabled site is still present"

nginx -t >/tmp/nginx-test.out 2>&1 || fail "nginx -t failed: $(cat /tmp/nginx-test.out)"

nginx -s stop >/dev/null 2>&1 || true
nginx >/tmp/nginx-start.out 2>&1 || fail "nginx failed to start: $(cat /tmp/nginx-start.out)"
trap 'nginx -s stop >/dev/null 2>&1 || true' EXIT

for _ in $(seq 1 30); do
  if curl -fsS --max-time 1 http://127.0.0.1:18082/ >/tmp/root.body 2>/dev/null; then
    break
  fi
  sleep 0.2
done

curl -fsS -D /tmp/root.headers http://127.0.0.1:18082/ -o /tmp/root.body || fail "root route did not return 200"
grep -q 'Release Console 2026.06' /tmp/root.body || fail "root route did not serve current release"
grep -qi '^X-Frame-Options: DENY' /tmp/root.headers || fail "root route lacks hardened headers"
grep -qi '^X-Content-Type-Options: nosniff' /tmp/root.headers || fail "root route lacks nosniff header"

curl -fsS -D /tmp/app.headers http://127.0.0.1:18082/app/deployments/alpha -o /tmp/app.body || fail "app nested route did not return 200"
grep -q 'Release app shell 2026.06' /tmp/app.body || fail "app nested route did not fall back to /app/index.html"

asset_status=$(curl -sS -o /tmp/missing.body -w '%{http_code}' http://127.0.0.1:18082/assets/missing.js)
[ "$asset_status" = "404" ] || fail "missing asset returned $asset_status instead of 404"

curl -fsS -D /tmp/asset.headers http://127.0.0.1:18082/assets/main.77f3.js -o /tmp/asset.body || fail "asset route did not serve the JS"
grep -q 'release-console build 77f3' /tmp/asset.body || fail "asset body is wrong"
grep -qi '^Cache-Control: public, max-age=31536000, immutable' /tmp/asset.headers || fail "asset cache header is wrong"
grep -qi '^X-Frame-Options: DENY' /tmp/asset.headers || fail "asset route lost hardened headers"

curl -fsS -H 'Accept-Encoding: gzip' -D /tmp/gzip.headers http://127.0.0.1:18082/assets/main.77f3.js -o /tmp/asset.gz || fail "gzip asset request failed"
grep -qi '^Content-Encoding: gzip' /tmp/gzip.headers || fail "precompressed asset was not served with gzip encoding"
gzip -dc /tmp/asset.gz | grep -q 'release-console build 77f3' || fail "gzip asset content is wrong"

curl -fsS -D /tmp/export.headers http://127.0.0.1:18082/exports/daily.csv -o /tmp/export.body || fail "export route did not serve daily.csv"
grep -q '2026-06-25,green' /tmp/export.body || fail "export body is wrong"
grep -qi '^Cache-Control: private, no-store' /tmp/export.headers || fail "export cache header is wrong"
grep -qi '^X-Frame-Options: DENY' /tmp/export.headers || fail "export route lost hardened headers"
exports_status=$(curl -sS -o /tmp/exports-index.body -w '%{http_code}' http://127.0.0.1:18082/exports/)
[ "$exports_status" != "200" ] || fail "exports directory listing is reachable"
export_missing_status=$(curl -sS -o /tmp/export-missing.body -w '%{http_code}' http://127.0.0.1:18082/exports/missing.csv)
[ "$export_missing_status" = "404" ] || fail "missing export returned $export_missing_status instead of 404"

curl -fsS -D /tmp/api.headers http://127.0.0.1:18082/api/status -o /tmp/api.body || fail "api status route did not return 200"
[ "$(cat /tmp/api.body)" = '{"status":"ok","release":"2026.06"}' ] || fail "api status body is not exact"
grep -qi '^Content-Type: application/json' /tmp/api.headers || fail "api status content type is not JSON"
api_other_status=$(curl -sS -o /tmp/api-other.body -w '%{http_code}' http://127.0.0.1:18082/api/status/extra)
[ "$api_other_status" = "404" ] || fail "unknown api path returned $api_other_status instead of 404"

maintenance_status=$(curl -sS -o /tmp/maintenance-direct.body -w '%{http_code}' http://127.0.0.1:18082/maintenance.html)
[ "$maintenance_status" = "404" ] || fail "maintenance page is directly reachable with status $maintenance_status"
force_status=$(curl -sS -o /tmp/force.body -w '%{http_code}' http://127.0.0.1:18082/force-maintenance)
[ "$force_status" = "503" ] || fail "force-maintenance returned $force_status instead of 503"
grep -q 'Release maintenance window' /tmp/force.body || fail "503 did not use the internal maintenance page"

echo 1 > /logs/verifier/reward.txt
echo "ok"
