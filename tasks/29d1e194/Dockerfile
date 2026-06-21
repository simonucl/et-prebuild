FROM ubuntu:22.04

# From %help or %labels (converted to comments)
# chmod 755 /home/user
# Author mobile-ci-prep
# Description "Environment for symlink normalisation task (Android SDK & Gradle). Pytest pre-checks included."

ENV HOME=/home/user

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/build-tools/android-sdk-r30 && \
    touch /home/user/build-tools/android-sdk-r30/placeholder.txt

RUN mkdir -p /home/user/projects/sample-app && \
    touch /home/user/projects/sample-app/gradlew && \
    chmod +x /home/user/projects/sample-app/gradlew

RUN chmod -R 0777 /home/user

RUN apt-get clean && rm -rf /var/lib/apt/lists/*