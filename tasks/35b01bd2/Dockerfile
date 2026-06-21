FROM ubuntu:22.04

# %help not provided; skipping

# Labels from %labels
LABEL Author="Apptainer Task Preparation"
LABEL Description="Container with initial state for the failed-artifact extraction task."

# Environment variables from %environment
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Post section
RUN set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/builds && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/builds

RUN cat > /home/user/builds/2024-05-01_daily_build_status.csv <<'EOF'
BuildID,Platform,Duration,Result,Artifact
B001,Android,15m,PASS,app-android-B001.apk
B002,iOS,17m,FAIL,app-ios-B002.ipa
B003,Android,18m,FAIL,app-android-B003.apk
B004,iOS,15m,PASS,app-ios-B004.ipa
EOF

RUN chmod 0666 /home/user/builds/2024-05-01_daily_build_status.csv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    chmod 755 /home/user