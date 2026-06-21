FROM ubuntu:22.04

# Help section
# Container for performance logging exercise with Python and pytest installed.

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        ca-certificates && \
    ln -sf /usr/bin/python3 /usr/local/bin/python && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/perf_logs

RUN cat <<'EOF' >/home/user/perf_logs/cpu_profile.log
time,usage
0,12
1,18
2,17
EOF

RUN cat <<'EOF' >/home/user/perf_logs/memory_profile.log
time,usage
0,153600
1,158720
2,162304
EOF

RUN cat <<'EOF' >/home/user/perf_logs/io_profile.log
time,bytes
0,4096
1,8192
2,6144
EOF

RUN chmod 0777 /home/user && \
    chmod 0755 /home/user/perf_logs && \
    chmod 0644 /home/user/perf_logs/*.log && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

CMD ["bash"]