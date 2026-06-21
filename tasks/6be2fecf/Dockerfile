FROM ubuntu:22.04

# Author diagnostic_bundle_task
# Description "Environment for the 'sample-app' support-bundle exercise."

# This container provides the initial filesystem state for the "sample-app" support-bundle exercise.
# Python and pytest are pre-installed for automated grading.

RUN set -e && \
    echo "Updating APT and installing Python tooling..." && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN echo "Preparing initial filesystem for the exercise..." && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    mkdir -p /home/user/sample-app/logs

# Create /home/user/sample-app/config.yaml
RUN cat > /home/user/sample-app/config.yaml <<'EOF'
app:
  name: Sample App
  version: "1.2.3"
server:
  port: 8080
logging:
  level: INFO
EOF

# Create /home/user/sample-app/env_vars
RUN cat > /home/user/sample-app/env_vars <<'EOF'
PATH=/usr/local/bin:/usr/bin:/bin
JAVA_HOME=/usr/lib/jvm/default-java
SAMPLE_APP_OPTS=-Xmx256m
EOF

# Create /home/user/sample-app/logs/app.log
RUN cat > /home/user/sample-app/logs/app.log <<'EOF'
2023-10-02 10:40:01 INFO Starting Sample App version 1.2.3
2023-10-02 10:40:05 INFO Listening on port 8080
2023-10-02 10:41:33 WARN Cache miss for key user:42
2023-10-02 10:42:07 ERROR Failed to connect to database
EOF

# Create /home/user/sample-app/status.txt
RUN cat > /home/user/sample-app/status.txt <<'EOF'
● sample-app.service - Sample App Service
   Loaded: loaded (/etc/systemd/system/sample-app.service; enabled; vendor preset: enabled)
   Active: active (running) since Mon 2023-10-02 10:40:00 UTC; 2h 05min ago
 Main PID: 1234 (java)
    Tasks: 14 (limit: 4915)
   Memory: 150.7M
   CGroup: /system.slice/sample-app.service
           ├─ 1234 /usr/bin/java -jar /opt/sample-app.jar
EOF

# Set permissions: allow read for everyone, write only for owner (root)
RUN find /home/user/sample-app -type f -exec chmod 0644 {} \; && \
    find /home/user/sample-app -type d -exec chmod 0755 {} \; && \
    chmod 755 /home/user

WORKDIR /home/user