FROM ubuntu:22.04

# Labels
LABEL Author="Auto-generated for log-analysis task"
LABEL Description="Container providing initial state for log validation challenge"

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user named 'user' with matching home
RUN if ! id -u user >/dev/null 2>&1; then \
        useradd -m -d /home/user user; \
    fi

# Prepare the required directory structure
RUN mkdir -p /home/user/logs && \
    mkdir -p /home/user/output && \
    chmod 755 /home/user && \
    chmod 755 /home/user/logs && \
    chmod 755 /home/user/output

# Create the app.log with exact contents (LF endings)
RUN cat > /home/user/logs/app.log <<'EOF'
{"timestamp":"2023-10-01T12:00:00Z","level":"INFO","message":"Service started"}
{"timestamp":"2023-10-01T12:05:00Z","level":"ERROR","message":"Failed to connect to DB","error_code":"ERR001"}
{"timestamp":"2023-10-01T12:06:00Z","level":"ERROR","message":"Null pointer exception","error_code":"ERR002"}
{"timestamp":"2023-10-01T12:07:00Z","level":"ERROR","message":"Invalid input data"}
{"timestamp":"2023-10-01T12:08:00Z","level":"WARN","message":"High memory usage"}
EOF

# Set permissions for the log file
RUN chmod 644 /home/user/logs/app.log

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH