# Author: Apptainer Prep Bot
# Description: Container image that provides the initial state for the deployment-bundle task, including test input files and pytest installed.

FROM ubuntu:22.04

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN set -e && \
    echo "Updating package index and installing Python tooling..." && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip ca-certificates curl && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest

RUN set -e && \
    echo "Creating initial release tree..." && \
    BASE_DIR="/home/user/releases/2024-06-01" && \
    mkdir -p "${BASE_DIR}"

# auth-service
RUN AUTH_DIR="/home/user/releases/2024-06-01/auth-service" && \
    mkdir -p "${AUTH_DIR}" && \
    cat <<'EOF' > "${AUTH_DIR}/manifest.yaml"
metadata:
  service: auth-service
  version: "2.1.0"
  container:
    port: 7000
EOF

RUN AUTH_DIR="/home/user/releases/2024-06-01/auth-service" && \
    cat <<'EOF' > "${AUTH_DIR}/config.env"
DB_HOST=auth-db.internal
DB_PORT=5432
JWT_SECRET=s3cr3t
LOG_LEVEL=INFO
EOF

# billing-service
RUN BILL_DIR="/home/user/releases/2024-06-01/billing-service" && \
    mkdir -p "${BILL_DIR}" && \
    cat <<'EOF' > "${BILL_DIR}/manifest.yaml"
metadata:
  service: billing-service
  version: "3.4.2"
  container:
    port: 7100
EOF

RUN BILL_DIR="/home/user/releases/2024-06-01/billing-service" && \
    cat <<'EOF' > "${BILL_DIR}/config.env"
DB_HOST=billing-db.internal
DB_PORT=5432
PAYMENT_GATEWAY_TOKEN=abcd1234
LOG_LEVEL=INFO
CURRENCY=USD
EOF

# report-service
RUN REPORT_DIR="/home/user/releases/2024-06-01/report-service" && \
    mkdir -p "${REPORT_DIR}" && \
    cat <<'EOF' > "${REPORT_DIR}/manifest.yaml"
metadata:
  service: report-service
  version: "1.8.0"
  container:
    port: 7200
EOF

RUN REPORT_DIR="/home/user/releases/2024-06-01/report-service" && \
    cat <<'EOF' > "${REPORT_DIR}/config.env"
DB_HOST=report-db.internal
DB_PORT=5432
REPORT_CACHE_SIZE=512
LOG_LEVEL=DEBUG
EOF

RUN chmod -R 755 /home/user && \
    find /home/user -type f -exec chmod 644 {} +

RUN chmod 755 /home/user

CMD echo "Container for deployment-bundle task." && echo "You can now start solving the assignment."