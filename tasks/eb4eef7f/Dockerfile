FROM ubuntu:22.04

# Labels
LABEL Author="TaskSetup"
LABEL Description="Initial state container for CSV cleaning AWK/Sed exercise"

# Install system dependencies and Python tooling
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest

# Create the initial directory structure expected by the task
RUN mkdir -p /home/user/data

# Create the raw CSV with exact required content and LF line endings
RUN cat > /home/user/data/raw_customer_churn.csv << 'EOF'
customer_id,name,age,churn,signup_date
1,Alice,30,0,2020-01-01
2,Bob,45,1,2019-11-21
3,Charlie,25,0,2021-06-12
4,Denise,33,1,2020-07-30
5,Evan,28,0,2022-02-14
EOF

# Ensure writable permissions for the non-root user who will run the task
RUN chmod -R 777 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Default command
CMD ["bash", "-c", "echo 'Container for the CSV cleaning task. Drop into a shell with: docker exec -it <container> bash'"]