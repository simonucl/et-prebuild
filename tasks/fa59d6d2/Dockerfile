FROM ubuntu:22.04

# Labels
LABEL Author="support_engineering_example"
LABEL Description="Base container for support-case exercise with initial configuration files and pytest installed."

# Post installation
RUN set -e && \
    echo "==> Updating apt and installing Python + pip" && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN echo "==> Installing pytest" && \
    pip3 install --no-cache-dir --upgrade pip setuptools && \
    pip3 install --no-cache-dir pytest

RUN echo "==> Creating support_case directory structure" && \
    mkdir -p /home/user/support_case && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/support_case

RUN echo "==> Populating initial app_config.yaml" && \
    cat > /home/user/support_case/app_config.yaml <<'EOF'
service:
  name: "FileProcessor"
  version: "1.2.3"
  enabled: false

logging:
  level: "info"
  path: "/var/log/fileprocessor/"
EOF

RUN echo "==> Populating initial system_info.toml" && \
    cat > /home/user/support_case/system_info.toml <<'EOF'
[cpu]
cores = 4
model = "Intel(R) Core(TM) i5-8250U"

[memory]
total_gb = 8

[os]
name = "Ubuntu"
version = "20.04"
EOF

RUN chmod 0666 /home/user/support_case/app_config.yaml && \
    chmod 0666 /home/user/support_case/system_info.toml

# Environment variables
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin"