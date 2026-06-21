# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels
LABEL Author="OpenAI ChatGPT" \
      Description="Container for compliance-audit shell task with pytest and initial mock_passwd."

# Post section
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/audit_data && \
    chmod 0777 /home/user && \
    chmod 0755 /home/user/audit_data

RUN cat > /home/user/audit_data/mock_passwd <<'EOF'
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
alice:x:1000:1000:Alice:/home/alice:/bin/bash
bob:x:1001:1001:Bob:/home/bob:/bin/zsh
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
john:x:1002:1002:John:/home/john:/bin/false
jane:x:1003:1003:Jane:/home/jane:/bin/bash
EOF

RUN chmod 0644 /home/user/audit_data/mock_passwd

# Environment
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH