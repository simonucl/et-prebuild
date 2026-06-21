FROM ubuntu:22.04

# Help text
# This Apptainer image provides the initial workspace for the
# "parallelised security-scan" assignment.
# Pre-created resources:
#   • /home/user/sample_data/mock_netstat.txt
#   • /home/user/sample_data/mock_passwd
#   • /home/user/reports/  (writable, initially empty)
# Python 3 and pytest are installed for automated validation.

RUN set -e && \
    echo "Updating package lists and installing Python tooling..." && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
    && apt-get clean && rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir --upgrade pip pytest && \
    mkdir -p /home && \
    mkdir -p /home/user/sample_data && \
    mkdir -p /home/user/reports && \
    chmod 0777 /home/user/reports

RUN cat >/home/user/sample_data/mock_netstat.txt <<'EOF'
Proto LocalAddress  State  PID/Program
tcp   0.0.0.0:22    LISTEN 123/sshd
tcp   0.0.0.0:8080  LISTEN 456/nginx
udp   0.0.0.0:53           789/dnsmasq
EOF

RUN cat >/home/user/sample_data/mock_passwd <<'EOF'
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
user1:x:1000:1000:User One:/home/user1:/bin/bash
EOF

RUN chmod 0644 /home/user/sample_data/mock_netstat.txt && \
    chmod 0644 /home/user/sample_data/mock_passwd && \
    chmod 0755 /home/user/sample_data && \
    rm -f /home/user/reports/run_security_scan.sh \
          /home/user/reports/infra_security_report.yml \
          /home/user/reports/scan_exec_time.log || true && \
    chmod 755 /home/user

ENV PYTHONIOENCODING=utf-8