FROM ubuntu:22.04

# Set environment variables
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# ------------------------------------------------------------------ #
# Basic OS packages + Python tooling
# ------------------------------------------------------------------ #
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        locales \
        ca-certificates \
        tzdata && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Locales (needed by many Python libs)
RUN locale-gen en_US.UTF-8

# ------------------------------------------------------------------ #
# Python testing utilities
# ------------------------------------------------------------------ #
RUN pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------ #
# Create initial sample database directory with exact contents
# ------------------------------------------------------------------ #
RUN mkdir -p /home/user/sample_db_data

# customers.csv – 50 lines (1 header + 49 data lines)
RUN { \
        echo "id,name"; \
        for i in $(seq 1 49); do \
            echo "${i},Customer_${i}"; \
        done; \
    } > /home/user/sample_db_data/customers.csv

# orders.csv – 100 lines (1 header + 99 data lines)
RUN { \
        echo "id,customer_id,total"; \
        for i in $(seq 1 99); do \
            cust=$(( (i % 49) + 1 )); \
            echo "${i},${cust},$((i * 10))"; \
        done; \
    } > /home/user/sample_db_data/orders.csv

# products.csv – 30 lines (1 header + 29 data lines)
RUN { \
        echo "id,name,price"; \
        for i in $(seq 1 29); do \
            echo "${i},Product_${i},$((i * 5))"; \
        done; \
    } > /home/user/sample_db_data/products.csv

# Consistent permissions (read-only to guarantee no accidental mutation)
RUN chmod -R 0755 /home/user/sample_db_data && \
    chmod 755 /home/user

# ------------------------------------------------------------------ #
# Ensure that the benchmark output directory does NOT exist
# ------------------------------------------------------------------ #
RUN rm -rf /home/user/backup_benchmark || true

# Set working directory
WORKDIR /home/user

# Help information as comments:
# This container provides the exact initial filesystem state required for
# the "Database Backup Benchmark" assignment.
#
# Contents prepared:
#   • /home/user/sample_db_data
#         ↳ customers.csv (50 lines, header: id,name)
#         ↳ orders.csv    (100 lines, header: id,customer_id,total)
#         ↳ products.csv  (30 lines, header: id,name,price)
#
# Python and pytest are installed so that the autograder can validate the
# initial state.  No benchmark output directory is present; the student
# must create /home/user/backup_benchmark during the task execution.

CMD ["echo", "Container for the 'Database Backup Benchmark' exercise. Sample CSV data is available in /home/user/sample_db_data."]