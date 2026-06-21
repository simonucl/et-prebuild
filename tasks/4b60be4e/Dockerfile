FROM ubuntu:22.04

# Labels
LABEL Author="AI-generated"
LABEL Description="Environment for log-processing task with pytest pre-installed."

# --- Base tooling --------------------------------------------------------
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip

# --- Python test framework ----------------------------------------------
RUN pip3 install --no-cache-dir pytest

# --- Prepare initial filesystem state -----------------------------------
RUN mkdir -p /home/user/logs

# Pre-generated raw availability log (tab-separated, newline-terminated)
RUN cat <<'EOF' > /home/user/logs/uptime_raw.tsv
timestamp	service	status	response_ms
2024-04-01T00:00:00Z	auth-api	OK	120
2024-04-01T00:05:00Z	payment-api	FAIL	-
2024-04-01T00:10:00Z	auth-api	OK	110
2024-04-01T00:15:00Z	payment-api	OK	210
2024-04-01T00:20:00Z	auth-api	OK	115
EOF

# Permissions: directory must be writable by the unprivileged learner
RUN chmod 777 /home/user/logs && \
    chmod 644 /home/user/logs/uptime_raw.tsv && \
    chmod 755 /home/user

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"