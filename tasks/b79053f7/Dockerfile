# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help:
# Container for FinOps automation exercise.
# Provides the initial YAML and TOML configuration files under /home/user/finops
# and includes pytest for automated grading.

LABEL Author="finops-scenario"

ENV HOME=/home/user

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/finops

RUN cat <<'YAML' > /home/user/finops/cost_policy.yaml
environments:
  dev:
    monthly_budget: 300
  prod:
    monthly_budget: 1200
YAML

RUN cat <<'TOML' > /home/user/finops/subscription.toml
[features]
spot_instances = false
commitment_discounts = false
rightsizing = false

[limits]
max_instances = 50
max_cores = 200
TOML

RUN chmod 0644 /home/user/finops/cost_policy.yaml /home/user/finops/subscription.toml

RUN chmod 755 /home/user