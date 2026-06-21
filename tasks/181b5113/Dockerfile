FROM ubuntu:22.04

# Help text
# Author Microservices Diagnostics Setup
# Description Initial filesystem state for diagnostics exercise (includes pytest)
# This container image provides the starting point for the microservices
# diagnostics exercise. It pre-seeds the required log files and installs
# pytest for the automated grader.

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && \
    chmod 1777 /home/user

RUN for svc in service-a service-b service-c; do \
        mkdir -p "/home/user/microservices/${svc}/logs"; \
    done

RUN cat > /home/user/microservices/service-a/logs/app.log << 'EOF'
2024-06-20T09:00:01Z INFO [c142] latency=120 status=200
2024-06-20T09:00:02Z INFO [c143] latency=110 status=200
2024-06-20T09:00:03Z INFO [c144] latency=130 status=200
2024-06-20T09:00:04Z INFO [c145] latency=125 status=200
2024-06-20T09:00:05Z INFO [c146] latency=140 status=200
2024-06-20T09:00:06Z INFO [c147] latency=115 status=200
2024-06-20T09:00:07Z INFO [c148] latency=118 status=200
2024-06-20T09:00:08Z INFO [c149] latency=121 status=200
2024-06-20T09:00:09Z ERROR [c150] latency=119 status=500
2024-06-20T09:00:10Z INFO [c151] latency=117 status=200
EOF

RUN cat > /home/user/microservices/service-b/logs/app.log << 'EOF'
2024-06-20T09:00:11Z INFO [d242] latency=100 status=200
2024-06-20T09:00:12Z INFO [d243] latency=102 status=200
2024-06-20T09:00:13Z INFO [d244] latency=98 status=200
2024-06-20T09:00:14Z INFO [d245] latency=97 status=200
2024-06-20T09:00:15Z INFO [d246] latency=101 status=200
2024-06-20T09:00:16Z INFO [d247] latency=99 status=200
EOF

RUN cat > /home/user/microservices/service-c/logs/app.log << 'EOF'
2024-06-20T09:00:17Z INFO [e342] latency=210 status=200
2024-06-20T09:00:18Z INFO [e343] latency=230 status=200
2024-06-20T09:00:19Z ERROR [e344] latency=220 status=503
2024-06-20T09:00:20Z INFO [e345] latency=215 status=200
EOF

RUN chmod -R 0755 /home/user/microservices

ENV PATH="$PATH:/home/user/.local/bin"