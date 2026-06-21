FROM ubuntu:22.04

# Labels
LABEL Author="task-setup"
LABEL Description="Docker image for incident report exercise – template and pytest pre-installed"

############################
# 1. System dependencies   #
############################
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

############################
# 2. Python tooling        #
############################
RUN pip3 install --no-cache-dir pytest

############################
# 3. Workspace setup       #
############################
# Create the user home and incidents directory
RUN mkdir -p /home/user/incidents

# Make sure the student (non-root runtime user) can write here
RUN chmod 777 /home/user && \
    chmod 777 /home/user/incidents

# Provide a non-empty incident template the student will fill in
RUN cat > /home/user/incidents/INCIDENT_TEMPLATE.md <<'EOF'
Incident ID: <REPLACE_ME>
Date: <YYYY-MM-DD>

Summary
-------
<Brief summary of the incident>

Root Cause
----------
<Root cause description>

Impact
------
<Impact description>

Mitigation
----------
<Mitigation steps>

Postmortem Actions
------------------
1. <Action item 1>
2. <Action item 2>
3. <Action item 3>
EOF

# Ensure the template is writable by the student
RUN chmod 666 /home/user/incidents/INCIDENT_TEMPLATE.md

# Environment variables
ENV PATH="/usr/local/bin:$PATH"

WORKDIR /home/user

CMD echo "Container is set up for the incident report exercise." && \
    echo "You can start by navigating to /home/user/incidents." && \
    /bin/bash