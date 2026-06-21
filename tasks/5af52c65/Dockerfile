# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from %labels section
LABEL Author="your_name"
LABEL Description="Container for heavy specimen extraction task"

# Post-installation steps from %post section
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        gawk \
        sed \
        --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the test harness
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Create the data directory
RUN mkdir -p /home/user/data

# Create the specimen TSV file using a heredoc
RUN cat > /home/user/data/specimens.tsv <<'EOF'
id	species	location	weight_g	notes
SPC001	Mus musculus	LabA	23	pregnant
SPC002	Rattus norvegicus	LabB	512	adult
SPC003	Mus musculus	Field	712	juvenile
SPC004	Rattus norvegicus	LabC	98	adult
SPC005	Mus musculus	Field	501	adult
EOF

# Set appropriate permissions
RUN chmod 644 /home/user/data/specimens.tsv && \
    chmod 755 /home/user /home/user/data

# Environment variables from %environment section
ENV PATH=/usr/bin:$PATH

# Help text from %help / %runscript section
# This container is set up for the heavy specimen extraction task.
# Use awk/sed as described in the assignment.

# Default command corresponding to %runscript
CMD ["/bin/sh", "-c", "echo \"This container is set up for the heavy specimen extraction task.\" && echo \"Use awk/sed as described in the assignment.\""]