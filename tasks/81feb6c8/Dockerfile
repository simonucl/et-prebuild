FROM ubuntu:22.04

# Basic tooling
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git-core \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Set up initial project tree expected by the assignment tests
RUN mkdir -p /home/user/projects/ci_logs

# ---------- 2023-11-01 ----------
RUN cat > /home/user/projects/ci_logs/logs_2023-11-01.txt <<'EOF'
[2023-11-01 09:15:23] BUILD_ID=build-001 STATUS=SUCCESS DURATION=113s
[2023-11-01 09:24:01] BUILD_ID=build-002 STATUS=FAILURE DURATION=87s
[2023-11-01 10:05:44] BUILD_ID=build-003 STATUS=SUCCESS DURATION=101s
[2023-11-01 10:55:30] BUILD_ID=build-004 STATUS=SUCCESS DURATION=95s
[2023-11-01 11:12:09] BUILD_ID=build-005 STATUS=FAILURE DURATION=110s
[2023-11-01 11:48:19] BUILD_ID=build-006 STATUS=SUCCESS DURATION=88s
[2023-11-01 12:30:41] BUILD_ID=build-007 STATUS=SUCCESS DURATION=97s
[2023-11-01 13:02:56] BUILD_ID=build-008 STATUS=SUCCESS DURATION=99s
[2023-11-01 14:25:17] BUILD_ID=build-009 STATUS=SUCCESS DURATION=102s
[2023-11-01 15:43:55] BUILD_ID=build-010 STATUS=SUCCESS DURATION=90s
EOF

# ---------- 2023-11-02 ----------
RUN cat > /home/user/projects/ci_logs/logs_2023-11-02.txt <<'EOF'
[2023-11-02 09:05:13] BUILD_ID=build-011 STATUS=SUCCESS DURATION=115s
[2023-11-02 09:47:28] BUILD_ID=build-012 STATUS=SUCCESS DURATION=108s
[2023-11-02 10:11:06] BUILD_ID=build-013 STATUS=FAILURE DURATION=86s
[2023-11-02 10:59:40] BUILD_ID=build-014 STATUS=FAILURE DURATION=92s
[2023-11-02 11:23:18] BUILD_ID=build-015 STATUS=SUCCESS DURATION=99s
[2023-11-02 11:58:07] BUILD_ID=build-016 STATUS=SUCCESS DURATION=94s
[2023-11-02 12:34:29] BUILD_ID=build-017 STATUS=SUCCESS DURATION=97s
[2023-11-02 13:06:52] BUILD_ID=build-018 STATUS=SUCCESS DURATION=112s
[2023-11-02 13:55:14] BUILD_ID=build-019 STATUS=FAILURE DURATION=88s
[2023-11-02 14:37:33] BUILD_ID=build-020 STATUS=SUCCESS DURATION=91s
EOF

# Initialise a dummy git repository structure (tests just check for the dir)
RUN mkdir -p /home/user/projects/.git

# Create the initial .gitignore file with the exact required two lines
RUN cat > /home/user/projects/.gitignore <<'EOF'
# Existing ignore patterns
*.tmp
EOF

# Permissions: the unprivileged user running inside the container
#              must be able to create new files under /home/user/projects
RUN chmod -R a+rX /home/user && \
    chmod -R a+w /home/user/projects && \
    chmod 755 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=utf-8