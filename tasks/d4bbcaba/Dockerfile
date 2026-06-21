FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Setup Bot"
LABEL Description="Environment for UNIX cut/paste exercise with preloaded CSV data and pytest installed."

# Update package lists and install Python + pip
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the test harness
RUN pip3 install --no-cache-dir pytest

# Create the /home/user hierarchy and the data directory
RUN mkdir -p /home/user/data

# Write the employee_master.csv file
RUN cat > /home/user/data/employee_master.csv <<'EOF'
EmployeeID,FullName,Department,Role,JoinDate
1001,Ann Dowling,Engineering,DevOps,2015-06-11
1002,Bob Tran,Sales,Account Manager,2018-03-17
1003,Carla Méndez,HR,Recruiter,2019-11-05
1004,Deepak Singh,Engineering,Backend Developer,2021-01-23
1005,Eva Rossi,Finance,Accountant,2017-07-30
EOF

# Write the payroll_Q1.csv file
RUN cat > /home/user/data/payroll_Q1.csv <<'EOF'
EmployeeID,Jan,Feb,Mar
1001,12750,12900,12800
1002,9450,9100,9300
1003,8750,8800,8900
1004,10600,10750,10850
1006,9900,10050,10100
EOF

# Ensure world-readable permissions (0644) on the source files
RUN chmod 644 /home/user/data/employee_master.csv /home/user/data/payroll_Q1.csv

# Set permissions on /home/user
RUN chmod 755 /home/user

# Environment variables
ENV PATH="$PATH:/root/.local/bin"

WORKDIR /home/user