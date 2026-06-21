FROM ubuntu:22.04

# Help / runscript note
# Container ready. Parse the logs in /home/user/backup_logs as per the task.

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/backup_logs

RUN cat > /home/user/backup_logs/restore_20240601.log <<'EOF'
2024-06-01 00:00:01 START /srv/data size=15728640
2024-06-01 00:05:02 END   /srv/data duration=301s status=SUCCESS
2024-06-01 01:10:00 START /srv/media size=31457280
2024-06-01 01:30:31 END   /srv/media duration=1231s status=FAILURE code=E42
EOF

RUN cat > /home/user/backup_logs/restore_20240602.log <<'EOF'
2024-06-02 02:00:00 START /srv/data size=15728640
2024-06-02 02:05:03 END   /srv/data duration=303s status=SUCCESS
2024-06-02 03:15:10 START /srv/docs size=1048576
2024-06-02 03:18:00 END   /srv/docs duration=170s status=SUCCESS
2024-06-02 04:00:00 START /srv/media size=41943040
2024-06-02 04:30:05 END   /srv/media duration=1805s status=SUCCESS
EOF

RUN cat > /home/user/backup_logs/restore_20240603.log <<'EOF'
2024-06-03 00:00:05 START /srv/data size=15728640
2024-06-03 00:05:10 END   /srv/data duration=305s status=FAILURE code=E13
2024-06-03 01:20:00 START /srv/media size=10485760
2024-06-03 01:22:10 END   /srv/media duration=130s status=SUCCESS
EOF

RUN chmod -R a+rwX /home/user && \
    [ -d /home/user/restore_reports ] && rm -rf /home/user/restore_reports || true && \
    chmod 755 /home/user

ENV LC_ALL=C