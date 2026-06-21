# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python 3, pip, and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create user home and backup directory
RUN mkdir -p /home/user/backup && \
    chmod 777 /home/user /home/user/backup

# Populate /home/user/backup/report.tsv with exact required content
RUN sh -c "{ \
    printf 'id\tfile\tsha256\tstatus\n'; \
    printf '1001\tconfig.tar.gz\t5d41402abc4b2a76b9719d911017c592\tsuccess\n'; \
    printf '1002\tdb.sql\t'; \
    printf 'da4b9237bacccdf19c0760cab7aec4a8359010b0\tsuccess\n'; \
    printf '1003\tlogs.zip\t'; \
    printf '77de68daecd823babbb58edb1c8e14d7106e83bb\tfailed\n'; \
    printf '1004\tpictures.tar\t'; \
    printf '1b6453892473a467d07372d45eb05abc2031647a\tsuccess\n'; \
} > /home/user/backup/report.tsv"

# Set read permissions on the source file
RUN chmod 644 /home/user/backup/report.tsv && \
    chmod 755 /home/user

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PATH="/usr/local/bin:$PATH"

# Run script equivalent
CMD echo "Container for the backup-integrity exercise." && \
    echo "Switch to /home/user/backup and follow the task instructions."