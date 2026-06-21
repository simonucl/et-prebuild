FROM ubuntu:22.04

# Help text
# This container image supplies the required input files located under
# /home/user/scan_data for the security-report exercise and has pytest
# pre-installed for automated assessment.

# Labels
LABEL Author="SecurityReportSetup"
LABEL Description="Container with prerequisite data for the security report task and pytest installed."

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/scan_data && \
    mkdir -p /home/user/security_scan && \
    chmod 1777 /home/user && \
    chmod 0755 /home/user/scan_data && \
    chmod 1777 /home/user/security_scan

RUN printf '5.15.0-test\n' > /home/user/scan_data/kernel.txt

RUN cat > /home/user/scan_data/port_scan.log <<'EOF'
Netid State      Recv-Q Send-Q Local Address:Port Peer Address:Port
tcp   LISTEN     0      128      0.0.0.0:22      0.0.0.0:*
tcp   LISTEN     0      128      0.0.0.0:8080    0.0.0.0:*
udp   UNCONN     0      0        0.0.0.0:68      0.0.0.0:*
EOF

RUN cat > /home/user/scan_data/sshd_config <<'EOF'
# Example sshd_config snippet
PermitRootLogin yes
PasswordAuthentication no
EOF

RUN chmod 0644 /home/user/scan_data/kernel.txt && \
    chmod 0644 /home/user/scan_data/port_scan.log && \
    chmod 0644 /home/user/scan_data/sshd_config && \
    chmod 755 /home/user

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"