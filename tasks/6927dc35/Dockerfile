# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Install Python and pytest
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Seed the initial filesystem that the student/agent will work on.
# ------------------------------------------------------------------
RUN mkdir -p -m 0777 /home/user/data && \
    truncate -s 1500000 /home/user/data/big1.txt && \
    truncate -s 1700000 /home/user/data/big2.log && \
    truncate -s    5000 /home/user/data/small.txt

RUN cat > /home/user/filelist.txt <<'EOF'
/home/user/data/big1.txt
/home/user/data/big2.log
/home/user/data/missing.doc
EOF

RUN chmod 0666 /home/user/filelist.txt && \
    chmod -R a+rwx /home/user

# ------------------------------------------------------------------
# Environment setup (from %environment)
# ------------------------------------------------------------------
RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PATH=/home/user/bin:$PATH

# ------------------------------------------------------------------
# Help
# ------------------------------------------------------------------
# This container provides a seeded filesystem under /home/user with
# sample data files and a file list for processing.