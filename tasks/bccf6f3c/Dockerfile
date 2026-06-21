# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help section not provided, so none added

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip ca-certificates && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN set -eux && \
    if ! id -u user >/dev/null 2>&1; then \
        useradd -m -s /bin/bash user; \
    fi

RUN mkdir -p /home/user/finops/logs

RUN cat << 'EOF' > /home/user/finops/logs/cluster_usage.tsv
2023-08-01T12:00:00Z	cluster-a	payment	app-payment-api	ComputeHours	50	12.50
2023-08-01T12:05:00Z	cluster-b	payment	app-payment-api	NetworkEgressGB	30	45.00
2023-08-01T12:10:00Z	cluster-a	search	app-search-api	ComputeHours	70	20.00
2023-08-01T12:15:00Z	cluster-b	search	app-search-api	NetworkEgressGB	10	15.00
2023-08-01T12:20:00Z	cluster-c	auth	app-auth-api	ComputeHours	40	8.00
2023-08-01T12:25:00Z	cluster-c	auth	app-auth-api	NetworkEgressGB	5	7.50
2023-08-01T12:30:00Z	cluster-a	reporting	app-report-api	ComputeHours	100	25.00
2023-08-01T12:35:00Z	cluster-b	reporting	app-report-api	NetworkEgressGB	120	180.00
2023-08-01T12:40:00Z	cluster-a	analytics	app-analytics	ComputeHours	80	30.00
2023-08-01T12:45:00Z	cluster-b	analytics	app-analytics	NetworkEgressGB	60	90.00
EOF

RUN chown -R user:user /home/user/finops && \
    chmod -R a+rX /home/user/finops && \
    chmod 755 /home/user

CMD ["bash"]