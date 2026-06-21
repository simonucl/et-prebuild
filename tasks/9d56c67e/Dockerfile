FROM ubuntu:22.04

# Author "Apptainer Task Builder"
# Description "Environment for vulnscan patching exercise with pytest pre-installed."

RUN set -e && \
    echo "Updating package index and installing prerequisites..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        patch \
        diffutils \
        ca-certificates

RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest

RUN mkdir -p /home/user/vulnscan/patches

RUN cat <<'EOF' >/home/user/vulnscan/services.conf
# Service configuration
ssh: enabled
telnet: enabled
ftp: enabled
http: enabled
https: disabled
snmp: enabled
# End of file
EOF

RUN cat <<'EOF' >/home/user/vulnscan/services.conf.fixed
# Service configuration
ssh: enabled
telnet: disabled
ftp: disabled
http: enabled
https: enabled
snmp: disabled
# End of file
EOF

RUN chmod -R a+rwX /home/user/vulnscan

RUN chmod 755 /home/user

ENV PYTHONUNBUFFERED=1
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH