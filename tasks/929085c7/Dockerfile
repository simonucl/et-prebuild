FROM ubuntu:22.04

# Help text
# This container sets up the initial filesystem layout for the permissions
# hardening task. After building the image, the learner is expected to run a
# single compound shell command that:
#   1. Sets the directory /home/user/dev_utils to mode 2750 (set-gid bit on).
#   2. Sets each helper script (build.sh, test.sh, deploy.sh) to mode 750.
#   3. Generates /home/user/dev_utils/perm_report.txt with the required 4-line
#      permissions report.

LABEL Author="chatbot"
LABEL Description="Container prepared for permission-hardening exercise: initial state with /home/user/dev_utils and three helper scripts."

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/dev_utils && \
    chmod 0755 /home/user

RUN cat <<'EOF' >/home/user/dev_utils/build.sh
#!/bin/bash
echo 'build'
EOF

RUN cat <<'EOF' >/home/user/dev_utils/test.sh
#!/bin/bash
echo 'test'
EOF

RUN cat <<'EOF' >/home/user/dev_utils/deploy.sh
#!/bin/bash
echo 'deploy'
EOF

RUN chmod 0755 /home/user/dev_utils && \
    chmod 0644 /home/user/dev_utils/build.sh \
               /home/user/dev_utils/test.sh \
               /home/user/dev_utils/deploy.sh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin