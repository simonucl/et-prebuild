# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare directory tree and initial log files
RUN mkdir -p /home/user/cloud_migration/logs

RUN cat <<'EOF' > /home/user/cloud_migration/logs/auth-service_20231015.log
[2023-10-15 10:00:01] auth-service mig-001 SUCCESS 450
[2023-10-15 10:05:22] auth-service mig-002 FAILED 300
[2023-10-15 10:15:10] auth-service mig-003 SUCCESS 500
EOF

RUN cat <<'EOF' > /home/user/cloud_migration/logs/payment-service_20231015.log
[2023-10-15 10:01:30] payment-service mig-010 SUCCESS 800
[2023-10-15 10:07:45] payment-service mig-011 SUCCESS 750
[2023-10-15 10:11:05] payment-service mig-012 FAILED 900
[2023-10-15 10:12:55] payment-service mig-013 FAILED 880
EOF

RUN cat <<'EOF' > /home/user/cloud_migration/logs/auth-service_20231016.log
[2023-10-16 11:00:11] auth-service mig-004 SUCCESS 460
[2023-10-16 11:05:55] auth-service mig-005 FAILED 350
EOF

RUN cat <<'EOF' > /home/user/cloud_migration/logs/payment-service_20231016.log
[2023-10-16 11:02:01] payment-service mig-014 SUCCESS 780
EOF

RUN find /home/user/cloud_migration/logs -type f -exec sed -i -e '$a\' {} \;

RUN chmod -R a+rwX /home/user && chmod 755 /home/user

ENV PATH="/usr/local/bin:/usr/bin:${PATH}"
ENV PYTHONUNBUFFERED=1