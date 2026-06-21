# Author: fast_linecount_initial_state
# Description: Container image providing the initial filesystem layout for the fast_linecount exercise.
# Runscript message:
# This container prepares the initial state for the fast_linecount exercise.
# Execute an interactive shell with: apptainer shell <image>.sif

FROM ubuntu:22.04

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/scripts && \
    mkdir -p /home/user/data

RUN cat <<'EOF' > /home/user/scripts/slow_linecount.sh
#!/bin/bash
# slow_linecount.sh: Count lines in files passed as arguments (slow variant)
total=0
for f in "$@"; do
    lines=$(cat "$f" | wc -l)
    total=$((total + lines))
done
echo "$total"
EOF

RUN chmod 755 /home/user/scripts/slow_linecount.sh

RUN yes dummy | head -n 10000 > /home/user/data/file1.txt && \
    yes dummy | head -n 15000 > /home/user/data/file2.txt && \
    chmod 644 /home/user/data/file1.txt /home/user/data/file2.txt