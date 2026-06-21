# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Install Python and pytest
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Create the required input directory and set permissions
# ------------------------------------------------------------------
RUN mkdir -p /home/user/data && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/data

# ------------------------------------------------------------------
# Create the TSV data file
# ------------------------------------------------------------------
RUN cat >/home/user/data/sales_2023.tsv <<'EOF'
order_id	product	units	unit_price	region
1001	Widget-A	25	9.99	NA
1002	Widget-B	50	19.99	EU
1003	Widget-C	10	4.99	APAC
EOF

RUN chmod 0666 /home/user/data/sales_2023.tsv

# ------------------------------------------------------------------
# Environment setup (no special environment variables needed)
# ------------------------------------------------------------------
RUN chmod 755 /home/user