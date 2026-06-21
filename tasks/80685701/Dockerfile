# Converted from Apptainer definition file
FROM ubuntu:22.04

# Help / labels
LABEL Author="Apptainer Task Generator"
LABEL Description="Container image providing initial state for project data consolidation task."

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Fix home permissions
RUN chmod 755 /home && mkdir -p /home/user

# Update and install Python, pip, pytest
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# Create project_data directory
RUN mkdir -p /home/user/project_data

# employees.csv
RUN cat > /home/user/project_data/employees.csv <<'EOF'
id,name,dept,salary
101,Alice Smith,Engineering,90000
102,Bob Johnson,Marketing,65000
103,Carol Martinez,Engineering,72000
104,David Lee,Engineering,68000
105,Eve Turner,HR,70000
106,Frank Wright,Engineering,80000
EOF

# statuses.json
RUN cat > /home/user/project_data/statuses.json <<'EOF'
[
  {"id": 101, "active": true},
  {"id": 102, "active": false},
  {"id": 103, "active": true},
  {"id": 104, "active": false},
  {"id": 105, "active": true},
  {"id": 106, "active": true}
]
EOF

# Permissions
RUN chmod -R 0777 /home/user/project_data