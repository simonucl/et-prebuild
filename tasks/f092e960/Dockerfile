FROM ubuntu:22.04

# Labels
LABEL Author="task-setup"
LABEL Description="Container for timezone/locale audit task"

# Post installation
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        locales \
        tzdata \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    echo "Etc/UTC" > /etc/timezone && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Set working directory
WORKDIR /home/user

# Default command
CMD ["/bin/bash"]

# Help information (as comments):
# This container provides the baseline environment for the timezone/locale
# compliance audit task.  The student must create /home/user/audit/
# and the required log file as specified in the assignment.  Pytest is
# pre-installed so that the automated grading suite can run.