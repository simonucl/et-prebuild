# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help section was empty in the source; nothing to include.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        file \
        locales \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN sed -i 's/^# *en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && locale-gen

RUN mkdir -p /home/user/cloud/reports && \
    mkdir -p /home/user/cloud/logs

RUN cat << 'EOF' > /tmp/monthly_cost_utf8.csv
Name,Service,Cost(USD)
José Martínez,Compute Engine,1234.56
Zoë François,Cloud Storage,789.10
René Dupont,BigQuery,456.78
EOF

RUN iconv -f UTF-8 -t ISO-8859-1 /tmp/monthly_cost_utf8.csv -o /home/user/cloud/reports/monthly_cost_iso.csv

RUN rm /tmp/monthly_cost_utf8.csv

RUN chmod -R 0777 /home/user/cloud && \
    chmod 0777 /home/user

ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8