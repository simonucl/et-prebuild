FROM ubuntu:22.04

# Help / metadata comments
# Author: Container Build Automation
# Description: Environment for CPU-scheduling priority task with pytest pre-installed

RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user

RUN cat > /home/user/db_long_query.sh << 'EOF'
#!/usr/bin/env bash
# Simulates a CPU-intensive long query.
while true; do :; done
EOF

RUN chmod 0755 /home/user/db_long_query.sh

RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

CMD echo "This container is intended for the CPU-scheduling priority exercise." && \
    echo "Invoke an interactive shell or run your solution script as needed."