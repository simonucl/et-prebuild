FROM ubuntu:22.04

# Labels
LABEL Author="Task Container Generator"
LABEL Description="Environment for optimisation-solver data-prep exercise with pytest pre-installed."

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Basic tools and Python environment
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        build-essential && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest

# Create initial data set for the exercise
RUN mkdir -p /home/user/raw_data

RUN cat > /home/user/raw_data/measurements.txt << 'EOF'
ID F1 F2 target
1 3.5 7.2 10.7
2 NaN 6.1 8.2
3 4.1 5.9 10.0
4 3.9 NaN 9.5
5 4.2 6.5 10.7
EOF

# Ensure students have write-access to their workspace
RUN chmod -R a+rwx /home/user

WORKDIR /home/user

CMD ["/bin/bash"]