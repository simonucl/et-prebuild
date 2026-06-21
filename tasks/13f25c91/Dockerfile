FROM ubuntu:22.04

# Install Python tooling and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && \
    pip3 install --no-cache-dir pytest

# Create required directory structure and seed source files
RUN mkdir -p /home/user/net_logs

RUN cat >/home/user/net_logs/ip_list.txt <<'EOF'
192.168.0.1:80
192.168.0.2:443
10.0.0.1:22
EOF

RUN cat >/home/user/net_logs/ping_ms.txt <<'EOF'
32
85
12
EOF

# Ensure permissions
RUN chmod -R a+rwx /home/user && chmod 755 /home/user

ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"
ENV PYTHONIOENCODING="utf-8"

# Run script equivalent
CMD ["bash"]