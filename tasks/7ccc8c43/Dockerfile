FROM ubuntu:22.04

# Labels
LABEL Author="Container Setup Bot"
LABEL Description="Environment for the 'Generate HTTP Status-Code Frequency Report' task with pytest pre-installed."

# --------------------------------------------------------------------- #
# 1. Install Python and pytest (plus minimal dependencies)
# --------------------------------------------------------------------- #
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        gnupg \
        build-essential && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# --------------------------------------------------------------------- #
# 2. Create the fixture directory structure and the pre-existing log
# --------------------------------------------------------------------- #
RUN mkdir -p /home/user/api_test/logs

RUN cat > /home/user/api_test/logs/responses.log <<'EOF'
2024-01-01T10:00:00Z GET /users 200
2024-01-01T10:00:01Z POST /users 201
2024-01-01T10:00:02Z GET /accounts 200
2024-01-01T10:00:03Z GET /users/123 404
2024-01-01T10:00:04Z GET /users 200
2024-01-01T10:00:05Z PUT /accounts/456 400
2024-01-01T10:00:06Z DELETE /users/789 200
2024-01-01T10:00:07Z GET /users 200
2024-01-01T10:00:08Z POST /login 400
2024-01-01T10:00:09Z GET /users 200
2024-01-01T10:00:10Z GET /accounts 500
2024-01-01T10:00:11Z GET /users 200
2024-01-01T10:00:12Z PATCH /accounts/456 500
2024-01-01T10:00:13Z POST /users 201
2024-01-01T10:00:14Z GET /transactions 400
EOF

# --------------------------------------------------------------------- #
# 3. Permissions
#    - Give write access to /home/user/api_test so the unprivileged agent
#      can create the "reports" directory and output file.
#    - The log directory and file remain read-only for safety.
# --------------------------------------------------------------------- #
RUN chmod 0777 /home/user/api_test && \
    chmod 0755 /home/user/api_test/logs && \
    chmod 0644 /home/user/api_test/logs/responses.log && \
    chmod 755 /home/user

# Ensure `python3` and `pytest` are in PATH (standard on Ubuntu once
# installed, but we make it explicit for clarity).
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"