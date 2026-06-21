FROM ubuntu:22.04

# Help:
# This container provides the starting state for the “user-accounts” task.
# It includes:
#   - /home/user/data/user_accounts.csv (pre-populated with 5 lines)
#   - pytest installed for automated grading

LABEL Author="YourName"
LABEL Description="Environment for the user-accounts task with initial data and pytest installed."

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/data

RUN cat > /home/user/data/user_accounts.csv <<'EOF'
username,email,role
alice,alice@example.com,editor
bob,bob@example.com,admin
carol,carol@example.com,viewer
dave,dave@example.com,editor
EOF

RUN chmod 755 /home/user && \
    chmod 755 /home/user/data && \
    chmod 644 /home/user/data/user_accounts.csv