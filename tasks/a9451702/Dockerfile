FROM ubuntu:22.04

# Labels
LABEL Author="evidence_bundle_setup"
LABEL Description="Container prepared for the incident-response evidence extraction exercise."

# Basic utilities and Python tooling
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        tar \
        gzip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# Create a regular, non-privileged user expected by the exercise
RUN useradd -m -u 1000 -s /bin/bash user

# Build the evidence bundle exactly as described
RUN mkdir -p /home/user/evidence && \
    mkdir -p /tmp/evidence_staging/nginx

# 1. auth.log.2023-08-11
RUN cat <<'EOF' > /tmp/evidence_staging/auth.log.2023-08-11
Aug 11 02:15:47 sshd[2318]: Accepted password for analyst from 10.0.0.42 port 55218 ssh2
EOF

# 2. syslog.2023-08-11
RUN cat <<'EOF' > /tmp/evidence_staging/syslog.2023-08-11
Aug 11 02:16:02 kernel: audit: type=1105 msg=audit(1691727362.123:98): audit_pid=1 ...
EOF

# 3. nginx/access.log
RUN cat <<'EOF' > /tmp/evidence_staging/nginx/access.log
10.0.0.17 - - [11/Aug/2023:02:17:03 +0000] "GET /index.html HTTP/1.1" 200 612 "-" "curl/7.58.0"
EOF

# 4. nginx/error.log
RUN cat <<'EOF' > /tmp/evidence_staging/nginx/error.log
2023/08/11 02:17:07 [error] 5342#0: *1 open() "/var/www/html/favicon.ico" failed (2: No such file or directory)...
EOF

# Create the tar archive (then gzip-compress it) with the correct paths
RUN tar -C /tmp/evidence_staging \
        -cf /home/user/evidence/evidence_bundle.tar \
        auth.log.2023-08-11 \
        syslog.2023-08-11 \
        nginx && \
    gzip -9 /home/user/evidence/evidence_bundle.tar

# Clean up staging area and adjust ownership so the unprivileged user
# can access everything during runtime.
RUN rm -rf /tmp/evidence_staging && \
    chown -R 1000:1000 /home/user && \
    chmod 755 /home/user

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

WORKDIR /home/user

CMD ["/bin/bash"]