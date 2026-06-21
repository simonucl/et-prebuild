# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Update package list and install Python + pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create /home/user with correct permissions
RUN mkdir -p /home/user && chmod 0755 /home/user

# Create ci_cd log hierarchy
RUN mkdir -p /home/user/ci_cd/logs && \
    chmod 0700 /home/user/ci_cd && \
    chmod 0700 /home/user/ci_cd/logs

# Populate build.log
RUN cat > /home/user/ci_cd/logs/build.log << 'EOF'
2023-06-01T10:30:25Z Build #101 SUCCESS
2023-06-01T11:00:20Z Build #102 FAILED
2023-06-01T11:30:42Z Build #103 SUCCESS
2023-06-01T12:00:05Z Build #104 SUCCESS
2023-06-01T12:30:44Z Build #105 ABORTED
2023-06-01T13:00:22Z Build #106 FAILED
2023-06-01T13:30:51Z Build #107 SUCCESS
2023-06-01T14:00:30Z Build #108 FAILED
2023-06-01T14:30:25Z Build #109 FAILED
2023-06-01T15:00:40Z Build #110 ABORTED
2023-06-01T15:30:15Z Build #111 SUCCESS
EOF

RUN chmod 0600 /home/user/ci_cd/logs/build.log

# Environment variables
ENV LANG=C
ENV LC_ALL=C