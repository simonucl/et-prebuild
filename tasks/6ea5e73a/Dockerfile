# syntax=docker/dockerfile:1
FROM ubuntu:22.04

LABEL Author="db-metrics-task-preparer"
LABEL Description="Starter container for the DB metrics CLI exercise"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        jq \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grading harness
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Prepare filesystem state expected by the tests
# ------------------------------------------------------------------
RUN mkdir -p /home/user/db_metrics

# Create query_metrics.json
RUN cat > /home/user/db_metrics/query_metrics.json <<'JSON_METRICS'
{
  "queries": [
    {
      "id": "Q123",
      "statement": "SELECT * FROM users;",
      "execution_time_ms": 153
    },
    {
      "id": "Q124",
      "statement": "UPDATE orders SET status='SHIPPED' WHERE id=100;",
      "execution_time_ms": 2345
    },
    {
      "id": "Q125",
      "statement": "DELETE FROM sessions WHERE last_active < NOW() - INTERVAL '30 days';",
      "execution_time_ms": 1820
    },
    {
      "id": "Q126",
      "statement": "SELECT * FROM transactions WHERE amount > 1000;",
      "execution_time_ms": 2890
    }
  ]
}
JSON_METRICS

# Create query_metrics_schema.json
RUN cat > /home/user/db_metrics/query_metrics_schema.json <<'JSON_SCHEMA'
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "QueryMetrics",
  "type": "object",
  "required": ["queries"],
  "properties": {
    "queries": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "statement", "execution_time_ms"],
        "properties": {
          "id": {
            "type": "string"
          },
          "statement": {
            "type": "string"
          },
          "execution_time_ms": {
            "type": "number"
          }
        }
      }
    }
  }
}
JSON_SCHEMA

# Set appropriate permissions
RUN chmod 644 /home/user/db_metrics/query_metrics.json \
              /home/user/db_metrics/query_metrics_schema.json && \
    chmod 755 /home/user /home/user/db_metrics

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Container for DB metrics CLI exercise. Open a shell to begin working.
CMD echo "Container for DB metrics CLI exercise. Open a shell to begin working."