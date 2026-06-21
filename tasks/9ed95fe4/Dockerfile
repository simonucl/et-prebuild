FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest

# Create directory structure
RUN mkdir -p /home/user/project/api_responses

# Create JSON stub files
RUN cat > /home/user/project/api_responses/response_200.json <<'EOF'
{"status":200,"message":"OK"}
EOF

RUN cat > /home/user/project/api_responses/response_400.json <<'EOF'
{"status":400,"message":"Bad Request"}
EOF

RUN cat > /home/user/project/api_responses/response_500.json <<'EOF'
{"status":500,"message":"Server Error"}
EOF

# Permissions
RUN chmod -R 777 /home/user/project && \
    chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8