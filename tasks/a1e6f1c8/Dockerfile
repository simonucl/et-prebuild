FROM ubuntu:22.04

# Help text
# This container provides the prerequisites for the Maven upload-status summary exercise.
# It includes:
# - Pre-created build log at /home/user/builds/logs/build_2023-08-15.log
# - Writable reports directory at /home/user/builds/reports
# - Python 3 and pytest for automated evaluation

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/builds/logs && \
    mkdir -p /home/user/builds/reports

RUN cat > /home/user/builds/logs/build_2023-08-15.log <<'EOF'
[INFO] Uploaded: commons-io-2.11.0.jar
[INFO] Uploaded: guava-32.1.0.jar
[ERROR] FAILED to upload: junit-4.13.2.jar
[ERROR] FAILED to upload: log4j-1.2.17.jar
[INFO] Uploaded: slf4j-api-1.7.36.jar
EOF

RUN chmod 0777 /home/user/builds/reports && \
    chmod 0755 /home/user/builds/logs && \
    chmod 0644 /home/user/builds/logs/build_2023-08-15.log && \
    chmod 755 /home/user

ENV HOME=/home/user