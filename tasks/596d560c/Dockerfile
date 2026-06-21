# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# 1. Install Python + pytest
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# 2. Create initial exercise filesystem layout
# ------------------------------------------------------------------
RUN mkdir -p /home/user/network

# firewall_rules.conf (exact baseline content, final newline included)
RUN cat > /home/user/network/firewall_rules.conf <<'EOF'
# Simulated iptables-save output generated on 2024-01-01
*filter
:INPUT DROP [0:0]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT -p tcp --dport 22 -j ACCEPT
-A INPUT -p tcp --dport 23 -j ACCEPT
-A INPUT -p tcp --dport 80 -j ACCEPT
-A INPUT -j DROP
COMMIT
EOF

# nmap_scan.txt (auxiliary file; not modified by the student)
RUN cat > /home/user/network/nmap_scan.txt <<'EOF'
Starting Nmap 7.80 ( https://nmap.org ) at 2024-01-02 00:00 UTC
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000098s latency).
Not shown: 997 closed ports
PORT   STATE SERVICE
22/tcp open  ssh
23/tcp open  telnet
80/tcp open  http
EOF

# ------------------------------------------------------------------
# 3. Permissions: allow the non-root runtime user to modify contents
# ------------------------------------------------------------------
RUN chmod 0777 /home/user/network && \
    chmod 0666 /home/user/network/firewall_rules.conf /home/user/network/nmap_scan.txt && \
    chmod 755 /home/user

# ------------------------------------------------------------------
# Labels
# ------------------------------------------------------------------
LABEL Author="ExampleAuthor" \
      Description="Initial state for “Disable inbound Telnet” exercise"

# ------------------------------------------------------------------
# Help
# ------------------------------------------------------------------
# This image provides the starting filesystem needed for the
# “Disable inbound Telnet” network-security task.
#
# The directory /home/user/network contains:
#   • firewall_rules.conf   (baseline iptables ruleset)
#   • nmap_scan.txt         (reference scan output)
#
# No backup or remediation log exists yet; the student must create them.
# pytest is pre-installed for automated grading.