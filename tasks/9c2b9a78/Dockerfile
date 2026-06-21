# Author: example
# Description: Container for server inventory counting task – provides initial servers.log and pytest.

FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 755 /home/user

RUN cat > /home/user/servers.log <<'EOF'
srv01,OK,87,0.23
srv02,DOWN,0,0.00
srv03,OK,102,0.65
srv04,WARNING,12,1.10
srv05,DOWN,0,0.00
srv06,OK,34,0.40
srv07,DOWN,0,0.00
EOF

RUN chmod 644 /home/user/servers.log

ENV PYTHONIOENCODING=UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

CMD echo "Container built for DOWN_COUNT task. Open a shell with 'docker run -it <image> /bin/bash' to start working."