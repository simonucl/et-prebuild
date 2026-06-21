FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/app/logs && \
    mkdir -p /home/user/output && \
    chmod 0755 /home && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/app && \
    chmod 0755 /home/user/app/logs && \
    chmod 0755 /home/user/output

RUN cat > /home/user/app/logs/perf.log <<'EOF'
2023-08-17 10:15:01 INFO Query A Execution time: 123 ms
2023-08-17 10:15:02 INFO Query B Execution time: 567 ms
2023-08-17 10:15:03 INFO Query C Execution time: 754 ms
2023-08-17 10:15:04 INFO Query D Execution time: 31 ms
2023-08-17 10:15:05 INFO Query E Execution time: 499 ms
2023-08-17 10:15:06 INFO Query F Execution time: 820 ms
EOF

RUN chmod 0644 /home/user/app/logs/perf.log && \
    chmod 0755 /home/user

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"