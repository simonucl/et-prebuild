FROM ubuntu:22.04

# Author Automated Build
# Description Scaffold for linear-programming workflow testing.

ENV HOME=/home/user

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/solver_demo && \
    chmod 755 /home/user && \
    chmod 755 /home/user/solver_demo

RUN cat > /home/user/solver_demo/run_lp.py <<'EOF'
#!/usr/bin/env python3
print("objective=22.0")
print("x=4.0")
print("y=5.0")
EOF

RUN chmod 755 /home/user/solver_demo/run_lp.py

LABEL Author="Automated Build"
LABEL Description="Scaffold for linear-programming workflow testing."