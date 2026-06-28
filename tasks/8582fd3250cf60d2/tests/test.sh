#!/bin/bash
set -u

mkdir -p /logs/verifier
reward_file=/logs/verifier/reward.txt
echo 0 > "$reward_file"

fail() {
  echo "FAIL: $1" >&2
  echo 0 > "$reward_file"
  cleanup
  exit 0
}

cleanup() {
  if [ -n "${backend_pid:-}" ] && kill -0 "$backend_pid" 2>/dev/null; then
    kill "$backend_pid" 2>/dev/null || true
  fi
  nginx -s quit >/dev/null 2>&1 || true
}

stop_nginx_processes() {
  for cmdline in /proc/[0-9]*/cmdline; do
    [ -r "$cmdline" ] || continue
    if tr '\0' ' ' < "$cmdline" 2>/dev/null | grep -q 'nginx'; then
      pid=${cmdline#/proc/}
      pid=${pid%/cmdline}
      kill "$pid" 2>/dev/null || true
    fi
  done
  sleep 0.5
  for cmdline in /proc/[0-9]*/cmdline; do
    [ -r "$cmdline" ] || continue
    if tr '\0' ' ' < "$cmdline" 2>/dev/null | grep -q 'nginx'; then
      pid=${cmdline#/proc/}
      pid=${pid%/cmdline}
      kill -9 "$pid" 2>/dev/null || true
    fi
  done
  sleep 0.2
}

trap cleanup EXIT

command -v nginx >/dev/null 2>&1 || fail "nginx is not installed"
command -v curl >/dev/null 2>&1 || fail "curl is not installed"

[ -f /etc/nginx/conf.d/docs-portal.conf ] || fail "docs-portal config is missing"
[ -f /etc/nginx/conf.d/upstream_echo.conf ] || fail "upstream echo config was removed"
[ ! -e /etc/nginx/conf.d/default.conf ] || fail "default site is still enabled"

expected_report=/tmp/expected-nginx-report.json
printf '%s\n' '{"site":"docs-portal","listen":18080,"spa_root":"/srv/docs/current","asset_alias":"/srv/docs/releases/2026.06.28/assets/","api_upstream":"http://127.0.0.1:9000/","validation_command":"nginx -t"}' > "$expected_report"
cmp -s "$expected_report" /home/user/nginx_migration_report.json || fail "migration report JSON is incorrect"

nginx -t >/tmp/nginx-test.out 2>&1 || fail "nginx -t failed: $(cat /tmp/nginx-test.out)"

stop_nginx_processes
nginx >/tmp/nginx-start.out 2>&1 || fail "nginx failed to start: $(cat /tmp/nginx-start.out)"
sleep 0.2

root_body=$(curl -fsS --max-time 3 http://127.0.0.1:18080/) || fail "root request failed"
case "$root_body" in
  *"DOCS_PORTAL_CURRENT_BUILD=2026.06.28"*) ;;
  *) fail "root did not serve current index; body was: $root_body" ;;
esac

health_body=$(curl -fsS --max-time 3 http://127.0.0.1:18080/health.txt) || fail "health request failed"
[ "$health_body" = "docs portal static health ok" ] || fail "health.txt content mismatch"

fallback_body=$(curl -fsS --max-time 3 http://127.0.0.1:18080/guide/install/linux) || fail "SPA fallback request failed"
case "$fallback_body" in
  *"DOCS_PORTAL_CURRENT_BUILD=2026.06.28"*) ;;
  *) fail "unknown path did not fall back to current index" ;;
esac

asset_headers=$(mktemp)
asset_body=$(curl -fsS --max-time 3 -D "$asset_headers" http://127.0.0.1:18080/assets/app.abc123.js) || fail "asset request failed"
[ "$asset_body" = 'window.__DOCS_ASSET_BUILD__ = "2026.06.28";' ] || fail "asset content mismatch"
grep -i '^Cache-Control: .*public' "$asset_headers" >/dev/null || fail "asset Cache-Control missing public"
grep -i '^Cache-Control: .*max-age=31536000' "$asset_headers" >/dev/null || fail "asset Cache-Control missing max-age"
grep -i '^Cache-Control: .*immutable' "$asset_headers" >/dev/null || fail "asset Cache-Control missing immutable"

secret_status=$(curl -sS --max-time 3 -o /tmp/secret.out -w '%{http_code}' http://127.0.0.1:18080/secret.txt || true)
if grep -q 'release-root-secret-must-not-be-served' /tmp/secret.out 2>/dev/null; then
  fail "secret content leaked"
fi

api_body=$(curl -fsS --max-time 3 'http://127.0.0.1:18080/api/status?check=ready') || fail "api proxy request failed"
[ "$api_body" = "UPSTREAM_PATH=/status?check=ready" ] || fail "api proxy did not strip /api/ prefix"

echo 1 > "$reward_file"
exit 0
