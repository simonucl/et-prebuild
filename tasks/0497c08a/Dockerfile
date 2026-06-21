FROM ubuntu:22.04

# Install requirements
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial filesystem state
RUN mkdir -p /home/user/build_logs

# appserver_build.log
RUN cat >/home/user/build_logs/appserver_build.log <<'EOF'
2023-07-19 14:20:55 [INFO ] Starting build for appserver
2023-07-19 14:20:56 [WARN ] Deprecated API usage detected
2023-07-19 14:20:57 [INFO ] Compiling modules...
2023-07-19 14:20:58 [ERROR] Failed to copy artifact artifact-xyz.jar
2023-07-19 14:21:10 Build step completed
2023-07-19 14:21:15 [INFO ] Running unit tests...
2023-07-19 14:21:20 [ERROR] Test suite failed for module security
2023-07-19 14:21:45  Tests run: 230, Failures: 3, Errors: 0, Skipped: 1
2023-07-19 14:22:12 Build step failed with code E5678
2023-07-19 14:22:20 [INFO ] Build finished with status FAILED
EOF

# db_build.log
RUN cat >/home/user/build_logs/db_build.log <<'EOF'
2023-07-19 14:00:01 [INFO ] Starting build for database layer
2023-07-19 14:00:05 [WARN ] Outdated driver version detected
2023-07-19 14:00:07 [INFO ] Executing migrations...
2023-07-19 14:00:09 Script completed successfully
2023-07-19 14:00:10 [ERROR] Migration 20230719_add_index.sql failed
2023-07-19 14:00:11 Error code E3141 encountered during migration
2023-07-19 14:00:15 [INFO ] Build finished with status FAILED
EOF

# ui_build.log
RUN cat >/home/user/build_logs/ui_build.log <<'EOF'
2023-07-19 13:40:10 [INFO ] Starting build for UI
2023-07-19 13:40:12 [INFO ] Installing dependencies...
2023-07-19 13:40:18 [WARN ] Package "left-pad" is deprecated
2023-07-19 13:40:28 [INFO ] Running lint...
2023-07-19 13:40:30  Lint failed at component Navbar with E0987
2023-07-19 13:40:33 [INFO ] Running unit tests...
2023-07-19 13:40:45 [ERROR] 12 tests failed
2023-07-19 13:40:55 [INFO ] Build finished with status FAILED
EOF

# Permissions
RUN chmod 644 /home/user/build_logs/*.log && \
    chmod 755 /home/user/build_logs && \
    chmod 755 /home/user

# Environment
ENV PATH="/home/user/.local/bin:${PATH}"

# Run script
CMD echo "This container is set up for the build-log parsing exercise." && \
    echo "Raw logs are located in /home/user/build_logs." && \
    echo "Develop your solution script and run it inside the container."