FROM ubuntu:22.04

# Help text
# This Apptainer image supplies the initial state required for the exercise
# “Generate an aggregated error–code frequency report using sort + uniq”.
# Two log files are pre-installed in /home/user/logs/, and pytest is available
# for automated grading.

RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/logs

RUN cat > /home/user/logs/app1.log <<'EOF'
[2024-06-01 10:00:00] ERROR E102 Connection timeout
[2024-06-01 10:00:01] WARN  W301 Cache miss
[2024-06-01 10:00:02] ERROR E104 Invalid token
[2024-06-01 10:00:03] ERROR E102 Connection timeout
[2024-06-01 10:00:04] ERROR E108 Disk full
[2024-06-01 10:00:05] ERROR E102 Connection timeout
EOF

RUN cat > /home/user/logs/app2.log <<'EOF'
2024-06-01T11:00:00Z ERROR E108 Disk full
2024-06-01T11:00:01Z ERROR E102 Connection timeout
2024-06-01T11:00:02Z ERROR E104 Invalid token
2024-06-01T11:00:03Z ERROR E104 Invalid token
2024-06-01T11:00:04Z ERROR E114 Null pointer
2024-06-01T11:00:05Z ERROR E108 Disk full
2024-06-01T11:00:06Z ERROR E104 Invalid token
2024-06-01T11:00:07Z ERROR E114 Null pointer
2024-06-01T11:00:08Z ERROR E102 Connection timeout
2024-06-01T11:00:09Z ERROR E102 Connection timeout
EOF

RUN chmod 755 /home/user && \
    chmod 755 /home/user/logs && \
    chmod 644 /home/user/logs/app1.log /home/user/logs/app2.log

ENV HOME=/home/user