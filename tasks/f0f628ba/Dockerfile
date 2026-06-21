FROM ubuntu:22.04

# Post section
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/status_columns

RUN printf "deploy-httpd\ndeploy-nginx\ndeploy-redis\n" \
        > /home/user/status_columns/status_column_1.txt

RUN printf "running\nrunning\npending\n" \
        > /home/user/status_columns/status_column_2.txt

RUN printf "3/3\n2/2\n0/1\n" \
        > /home/user/status_columns/status_column_3.txt

RUN printf "10m\n5m\n12m\n" \
        > /home/user/status_columns/status_column_4.txt

RUN chmod 755 /home/user && \
    chmod 755 /home/user/status_columns && \
    chmod 644 /home/user/status_columns/status_column_*.txt

# Environment
ENV LC_ALL=C
ENV LANG=C

# Labels
LABEL Author="Kubernetes-Status-Setup"
LABEL Description="Base image for the Kubernetes status reports task – provides initial files and pytest"

# Run script equivalent
CMD echo "Container for Kubernetes status report assignment. Execute your shell and get to work!"