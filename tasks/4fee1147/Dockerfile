# Converted from Apptainer definition file
FROM ubuntu:22.04

# Help section (none provided)

# Post section
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/app1/logs && \
    mkdir -p /home/user/app2/logs && \
    mkdir -p /home/user/app3/logs && \
    printf 'app1 access log stub\n'   > /home/user/app1/logs/access.log && \
    printf 'app1 error log stub\n'    > /home/user/app1/logs/error.log && \
    printf '2024-06-01 stub log\n'    > /home/user/app2/logs/2024-06-01.log && \
    printf '2024-06-02 stub log\n'    > /home/user/app2/logs/2024-06-02.log && \
    printf 'runtime stub log\n'       > /home/user/app3/logs/runtime.log && \
    chmod -R a+rwx /home/user

# Environment section
ENV PATH="$PATH:/usr/local/bin"

RUN chmod 755 /home/user