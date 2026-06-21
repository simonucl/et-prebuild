FROM ubuntu:22.04

# install python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# prepare initial filesystem state
RUN mkdir -p /home/user/app_configs && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/app_configs

RUN cat > /home/user/app_configs/webapp.ini <<'EOF'
[general]
port=8080

[credentials]
username=web_admin
password=OldWebPass123!
EOF

RUN cat > /home/user/app_configs/dbservice.ini <<'EOF'
[service]
host=127.0.0.1

[credentials]
username=db_root
password=OldDbPass456!
EOF

RUN cat > /home/user/app_configs/mqbroker.ini <<'EOF'
[broker]
queues=8

[credentials]
username=mq_manager
password=OldMqPass789!
EOF

RUN cat > /home/user/app_configs/analytics.ini <<'EOF'
[analytics]
enabled=true

[credentials]
username=analyst
password=OldAnalystPass000!
EOF

RUN chmod 0666 /home/user/app_configs/*.ini

# environment variables
RUN chmod 755 /home/user
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

LABEL Author="AI Assistant"
LABEL Description="Container for credential-rotation exercise with initial INI files and pytest installed."