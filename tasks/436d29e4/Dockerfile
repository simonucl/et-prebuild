FROM ubuntu:22.04

# Author benchmark-setup

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

# Create required directory structure and benchmark scripts
RUN mkdir -p /home/user/perf_bench/apps

# Create app_sort.py
RUN cat > /home/user/perf_bench/apps/app_sort.py << 'EOF'
#!/usr/bin/env python3
print("benchmark_result_ms:42")
EOF

# Create app_math.py
RUN cat > /home/user/perf_bench/apps/app_math.py << 'EOF'
#!/usr/bin/env python3
print("benchmark_result_ms:84")
EOF

# Ensure executability and set safe permissions
RUN chmod 0755 /home/user/perf_bench/apps/app_sort.py /home/user/perf_bench/apps/app_math.py && \
    chmod -R a+rx /home/user

ENV PYTHONUNBUFFERED=1