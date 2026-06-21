FROM ubuntu:22.04

# ---- System packages ----
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        zip \
        unzip \
        jq \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ---- Python tooling ----
RUN pip3 install --no-cache-dir pytest

# ---- Incident-response data set ----
RUN mkdir -p /home/user/ir_data

WORKDIR /tmp

# 1. auth.log.csv
RUN cat > auth.log.csv <<'EOF'
timestamp,username,status,source_ip
2024-06-01T10:00:01Z,alice,success,10.0.0.2
2024-06-01T10:05:22Z,bob,failed,10.0.0.3
2024-06-01T10:06:30Z,bob,failed,10.0.0.3
2024-06-01T10:07:55Z,charlie,failed,192.168.1.5
2024-06-01T10:09:11Z,dave,success,172.16.0.4
2024-06-01T10:10:42Z,bob,failed,10.0.0.3
2024-06-01T10:11:53Z,alice,failed,10.0.0.2
2024-06-01T10:12:14Z,charlie,failed,192.168.1.5
2024-06-01T10:13:27Z,erin,failed,10.0.0.6
EOF

# 2. network.log.csv
RUN cat > network.log.csv <<'EOF'
timestamp,src_ip,dst_ip,dst_port,protocol
2024-06-01T10:05:01Z,10.0.0.3,8.8.8.8,53,udp
2024-06-01T10:05:05Z,10.0.0.3,203.0.113.99,443,tcp
2024-06-01T10:07:44Z,192.168.1.5,104.26.10.78,80,tcp
2024-06-01T10:08:33Z,10.0.0.2,198.51.100.42,22,tcp
2024-06-01T10:09:50Z,10.0.0.6,203.0.113.99,80,tcp
2024-06-01T10:11:02Z,10.0.0.2,192.0.2.15,443,tcp
EOF

# 3. processes.json
RUN cat > processes.json <<'EOF'
[
  {"pid":123,"process_name":"sshd","user":"root"},
  {"pid":234,"process_name":"apache2","user":"www-data"},
  {"pid":345,"process_name":"nc","user":"bob"},
  {"pid":456,"process_name":"python3","user":"charlie"},
  {"pid":567,"process_name":"malware_x","user":"erin"}
]
EOF

# Package them into logs_bundle.zip
RUN zip -qj /home/user/ir_data/logs_bundle.zip auth.log.csv network.log.csv processes.json && \
    rm -f auth.log.csv network.log.csv processes.json

# Supporting text files - blacklist_ips.txt
RUN cat > /home/user/ir_data/blacklist_ips.txt <<'EOF'
203.0.113.99
198.51.100.42
EOF

# Supporting text files - suspicious_proc.txt
RUN cat > /home/user/ir_data/suspicious_proc.txt <<'EOF'
nc
malware_x
EOF

# Permissions: ensure any unprivileged user can read/write inside /home/user/ir_data
RUN chmod -R a+rwX /home/user/ir_data && \
    chmod 755 /home/user

WORKDIR /home/user

# Default command — start an interactive shell unless overridden
CMD ["bash"]