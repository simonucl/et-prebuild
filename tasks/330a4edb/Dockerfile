# Converted from Apptainer definition file
FROM ubuntu:22.04

# Install Python and pytest
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare project directory and seed files
RUN mkdir -p /home/user/data_project && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/data_project && \
    printf '1.3.5\n' > /home/user/data_project/version.txt

# Write CHANGELOG.md via heredoc
RUN cat > /home/user/data_project/CHANGELOG.md <<'EOF'
# Changelog

## [1.3.5] - 2023-06-30
- Added median calculation for quarterly_sales.csv
EOF

# Make files writable
RUN chmod 0666 /home/user/data_project/version.txt && \
    chmod 0666 /home/user/data_project/CHANGELOG.md

# Apply environment-time chmod
RUN chmod 755 /home/user

# Environment variables
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8