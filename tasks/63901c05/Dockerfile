FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip install --no-cache-dir pytest

# Prepare directory structure and seed files
RUN mkdir -p /home/user/projects/old

# Top-level Python utilities
RUN echo '# sample Python file' > /home/user/projects/alpha.py && \
    echo '# sample Python file' > /home/user/projects/beta.py && \
    echo '# sample Python file' > /home/user/projects/gamma_processor.py && \
    echo '# sample Python file' > /home/user/projects/zeta.py

# Non-Python files
RUN echo 'Sample README' > /home/user/projects/readme.md && \
    echo 'id,value' > /home/user/projects/data.csv

# Sub-directory with legacy utility
RUN echo '# legacy Python file' > /home/user/projects/old/legacy.py

# Set permissions
# Allow the unprivileged runtime user to create new files in /home/user/projects
RUN chmod 0777 /home/user/projects && \
    chmod 0777 /home/user/projects/old && \
    chmod 0666 /home/user/projects/*.py && \
    chmod 0666 /home/user/projects/readme.md && \
    chmod 0666 /home/user/projects/data.csv && \
    chmod 0666 /home/user/projects/old/legacy.py && \
    chmod 755 /home/user

# Labels
LABEL Author="task-prep-bot"
LABEL Description="Setup initial filesystem state for Python file listing task"