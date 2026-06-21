FROM ubuntu:22.04

# Author: connectivity-report-template
# Description: Environment for connectivity summary exercise with pytest pre-installed.

ENV LC_ALL=C
ENV LANG=C
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN set -e \
    && apt-get update -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip python3-setuptools python3-wheel \
        ca-certificates \
        grep gawk coreutils

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && chmod 755 /home/user

RUN cat > /home/user/network_raw.log <<'EOF'
[2024-05-10 10:00:01] --- 8.8.8.8 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3004ms
rtt min/avg/max/mdev = 13.942/14.235/14.588/0.249 ms

[2024-05-10 10:00:05] --- 1.1.1.1 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3005ms
rtt min/avg/max/mdev = 30.120/30.312/30.701/0.215 ms

[2024-05-10 10:00:09] --- example.com (93.184.216.34) ping statistics ---
4 packets transmitted, 0 received, 100% packet loss, time 4087ms
EOF

RUN chmod 644 /home/user/network_raw.log

RUN rm -rf /home/user/network_diagnostics \
    && mkdir -p /home/user/network_diagnostics \
    && chmod 755 /home/user/network_diagnostics

CMD echo "Container for connectivity-report exercise." && echo "Enter the shell with:  docker run -it <image> /bin/bash"