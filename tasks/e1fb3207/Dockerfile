FROM ubuntu:22.04

# Basic tooling
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && \
    pip3 install --no-cache-dir pytest

# Create unprivileged user (uid/gid = 1000) that will own the sample
# log tree. The runtime user on the platform usually has this UID, so
# ownership will match transparently.
RUN groupadd -g 1000 user || true && \
    useradd -m -u 1000 -g 1000 user || true

# Directory hierarchy expected by the tests
RUN mkdir -p /home/user/app1/logs && \
    mkdir -p /home/user/app2/logs && \
    mkdir -p /home/user/app3/data && \
    mkdir -p /home/user/archive && \
    mkdir -p /home/user/diagnostics

# Create qualifying log files (≥1024 bytes)
RUN dd if=/dev/zero bs=1024 count=2 2>/dev/null > /home/user/app1/logs/server.log && \
    dd if=/dev/zero bs=1024 count=2 2>/dev/null > /home/user/app1/logs/access.log && \
    dd if=/dev/zero bs=1024 count=2 2>/dev/null > /home/user/app2/logs/error.txt && \
    dd if=/dev/zero bs=1024 count=2 2>/dev/null > /home/user/app2/logs/trace.log && \
    dd if=/dev/zero bs=1024 count=2 2>/dev/null > /home/user/archive/old.log

# Create decoy / non-qualifying files (<1024 bytes)
RUN echo "placeholder" > /home/user/app1/logs/debug-20230802.log && \
    echo "placeholder" > /home/user/app2/logs/README.md && \
    echo "placeholder" > /home/user/app3/data/datafile.log

# Permissions: make sure everything is owned by uid/gid 1000:1000 and
# world-readable so the unprivileged tester can access them.
RUN chown -R 1000:1000 /home/user && \
    chmod -R u+rwX,go+rX /home/user

# Environment setup
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Set permissions on /home/user at runtime
RUN chmod 755 /home/user