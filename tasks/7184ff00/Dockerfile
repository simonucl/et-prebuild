# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Basic tooling
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Prepare filesystem layout required by the assignment
# ------------------------------------------------------------------
# Create writable home for the student
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Create scans directory
RUN mkdir -p /home/user/scans && \
    chmod 0755 /home/user/scans

# Populate the fixture log file
RUN cat > /home/user/scans/nmap_scan.log <<'EOF'
192.168.1.10:22/tcp open ssh (protocol 2.0) | vuln: openssh-cve-2018-15473
192.168.1.12:80/tcp open http apache 2.4.29 | vuln: cve-2021-41773
192.168.1.15:443/tcp open https nginx 1.14.0
192.168.1.20:23/tcp closed telnet
192.168.1.30:3306/tcp open mysql 5.7.31 | vuln: cve-2019-5480
192.168.1.35:25/tcp open smtp postfix
192.168.1.40:8080/tcp open http-proxy squid 3.5 | vuln: cve-2019-12529
10.0.0.5:53/udp open domain bind 9.10.3-P4
10.0.0.8:110/tcp open pop3 dovecot 2.3.13 | vuln: cve-2020-10967
10.0.0.9:995/tcp open pop3s dovecot 2.3.13
10.0.0.10:143/tcp open imap dovecot 2.3.13 | vuln: cve-2020-25275
10.0.0.20:21/tcp open ftp vsftpd 3.0.3 | vuln: cve-2011-2523
EOF

RUN chmod 0644 /home/user/scans/nmap_scan.log

# ------------------------------------------------------------------
# Environment
# ------------------------------------------------------------------
RUN chmod 0755 /home/user
ENV PATH=/home/user:$PATH

# ------------------------------------------------------------------
# Labels
# ------------------------------------------------------------------
LABEL Author="ChatGPT" \
      Description="Environment for the critical-vulnerability extraction task"