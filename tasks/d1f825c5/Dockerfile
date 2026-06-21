FROM ubuntu:22.04

# Labels
LABEL Author="MyCompany"
LABEL Description="Environment for CSV cleaning & benchmarking exercise"

# Update package lists and install Python, pip, pytest, and GNU time
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        time && \
    pip3 install --no-cache-dir pytest

# Create the user home hierarchy
RUN mkdir -p /home/user/datasets/raw

# Write the exact raw CSV file (LF endings, newline after last line)
RUN cat <<'EOF' > /home/user/datasets/raw/sales.csv
id,region,sales
1,North,100
2,South,200
3,,150
4,East,
5,West,300
EOF

# Ensure permissive permissions so the non-root agent can create new files
RUN chmod -R 777 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8

# Default command
CMD ["echo", "Container for CSV cleaning exercise. Open a shell to begin."]