FROM ubuntu:22.04

# ------------------------------------------------------------------
# Fundamental tools + pytest for the grader
# ------------------------------------------------------------------
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Prepare the simulated CI filesystem under /home/user
# ------------------------------------------------------------------
RUN mkdir -p /home/user/mobile-build/artifacts && \
    mkdir -p /home/user/mobile-build/logs

# ---- Artefact files ------------------------------------------------
# Sizes are strict multiples of 1024 × 1024 as required by the tests.
RUN truncate -s 26214400  /home/user/mobile-build/artifacts/app-debug-1.apk && \
    truncate -s 31457280  /home/user/mobile-build/artifacts/app-release.apk && \
    truncate -s 29360128  /home/user/mobile-build/artifacts/old-test.ipa && \
    truncate -s 19922944  /home/user/mobile-build/artifacts/beta-small.apk

# ---- Log files -----------------------------------------------------
RUN truncate -s 12000  /home/user/mobile-build/logs/build-20230901.log && \
    truncate -s 8000   /home/user/mobile-build/logs/test-20230902.log && \
    truncate -s 15000  /home/user/mobile-build/logs/build-latest.log

# Mark the first two logs as "old" (>7 days) at build time.
RUN touch -d "$(date -d '10 days ago')" /home/user/mobile-build/logs/build-20230901.log && \
    touch -d "$(date -d '9 days ago')"  /home/user/mobile-build/logs/test-20230902.log && \
    chmod 755 /home/user

# ------------------------------------------------------------------
# Permissions: everything world-readable/executable for the CI user.
# ------------------------------------------------------------------
RUN chmod -R a+rX /home/user/mobile-build

# ------------------------------------------------------------------
# Create entrypoint script to refresh timestamp on container start
# ------------------------------------------------------------------
RUN cat <<'EOF' > /entrypoint.sh
#!/bin/sh
# Ensure the "new" log is always ≤ 7 days old by refreshing its mtime
# every time the container starts.
if [ -f /home/user/mobile-build/logs/build-latest.log ]; then
    touch /home/user/mobile-build/logs/build-latest.log
fi
exec "$@"
EOF

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/bin/bash"]