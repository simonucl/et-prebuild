#!/bin/bash
set -euo pipefail

ROOT="${ROOT_PREFIX:-}"
BASE="$ROOT/home/user/prom_lab"

cat > "$BASE/rules/checkout.rules.yml" <<'YAML'
groups:
  - name: checkout:slo
    interval: 30s
    rules:
      - record: job:checkout_request_errors:ratio5m
        expr: sum(rate(checkout_http_requests_total{job="checkout-api",status=~"5.."}[5m])) / sum(rate(checkout_http_requests_total{job="checkout-api"}[5m]))
      - record: job:checkout_request_duration_seconds:p95_5m
        expr: histogram_quantile(0.95, sum by (le) (rate(checkout_request_duration_seconds_bucket{job="checkout-api"}[5m])))
  - name: checkout:alerts
    rules:
      - alert: CheckoutHighErrorRate
        expr: job:checkout_request_errors:ratio5m > 0.02
        for: 10m
        labels:
          severity: page
          team: payments
        annotations:
          summary: Checkout API 5xx error ratio is above 2%
          description: The checkout-api 5xx request ratio has been above 2% for 10 minutes.
      - alert: CheckoutHighLatencyP95
        expr: job:checkout_request_duration_seconds:p95_5m > 0.75
        for: 15m
        labels:
          severity: ticket
          team: payments
        annotations:
          summary: Checkout API p95 latency is above 750ms
          description: The checkout-api p95 request latency has been above 750ms for 15 minutes.
YAML

cat > "$BASE/tests/checkout.test.yml" <<'YAML'
rule_files:
  - /home/user/prom_lab/rules/checkout.rules.yml
evaluation_interval: 1m
tests:
  - interval: 1m
    input_series:
      - series: 'checkout_http_requests_total{job="checkout-api",status="200"}'
        values: '0+600x30'
      - series: 'checkout_http_requests_total{job="checkout-api",status="500"}'
        values: '0+1x30'
      - series: 'checkout_request_duration_seconds_bucket{job="checkout-api",le="0.5"}'
        values: '0+590x30'
      - series: 'checkout_request_duration_seconds_bucket{job="checkout-api",le="0.75"}'
        values: '0+599x30'
      - series: 'checkout_request_duration_seconds_bucket{job="checkout-api",le="1"}'
        values: '0+600x30'
      - series: 'checkout_request_duration_seconds_bucket{job="checkout-api",le="+Inf"}'
        values: '0+600x30'
    alert_rule_test:
      - eval_time: 20m
        alertname: CheckoutHighErrorRate
        exp_alerts: []
      - eval_time: 20m
        alertname: CheckoutHighLatencyP95
        exp_alerts: []
  - interval: 1m
    input_series:
      - series: 'checkout_http_requests_total{job="checkout-api",status="200"}'
        values: '0+100x40'
      - series: 'checkout_http_requests_total{job="checkout-api",status="500"}'
        values: '0+10x40'
      - series: 'checkout_request_duration_seconds_bucket{job="checkout-api",le="0.5"}'
        values: '0+10x40'
      - series: 'checkout_request_duration_seconds_bucket{job="checkout-api",le="0.75"}'
        values: '0+50x40'
      - series: 'checkout_request_duration_seconds_bucket{job="checkout-api",le="1"}'
        values: '0+100x40'
      - series: 'checkout_request_duration_seconds_bucket{job="checkout-api",le="+Inf"}'
        values: '0+100x40'
    alert_rule_test:
      - eval_time: 20m
        alertname: CheckoutHighErrorRate
        exp_alerts:
          - exp_labels:
              alertname: CheckoutHighErrorRate
              severity: page
              team: payments
            exp_annotations:
              summary: Checkout API 5xx error ratio is above 2%
              description: The checkout-api 5xx request ratio has been above 2% for 10 minutes.
      - eval_time: 25m
        alertname: CheckoutHighLatencyP95
        exp_alerts:
          - exp_labels:
              alertname: CheckoutHighLatencyP95
              severity: ticket
              team: payments
            exp_annotations:
              summary: Checkout API p95 latency is above 750ms
              description: The checkout-api p95 request latency has been above 750ms for 15 minutes.
YAML

cat > "$BASE/release/manifest.json" <<'JSON'
{"rules":"/home/user/prom_lab/rules/checkout.rules.yml","tests":"/home/user/prom_lab/tests/checkout.test.yml","groups":["checkout:slo","checkout:alerts"],"alerts":["CheckoutHighErrorRate","CheckoutHighLatencyP95"],"promtool":"promtool test rules /home/user/prom_lab/tests/checkout.test.yml"}
JSON

chmod 0644 "$BASE/rules/checkout.rules.yml" "$BASE/tests/checkout.test.yml" "$BASE/release/manifest.json"
