# Prometheus Checkout Rule Handoff

Repair the offline Prometheus rule handoff under `/home/user/prom_lab`.

Create or replace exactly these three deliverables:

1. `/home/user/prom_lab/rules/checkout.rules.yml`
2. `/home/user/prom_lab/tests/checkout.test.yml`
3. `/home/user/prom_lab/release/manifest.json`

Do not use the network. Do not modify anything under `/home/user/prom_lab/notes`.

The rules file must contain two groups, in this order:

1. `checkout:slo`, evaluated every `30s`, with these recording rules in order:
   - `job:checkout_request_errors:ratio5m`
   - `job:checkout_request_duration_seconds:p95_5m`
2. `checkout:alerts`, with these alerting rules in order:
   - `CheckoutHighErrorRate`
   - `CheckoutHighLatencyP95`

Required PromQL:

- Error ratio: the 5-minute rate of `checkout_http_requests_total{job="checkout-api",status=~"5.."}` divided by the 5-minute rate of all `checkout_http_requests_total{job="checkout-api"}`.
- p95 latency: `histogram_quantile` over the 5-minute rate of `checkout_request_duration_seconds_bucket{job="checkout-api"}`, aggregated with `sum by (le)`.
- `CheckoutHighErrorRate` fires when the error-ratio recording rule is greater than `0.02` for `10m`.
- `CheckoutHighLatencyP95` fires when the p95-latency recording rule is greater than `0.75` for `15m`.

Both alerts must have labels `team: payments`; the error-rate alert has `severity: page`, and the latency alert has `severity: ticket`.

The promtool test file must reference the rules file and include tests for both alerts. Use a 1-minute evaluation interval.

Create `/home/user/prom_lab/release/manifest.json` as minified JSON with exactly one trailing newline. It must describe the handoff paths, group names, alert names, and the promtool command needed to run the test file.
