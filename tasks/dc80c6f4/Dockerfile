FROM ubuntu:22.04

# Help information:
# This container image sets up the initial filesystem state for
# the "backup-isolation" task.  It places the required CSV files
# under /home/user/datasets/raw/, installs pytest for grading,
# and ensures permissions allow modification by the unprivileged
# runtime user.

# Labels
LABEL Author="backup-task-setup"
LABEL Description="Environment prepared for the backup-isolation exercise"

# Update package lists and install needed tools
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        coreutils \
        findutils \
        gzip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Create the initial directory layout and fixture files
RUN set -e && \
    DATASETS="/home/user/datasets" && \
    RAW="$DATASETS/raw" && \
    OLD="$RAW/old" && \
    ARCHIVE="$RAW/archive" && \
    mkdir -p "$OLD" "$ARCHIVE" && \
    head -c 3072 /dev/zero > "$RAW/sales_backup.csv" && \
    head -c 2048 /dev/zero > "$OLD/sales_jan_backup.csv" && \
    head -c 1024 /dev/zero > "$OLD/customers_backup.csv" && \
    head -c 4096 /dev/zero > "$ARCHIVE/2021_sales_backup.csv" && \
    echo "Month,Sales" > "$RAW/sales_jan.csv" && \
    echo "Month,Sales" > "$RAW/sales_feb.csv" && \
    echo "CustomerID,Name" > "$RAW/customers.csv" && \
    echo "This directory contains raw CSV datasets." > "$RAW/readme.txt" && \
    chmod -R a+rwX /home/user

RUN chmod 755 /home/user