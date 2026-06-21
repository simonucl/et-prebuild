FROM ubuntu:22.04

# Labels
LABEL Author="Container build for sales-CSV filtering task"
LABEL Description="Provides initial CSV data and pytest for automated grading."

# Help information (as comments):
# This container image includes:
# • The three quarterly sales CSV files in /home/user/data/
# • pytest installed for the grading harness
#
# Students/agents are expected to create /home/user/output/filtered_sales.csv
# and /home/user/output/process.log according to the assignment instructions.

# Update APT index and install Python + pip, then install pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest

# Create the required data directory
RUN mkdir -p /home/user/data

# Create Q1_sales.csv
RUN cat > /home/user/data/Q1_sales.csv <<'EOF'
OrderID,Product,Amount,Status
1001,Laptop,1200,Completed
1002,Mouse,25,Completed
1003,Desk,300,Pending
1004,Monitor,200,Cancelled
1005,Phone,800,Completed
1006,Server,2500,Completed
EOF

# Create Q2_sales.csv
RUN cat > /home/user/data/Q2_sales.csv <<'EOF'
OrderID,Product,Amount,Status
2001,Tablet,300,Completed
2002,Chair,150,Pending
2003,Headset,70,Completed
2004,Printer,600,Completed
2005,Camera,1100,Completed
EOF

# Create Q3_sales.csv
RUN cat > /home/user/data/Q3_sales.csv <<'EOF'
OrderID,Product,Amount,Status
3001,Router,90,Completed
3002,Switch,1200,Completed
3003,Desk,320,Cancelled
3004,Laptop,1400,Completed
3005,Microphone,80,Pending
EOF

# Ensure the /home/user tree is writable by the non-root user
# Clean up APT caches to keep the image small
RUN chmod -R a+rwx /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"