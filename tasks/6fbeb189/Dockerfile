# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ---- %post section ----
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip locales && \
    python3 -m pip install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/reports

RUN cat > /home/user/reports/test_report.txt <<'EOF'
TC-0001 : PASS : 1120
TC-0002 : FAIL : 2075
TC-0003 : PASS : 998
TC-0004 : PASS : 1311
TC-0005 : FAIL : 1567
TC-0006 : PASS : 1044
TC-0007 : FAIL : 1452
TC-0008 : PASS : 1005
TC-0009 : PASS : 1113
TC-0010 : PASS : 1250
EOF

RUN chmod -R a+rX,u+w,go+w /home/user

# ---- %environment section ----
RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8