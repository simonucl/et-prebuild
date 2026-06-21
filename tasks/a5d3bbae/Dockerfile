FROM ubuntu:22.04

# Help / labels from %labels
LABEL Author="Apptainer Task Setup"
LABEL Description="Environment for manifest creation task with pytest pre-installed."

# Ensure /home/user exists
RUN mkdir -p /home/user

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/my_project/docs && \
    mkdir -p /home/user/my_project/src && \
    mkdir -p /home/user/my_project/tests && \
    echo "Project README" > /home/user/my_project/README.md && \
    echo "Usage documentation" > /home/user/my_project/docs/usage.txt && \
    echo 'print("app running")' > /home/user/my_project/src/app.py && \
    echo '# Helper functions' > /home/user/my_project/src/helpers.py && \
    echo '# Tests for app.py' > /home/user/my_project/tests/test_app.py && \
    echo '# Tests for helpers.py' > /home/user/my_project/tests/test_helpers.py && \
    find /home/user/my_project -type d -exec chmod 755 {} \; && \
    find /home/user/my_project -type f -exec chmod 644 {} \; && \
    chmod 755 /home/user

ENV PROJECT_ROOT=/home/user/my_project