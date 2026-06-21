FROM ubuntu:22.04

# Container for the "CSV consolidation" task.
# On every start-up it guarantees that:
#   * /home/user/scans/open_ports.csv
#   * /home/user/scans/vulns.csv
# exist with the correct contents and permissions.
# Pytest is pre-installed for automatic grading.

LABEL Author="PenTest Initial-State Container"

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && \
    chmod 755 /home/user

RUN cat << 'EOF' > /usr/local/bin/setup_task_state.sh
#!/bin/sh
set -e

TARGET_HOME="/home/user"
SCANS_DIR="$TARGET_HOME/scans"

# Create directory if missing
mkdir -p "$SCANS_DIR"
chmod 755 "$SCANS_DIR"

# ------------------------------------------------------------------
# open_ports.csv (permissions 644)
OPEN_FILE="$SCANS_DIR/open_ports.csv"
if [ ! -f "$OPEN_FILE" ]; then
cat > "$OPEN_FILE" <<'CSV'
IP,Port,Protocol,Service
192.168.1.10,22,tcp,ssh
192.168.1.10,80,tcp,http
192.168.1.20,445,tcp,smb
192.168.1.20,3389,tcp,rdp
CSV
chmod 644 "$OPEN_FILE"
fi

# ------------------------------------------------------------------
# vulns.csv (permissions 644)
VULN_FILE="$SCANS_DIR/vulns.csv"
if [ ! -f "$VULN_FILE" ]; then
cat > "$VULN_FILE" <<'CSV'
Service,CVE,Severity
ssh,CVE-2018-15473,High
smb,CVE-2020-0796,Critical
http,CVE-2021-26855,High
rdp,CVE-2019-0708,Critical
CSV
chmod 644 "$VULN_FILE"
fi
EOF

RUN chmod +x /usr/local/bin/setup_task_state.sh

# Run the setup script to create initial state
RUN /usr/local/bin/setup_task_state.sh

WORKDIR /home/user