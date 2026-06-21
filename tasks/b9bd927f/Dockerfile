# syntax=docker/dockerfile:1
# Converted from Apptainer definition file
FROM ubuntu:22.04

# Help text
# This container provides the initial state for the ".edu customer filter" exercise.
# It contains:
#   - /home/user/data/sales.csv  – source data (header + 10 rows)
#   - /home/user/output/         – empty, writable directory for results
# pytest is installed so that the supplied test-suite can be executed.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/data && \
    mkdir -p /home/user/output && \
    chmod 0777 /home/user/output

RUN cat << 'EOF' > /home/user/data/sales.csv
order_id,customer,email,amount
1001,Alice Smith,alice.smith@example.com,39.95
1002,Bob Jones,bjones@STATE.EDU,15.00
1003,Carla Ruiz,carla@college.edu,22.50
1004,David Zhang,dzhang@corp.com,85.00
1005,Eva Adams,evadams@school.edu,13.20
1006,Fred Grant,grantf@business.org,44.10
1007,Gina Hall,gina.hall@university.EDU,19.99
1008,Henry Ito,henry@random.net,33.33
1009,Ivy Keller,ivy.keller@tech.com,72.00
1010,Jack Lee,jlee@liberalarts.edu,18.75
EOF

RUN chmod 0644 /home/user/data/sales.csv && \
    chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH