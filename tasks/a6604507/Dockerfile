# Help
# This container image is pre-configured for the “clean customers CSV” coding exercise.
# Dataset location: /home/user/data/raw/customers.csv
# pytest is available for the test harness.

FROM ubuntu:22.04

ENV PATH="$PATH:/usr/local/bin"

RUN set -e \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN set -e \
    && if ! id -u 1000 >/dev/null 2>&1; then \
        useradd -m -u 1000 -s /bin/bash user; \
    fi

RUN chmod 755 /home/user || true

RUN mkdir -p /home/user/data/raw

RUN cat > /home/user/data/raw/customers.csv <<'EOF'
customer_id,first_name,last_name,email,age
1,John,Doe,john.doe@example.com,28
2,Jane,NULL,jane@example.com,34
3,Bob,Smith,NULL,45
4,Anna,Adams,anna.adams@example.com,31
5,NULL,White,white@example.com,27
6,Mark,Brown,mark.brown@example.com,NULL
EOF

RUN chmod 644 /home/user/data/raw/customers.csv \
    && chown 1000:1000 /home/user/data/raw/customers.csv || true

RUN mkdir -p /home/user/data \
    && chmod 777 /home/user/data \
    && chown 1000:1000 /home/user/data || true

RUN rm -rf /home/user/data/clean || true

LABEL Author="container-prep bot"
LABEL Description="Environment for the 'clean customers CSV' exercise with pytest pre-installed."