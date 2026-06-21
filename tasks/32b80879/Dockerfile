FROM ubuntu:22.04

# Basic packages
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    if [ ! -e /usr/bin/python ]; then ln -s /usr/bin/python3 /usr/bin/python; fi

# Create dataset directory
RUN mkdir -p /home/user/datasets

# Create CSV file
RUN cat << 'EOF' > /home/user/datasets/temperature_readings.csv
Date,City,TempC
2023-01-01,Paris,5
2023-01-01,New York,-3
2023-01-02,Paris,6.5
2023-01-02,New York,-1
EOF

# Set permissions
RUN chmod 777 /home/user && \
    chmod 755 /home/user/datasets && \
    chmod 644 /home/user/datasets/temperature_readings.csv

# Environment variables
ENV LC_ALL=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1

# Help text
# Container for the temperature-conversion assignment. Use this as a build image; no default action.