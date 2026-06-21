FROM ubuntu:22.04

# Help / labels
LABEL Author="AI Assistant"
LABEL Description="Container image with initial state for API-key rotation task (users.csv present, pytest installed)"

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/credentials && \
    chmod 0777 /home/user/credentials

RUN cat <<'EOF' > /home/user/credentials/users.csv
user_id,username,old_key
1,alice,akjdh231
2,bob,98dfjKsl
3,charlie,QWERTY999
EOF

RUN chmod 0644 /home/user/credentials/users.csv && \
    chmod 755 /home/user

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"