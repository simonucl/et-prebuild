#!/bin/bash
set -u

mkdir -p /logs/verifier
reward=0
ROOT="${ROOT_PREFIX:-}"
BASE="$ROOT/home/user/prom_lab"

finish() {
  echo "$reward" > /logs/verifier/reward.txt
}
trap finish EXIT

fail() {
  echo "FAIL: $*" >&2
  exit 0
}

[ -d "$BASE" ] || fail "missing /home/user/prom_lab"
[ -f "$BASE/rules/checkout.rules.yml" ] || fail "missing checkout.rules.yml"
[ -f "$BASE/tests/checkout.test.yml" ] || fail "missing checkout.test.yml"
[ -f "$BASE/release/manifest.json" ] || fail "missing manifest.json"

if [ "$(find "$BASE/release" -mindepth 1 -maxdepth 1 -printf '%f\n' | sort | tr '\n' ' ')" != "manifest.json " ]; then
  fail "release directory contains unexpected files"
fi

if [ -f "$BASE/notes/requirements.txt" ]; then
  grep -Fq 'checkout_http_requests_total{job="checkout-api",status="200|400|500|503"}' "$BASE/notes/requirements.txt" \
    || fail "notes/requirements.txt was modified"
else
  fail "notes/requirements.txt is missing"
fi

python3 - "$BASE" <<'PY' || fail "rules, tests, or manifest content is incorrect"
import json
import sys
from pathlib import Path

import yaml

base = Path(sys.argv[1])
rules_path = base / "rules/checkout.rules.yml"
tests_path = base / "tests/checkout.test.yml"
manifest_path = base / "release/manifest.json"

EXPECTED_RULES = {
    "groups": [
        {
            "name": "checkout:slo",
            "interval": "30s",
            "rules": [
                {
                    "record": "job:checkout_request_errors:ratio5m",
                    "expr": 'sum(rate(checkout_http_requests_total{job="checkout-api",status=~"5.."}[5m])) / sum(rate(checkout_http_requests_total{job="checkout-api"}[5m]))',
                },
                {
                    "record": "job:checkout_request_duration_seconds:p95_5m",
                    "expr": 'histogram_quantile(0.95, sum by (le) (rate(checkout_request_duration_seconds_bucket{job="checkout-api"}[5m])))',
                },
            ],
        },
        {
            "name": "checkout:alerts",
            "rules": [
                {
                    "alert": "CheckoutHighErrorRate",
                    "expr": "job:checkout_request_errors:ratio5m > 0.02",
                    "for": "10m",
                    "labels": {"severity": "page", "team": "payments"},
                    "annotations": {
                        "summary": "Checkout API 5xx error ratio is above 2%",
                        "description": "The checkout-api 5xx request ratio has been above 2% for 10 minutes.",
                    },
                },
                {
                    "alert": "CheckoutHighLatencyP95",
                    "expr": "job:checkout_request_duration_seconds:p95_5m > 0.75",
                    "for": "15m",
                    "labels": {"severity": "ticket", "team": "payments"},
                    "annotations": {
                        "summary": "Checkout API p95 latency is above 750ms",
                        "description": "The checkout-api p95 request latency has been above 750ms for 15 minutes.",
                    },
                },
            ],
        },
    ],
}

EXPECTED_TESTS = {
    "rule_files": ["/home/user/prom_lab/rules/checkout.rules.yml"],
    "evaluation_interval": "1m",
    "tests": [
        {
            "interval": "1m",
            "input_series": [
                {"series": 'checkout_http_requests_total{job="checkout-api",status="200"}', "values": "0+600x30"},
                {"series": 'checkout_http_requests_total{job="checkout-api",status="500"}', "values": "0+1x30"},
                {"series": 'checkout_request_duration_seconds_bucket{job="checkout-api",le="0.5"}', "values": "0+590x30"},
                {"series": 'checkout_request_duration_seconds_bucket{job="checkout-api",le="0.75"}', "values": "0+599x30"},
                {"series": 'checkout_request_duration_seconds_bucket{job="checkout-api",le="1"}', "values": "0+600x30"},
                {"series": 'checkout_request_duration_seconds_bucket{job="checkout-api",le="+Inf"}', "values": "0+600x30"},
            ],
            "alert_rule_test": [
                {"eval_time": "20m", "alertname": "CheckoutHighErrorRate", "exp_alerts": []},
                {"eval_time": "20m", "alertname": "CheckoutHighLatencyP95", "exp_alerts": []},
            ],
        },
        {
            "interval": "1m",
            "input_series": [
                {"series": 'checkout_http_requests_total{job="checkout-api",status="200"}', "values": "0+100x40"},
                {"series": 'checkout_http_requests_total{job="checkout-api",status="500"}', "values": "0+10x40"},
                {"series": 'checkout_request_duration_seconds_bucket{job="checkout-api",le="0.5"}', "values": "0+10x40"},
                {"series": 'checkout_request_duration_seconds_bucket{job="checkout-api",le="0.75"}', "values": "0+50x40"},
                {"series": 'checkout_request_duration_seconds_bucket{job="checkout-api",le="1"}', "values": "0+100x40"},
                {"series": 'checkout_request_duration_seconds_bucket{job="checkout-api",le="+Inf"}', "values": "0+100x40"},
            ],
            "alert_rule_test": [
                {
                    "eval_time": "20m",
                    "alertname": "CheckoutHighErrorRate",
                    "exp_alerts": [
                        {
                            "exp_labels": {
                                "alertname": "CheckoutHighErrorRate",
                                "severity": "page",
                                "team": "payments",
                            },
                            "exp_annotations": {
                                "summary": "Checkout API 5xx error ratio is above 2%",
                                "description": "The checkout-api 5xx request ratio has been above 2% for 10 minutes.",
                            },
                        }
                    ],
                },
                {
                    "eval_time": "25m",
                    "alertname": "CheckoutHighLatencyP95",
                    "exp_alerts": [
                        {
                            "exp_labels": {
                                "alertname": "CheckoutHighLatencyP95",
                                "severity": "ticket",
                                "team": "payments",
                            },
                            "exp_annotations": {
                                "summary": "Checkout API p95 latency is above 750ms",
                                "description": "The checkout-api p95 request latency has been above 750ms for 15 minutes.",
                            },
                        }
                    ],
                },
            ],
        },
    ],
}

EXPECTED_MANIFEST = {
    "rules": "/home/user/prom_lab/rules/checkout.rules.yml",
    "tests": "/home/user/prom_lab/tests/checkout.test.yml",
    "groups": ["checkout:slo", "checkout:alerts"],
    "alerts": ["CheckoutHighErrorRate", "CheckoutHighLatencyP95"],
    "promtool": "promtool test rules /home/user/prom_lab/tests/checkout.test.yml",
}

rules = yaml.safe_load(rules_path.read_text(encoding="utf-8"))
tests = yaml.safe_load(tests_path.read_text(encoding="utf-8"))
if rules != EXPECTED_RULES:
    raise SystemExit("rules YAML does not match required groups, expressions, labels, annotations, or order")
if tests != EXPECTED_TESTS:
    raise SystemExit("promtool test YAML does not match required scenarios or order")

raw_manifest = manifest_path.read_bytes()
if raw_manifest != json.dumps(EXPECTED_MANIFEST, separators=(",", ":")).encode("utf-8") + b"\n":
    raise SystemExit("manifest is not exact minified JSON with one trailing newline")
PY

if [ -z "$ROOT" ] && command -v promtool >/dev/null 2>&1; then
  promtool check rules "$BASE/rules/checkout.rules.yml" >/tmp/promtool-check.out 2>&1 \
    || fail "promtool check rules failed: $(cat /tmp/promtool-check.out)"
  promtool test rules "$BASE/tests/checkout.test.yml" >/tmp/promtool-test.out 2>&1 \
    || fail "promtool test rules failed: $(cat /tmp/promtool-test.out)"
fi

reward=1
