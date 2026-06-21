# Converted from Apptainer definition file
FROM ubuntu:22.04

# Help / labels
# Author: Auto-generated
# Description: Container for INI summarisation task with pytest pre-installed.
LABEL Author="Auto-generated"
LABEL Description="Container for INI summarisation task with pytest pre-installed."

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir --upgrade pip pytest

RUN mkdir -p /home/user/docs/configs && \
    mkdir -p /home/user/docs/reports

RUN cat <<'EOF' > /home/user/docs/configs/settings.ini
[general]
author=alice
version=1.2.3

[paths]
home=/home/alice
temp=/tmp/project
EOF

RUN cat <<'EOF' > /home/user/docs/configs/database.ini
[connection]
host=localhost
port=5432
user=dbuser

[pools]
min=1
max=15
EOF

RUN cat <<'EOF' > /home/user/docs/configs/ui.ini
[window]
width=1024
height=768

[theme]
color=dark
font=Roboto
EOF

RUN chmod -R a+r /home/user/docs/configs && \
    chmod -R a+rwX /home/user/docs/reports && \
    chmod a+rwX /home/user/docs && \
    chmod 755 /home/user