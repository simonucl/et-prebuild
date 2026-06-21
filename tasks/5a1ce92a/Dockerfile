# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels converted from %labels
LABEL Author="example@example.com" \
      Description="Initial state for ACTIVE users report task with Pytest installed."

# Install Python and Pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update -qq && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Create required directory structure and set permissions
RUN set -e && \
    mkdir -p /home/user/accounts && \
    chmod 755 /home/user && \
    chmod 755 /home/user/accounts

# Seed users_master.csv
RUN cat <<'EOF' > /home/user/accounts/users_master.csv
user_id,username,full_name,email,status
1,alice,Alice Walker,alice@example.com,ACTIVE
2,bob,Bob Stone,bob@example.com,INACTIVE
3,carol,Carol Smith,carol@example.com,ACTIVE
4,dave,David Johnson,dave@example.com,ACTIVE
5,erin,Erin Brown,erin@example.com,SUSPENDED
6,frank,Frank Harris,frank@example.com,ACTIVE
EOF

RUN chmod 644 /home/user/accounts/users_master.csv

# Seed departments.csv
RUN cat <<'EOF' > /home/user/accounts/departments.csv
username,department
alice,Engineering
bob,Sales
carol,HR
dave,Engineering
erin,Marketing
frank,Support
EOF

RUN chmod 644 /home/user/accounts/departments.csv

# Seed login_counts.csv
RUN cat <<'EOF' > /home/user/accounts/login_counts.csv
username,logins
alice,345
bob,127
carol,512
dave,98
erin,67
frank,250
EOF

RUN chmod 644 /home/user/accounts/login_counts.csv && \
    chmod 644 /home/user/accounts/*.csv

# Environment variables converted from %environment
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# %help
# Initial state for ACTIVE users report task with Pytest installed.