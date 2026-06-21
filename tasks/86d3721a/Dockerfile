FROM ubuntu:22.04

# Help: Converted from Apptainer definition file

ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=utf-8

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && \
    mkdir -p /home/user/ci_cd_diagnostics/raw

RUN cat > /home/user/ci_cd_diagnostics/raw/snapshot.txt <<'EOF'
TIMESTAMP=2025-04-01T12:30:00Z
CPU_USER=12.5
CPU_SYSTEM=3.1
CPU_IDLE=84.4
MEM_TOTAL=7989
MEM_USED=3120
MEM_FREE=4869
SWAP_TOTAL=2048
SWAP_USED=128
DISK_ROOT_USED_PCT=45
DISK_VAR_USED_PCT=67
DISK_HOME_USED_PCT=38
TOP_PROC_MEM=python3:512M
TOP_PROC_CPU=node:25.3
NET_RX_KBPS=120.5
NET_TX_KBPS=98.7

TIMESTAMP=2025-04-01T12:45:00Z
CPU_USER=15.8
CPU_SYSTEM=4.0
CPU_IDLE=80.2
MEM_TOTAL=7989
MEM_USED=3421
MEM_FREE=4568
SWAP_TOTAL=2048
SWAP_USED=256
DISK_ROOT_USED_PCT=46
DISK_VAR_USED_PCT=70
DISK_HOME_USED_PCT=39
TOP_PROC_MEM=java:640M
TOP_PROC_CPU=python3:27.9
NET_RX_KBPS=150.9
NET_TX_KBPS=110.3
EOF

RUN chmod 644 /home/user/ci_cd_diagnostics/raw/snapshot.txt && \
    chmod 755 /home/user && \
    chmod 755 /home/user/ci_cd_diagnostics && \
    chmod 755 /home/user/ci_cd_diagnostics/raw