FROM ubuntu:22.04

# Install Python tooling required by the exercise grader
RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare the initial filesystem state for the learner
# Create the directory hierarchy
RUN mkdir -p /home/user/vuln_scans && \
    chmod 0777 /home/user/vuln_scans

# Create the canonical scan file with exact expected content
RUN cat > /home/user/vuln_scans/initial_scan.txt <<'EOF'
Host: 10.0.0.5 (target-machine)  Status: Up
PORT     STATE SERVICE
21/tcp   open  ftp
22/tcp   open  ssh
80/tcp   open  http
111/tcp  closed rpcbind
5432/tcp open  postgresql
EOF

# Make the file writable by the learner while keeping exact content
RUN chmod 0666 /home/user/vuln_scans/initial_scan.txt && \
    chmod 755 /home/user

# Labels
LABEL Author="Pen-Test Training Environment"
LABEL Description="Initializes /home/user/vuln_scans/initial_scan.txt and installs pytest."

# Environment variables
ENV LC_ALL=C