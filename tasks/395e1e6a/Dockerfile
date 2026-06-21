FROM ubuntu:22.04

# Help text
# Container image for the “configuration migration” exercise.
# Initial state created:
#   • /home/user/old_service/conf/ with a.conf, b.conf, c.conf
#   • /home/user/migration_logs/ (empty)
# Directories not present until the learner creates them:
#   • /home/user/new_service/
#   • /home/user/backup_old_conf/
#   • /home/user/migration_logs/symlink_audit.log
# Pytest is pre-installed for automated grading.

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/old_service/conf && \
    mkdir -p /home/user/migration_logs

RUN cat >/home/user/old_service/conf/a.conf <<'EOF'
alpha=1
beta=2
EOF

RUN cat >/home/user/old_service/conf/b.conf <<'EOF'
gamma=3
delta=4
EOF

RUN cat >/home/user/old_service/conf/c.conf <<'EOF'
[service]
port=8080
EOF

RUN chmod -R a+rwX /home/user && \
    rm -rf /home/user/new_service || true && \
    rm -rf /home/user/backup_old_conf || true

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

RUN chmod 755 /home/user

CMD ["/bin/bash"]