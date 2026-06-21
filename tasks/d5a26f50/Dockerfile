FROM ubuntu:22.04

# Labels
LABEL Author="AI Generated"
LABEL Description="Container for diag CSV task – provides initial raw data and pytest."

# Environment
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Install required packages
RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create initial directory structure
RUN mkdir -p /home/user/diag/raw && \
    mkdir -p /home/user/diag/summary && \
    mkdir -p /home/user/diag/working

# Create memory_stat.log
RUN cat > /home/user/diag/raw/memory_stat.log <<'EOF'
MemTotal:       8173400 kB
MemFree:        204800 kB
MemAvailable:   3500000 kB
Buffers:        512000 kB
Cached:         1024000 kB
EOF

# Create disk_stat.log
RUN cat > /home/user/diag/raw/disk_stat.log <<'EOF'
Filesystem      Size  Used Avail Use% Mounted_on
/dev/sda1        40G   20G   18G  55% /
/dev/sda2        80G   60G   18G  77% /var
tmpfs           3.9G     0  3.9G   0% /run/user/1000
EOF

# Set permissions
RUN chmod 755 /home/user && \
    chmod -R 755 /home/user/diag