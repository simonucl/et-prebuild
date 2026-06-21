FROM ubuntu:22.04

# Install Python and pytest
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare required directory structure
RUN mkdir -p /home/user/repos/binrepo && \
    mkdir -p /home/user/reports

# Set permissions:
#   • binrepo must be readable (agent only reads)
#   • reports must be writable (agent writes log file here)
RUN chmod 755 /home/user && \
    chmod 755 /home/user/repos && \
    chmod 755 /home/user/repos/binrepo && \
    chmod 777 /home/user/reports

# Create the three binary files with exact sizes and contents
RUN yes A | tr -d '\n' | head -c 100 > /home/user/repos/binrepo/alpha.bin && \
    yes B | tr -d '\n' | head -c 200 > /home/user/repos/binrepo/beta.bin && \
    yes C | tr -d '\n' | head -c 300 > /home/user/repos/binrepo/gamma.bin && \
    chmod 644 /home/user/repos/binrepo/*.bin

# Labels
LABEL Author="Artifact-Curation-Challenge"

# Help: Container prepared for the "binrepo_disk_usage" task.
# Directories and sample binary files are pre-populated, and pytest is
# available for the grader.