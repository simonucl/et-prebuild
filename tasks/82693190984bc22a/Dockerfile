FROM debian:trixie-slim

WORKDIR /home/user/prom_lab

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
       bash ca-certificates coreutils prometheus python3 python3-yaml \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash user \
    && mkdir -p /home/user/prom_lab/rules /home/user/prom_lab/tests /home/user/prom_lab/release /home/user/prom_lab/notes

RUN cat > /home/user/prom_lab/rules/checkout.rules.yml <<'YAML'
groups:
  - name: checkout
    rules:
      - alert: CheckoutHighErrorRate
        expr: rate(checkout_http_requests_total{status="500"}[1m]) > 0
        labels:
          severity: critical
YAML

RUN cat > /home/user/prom_lab/tests/checkout.test.yml <<'YAML'
rule_files:
  - /home/user/prom_lab/rules/checkout.rules.yml
tests: []
YAML

RUN printf '{"status":"stale"}\n' > /home/user/prom_lab/release/manifest.json

RUN cat > /home/user/prom_lab/notes/requirements.txt <<'TEXT'
The production checkout-api service exposes:
- checkout_http_requests_total{job="checkout-api",status="200|400|500|503"}
- checkout_request_duration_seconds_bucket{job="checkout-api",le="..."}

The handoff should define recording rules first, alert rules second, and a
promtool unit-test file that exercises both the quiet and firing cases.
TEXT

RUN chown -R user:user /home/user/prom_lab

USER user
