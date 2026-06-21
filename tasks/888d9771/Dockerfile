FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest

# Create initial project layout and starter files
RUN mkdir -p /home/user/projects/webapp/utils

RUN cat > /home/user/projects/webapp/app.py << 'PY'
# main application
import os
def run():
    os.system("ls -la")  # insecure
    print("Hello")
    eval("2+2")  # insecure
PY

RUN cat > /home/user/projects/webapp/utils/helpers.py << 'PY'
import subprocess
def dangerous(cmd):
    subprocess.call(cmd, shell=True)  # insecure
def safe():
    print("safe")
PY

RUN cat > /home/user/projects/webapp/README.md << 'MD'
This is just a sample README file for the webapp project.
MD

# Permissions
RUN chmod 0777 /home/user && \
    chmod -R a+rX /home/user/projects

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

LABEL Author="Apptainer Task Setup"
LABEL Description="Container with starter project for security scan task, plus pytest installed."