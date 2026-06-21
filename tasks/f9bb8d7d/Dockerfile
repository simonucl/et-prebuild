FROM ubuntu:22.04

# Update package lists and install Python 3 + pip
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create runscript equivalent
RUN cat <<EOF > /usr/local/bin/runscript.sh
#!/bin/sh
chmod 755 /home/user
exec "\$@"
EOF

RUN chmod +x /usr/local/bin/runscript.sh

ENTRYPOINT ["/usr/local/bin/runscript.sh"]