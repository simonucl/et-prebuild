FROM ubuntu:22.04

# Install required software
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        gnupg \
        python3-pip \
        ca-certificates && \
    pip install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial workspace expected by the tests
RUN mkdir -p /home/user/compliance_work && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/compliance_work

# Seed file: client_data.csv
RUN cat >/home/user/compliance_work/client_data.csv <<'EOF'
id,name,balance
101,Alice,2500
102,Bob,1750
EOF

# Seed file: code_of_conduct.txt
RUN cat >/home/user/compliance_work/code_of_conduct.txt <<'EOF'
ACME CORPORATION – CODE OF CONDUCT
1. We comply with all applicable laws.
2. We act with honesty and integrity.
3. We respect confidentiality at every level.
EOF

# Seed file: detached signature
RUN cat >/home/user/compliance_work/code_of_conduct.txt.sig <<'EOF'
dummy signature
EOF

RUN chmod 0666 /home/user/compliance_work/* && \
    chmod 0777 /home/user/compliance_work

# Environment variables
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1

RUN chmod 755 /home/user