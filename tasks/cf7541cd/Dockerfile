FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Build Script"
LABEL Description="Container for classic Unix text-processing task (API log aggregation)."

# Post installation
RUN set -e && \
    echo "Updating package index and installing Python tooling..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        ca-certificates \
        tzdata \
        locales && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    echo "Installing pytest via pip..." && \
    pip3 install --no-cache-dir pytest && \
    echo "Creating non-root user 'user'..." && \
    groupadd --gid 1000 user && \
    useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash user

# Setting up initial directory structure and fixture files
RUN set -e && \
    RAW_DIR=/home/user/api_logs/raw && \
    SUMMARY_DIR=/home/user/api_logs/summary && \
    mkdir -p "${RAW_DIR}" && \
    mkdir -p "${SUMMARY_DIR}" && \
    touch "${SUMMARY_DIR}/.gitkeep"

# Create first log file
RUN cat > /home/user/api_logs/raw/service_2023-05-12.log <<'EOF'
2023-05-12T14:23:11Z - {"service":"user","endpoint":"/v1/register","status":200,"response_time_ms":132}
2023-05-12T14:25:46Z - {"service":"auth","endpoint":"/v1/login","status":500,"error":"DB_TIMEOUT","response_time_ms":987}
2023-05-12T14:28:09Z - {"service":"user","endpoint":"/v1/profile","status":200,"response_time_ms":84}
2023-05-12T14:31:55Z - {"service":"payment","endpoint":"/v1/pay","status":500,"error":"CARD_DECLINED","response_time_ms":453}
EOF

# Create second log file
RUN cat > /home/user/api_logs/raw/service_2023-05-13.log <<'EOF'
2023-05-13T07:12:44Z - {"service":"payment","endpoint":"/v1/refund","status":200,"response_time_ms":211}
2023-05-13T07:15:02Z - {"service":"auth","endpoint":"/v1/login","status":200,"response_time_ms":153}
2023-05-13T07:18:27Z - {"service":"user","endpoint":"/v1/delete","status":500,"error":"UNKNOWN_USER","response_time_ms":674}
2023-05-13T07:20:19Z - {"service":"payment","endpoint":"/v1/pay","status":500,"error":"INSUFFICIENT_FUNDS","response_time_ms":502}
EOF

# Ensure proper ownership for the non-root user
RUN chown -R user:user /home/user && \
    chmod 755 /home/user

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Set working directory
WORKDIR /home/user

# Default command
CMD ["bash", "-c", "echo 'This Docker image is intended for an educational exercise.' && echo 'Switch to the user account before running the tests or doing work:' && echo '   su - user' && echo 'Happy coding!' && exec bash"]