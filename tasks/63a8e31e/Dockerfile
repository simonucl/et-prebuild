# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# --------------------------------------------------------------------- #
# Apptainer build for Compliance-Officer exercise                         #
# Author="Apptainer build for Compliance-Officer exercise"               #
# --------------------------------------------------------------------- #

LABEL Author="Apptainer build for Compliance-Officer exercise"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# --------------------------------------------------------------------- #
# Prepare initial dataset for the compliance-officer exercise           #
# --------------------------------------------------------------------- #
RUN mkdir -p /home/user/audit_data

# hosts.csv
RUN cat > /home/user/audit_data/hosts.csv <<'EOF'
host_id,hostname,ip,owner
1,db-prod-01,10.0.0.11,finance
2,web-prod-02,10.0.0.21,marketing
3,db-test-01,10.0.1.11,finance
4,ci-server,10.0.2.5,devops
EOF

# vulnerabilities.csv
RUN cat > /home/user/audit_data/vulnerabilities.csv <<'EOF'
host_id,cve_id,severity,fix_available
1,CVE-2022-0001,Critical,Yes
1,CVE-2022-0002,High,Yes
2,CVE-2021-1111,Critical,No
3,CVE-2020-2222,Medium,Yes
4,CVE-2019-3333,Low,No
EOF

# Ensure reasonable default permissions
RUN chmod -R 755 /home/user

ENV PYTHONUNBUFFERED=1