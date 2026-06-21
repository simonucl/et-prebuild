FROM ubuntu:22.04

# Help section from Apptainer
# Container for log-analysis exercise.
# Open a shell or run the provided test suite with: pytest -q

RUN set -e && \
    echo "Updating package lists and installing Python tooling..." && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    echo "Installing pytest so that test suites can run inside the container..." && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/app/logs

RUN cat > /home/user/app/logs/app.log <<'EOF'
2023-09-15 10:15:21 [INFO] Application started
2023-09-15 10:15:22 [INFO] Loading configuration
2023-09-15 10:15:23 [WARN] Deprecated config option used
2023-09-15 10:15:24 [ERROR] Failed to connect to database
2023-09-15 10:15:25 [INFO] Retrying connection
2023-09-15 10:15:26 [ERROR] Failed to connect to database
2023-09-15 10:15:27 [WARN] Using fallback settings
2023-09-15 10:15:28 [INFO] Starting processing loop
2023-09-15 10:16:00 [INFO] Processed 100 records
2023-09-15 10:16:05 [ERROR] Unexpected null pointer
2023-09-15 10:16:10 [INFO] Shutting down
2023-09-15 10:16:11 [INFO] Application stopped
2023-09-16 09:00:00 [INFO] Application started
2023-09-16 09:00:01 [WARN] Low disk space
2023-09-16 09:00:02 [ERROR] Disk write failed
2023-09-16 09:00:03 [INFO] Cleanup complete
EOF

RUN chmod 0777 /home/user/app/logs && \
    chmod 0644 /home/user/app/logs/app.log && \
    mkdir -p /home/user && chmod 755 /home/user

ENV PATH="/usr/local/bin:$PATH"

CMD echo "Container for log-analysis exercise." && echo "Open a shell or run the provided test suite with:  pytest -q"