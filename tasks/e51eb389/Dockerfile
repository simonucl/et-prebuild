FROM ubuntu:22.04

# Labels
LABEL Author="CSV-disk-usage-exercise-setup"
LABEL Description="Initial state container for the CSV disk-usage snapshot exercise."

# Set environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean

# Prepare initial filesystem state for the CSV disk-usage exercise
# Create the required directory structure
RUN mkdir -p /home/user/data/csv

# Create the three CSV files with their exact apparent sizes
RUN dd if=/dev/zero of=/home/user/data/csv/marketing.csv bs=1 count=30720 && \
    dd if=/dev/zero of=/home/user/data/csv/sales_q1.csv bs=1 count=10240 && \
    dd if=/dev/zero of=/home/user/data/csv/sales_q2.csv bs=1 count=20480

# Set appropriate permissions
RUN chmod 644 /home/user/data/csv/*.csv && \
    chmod 755 /home/user /home/user/data /home/user/data/csv

# Ensure the reports directory does NOT exist
RUN rm -rf /home/user/reports || true

# Help information (as comments):
# This container image sets up the starting environment for the
# "CSV disk-usage snapshot" programming exercise:
#
#   • /home/user/data/csv/ contains exactly three CSV files with the required
#     byte sizes.
#   • /home/user/reports/ is absent.
#   • pytest is installed for the included test suite.