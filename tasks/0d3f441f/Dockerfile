FROM ubuntu:22.04

# Install Python and pytest
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip && pip3 install --no-cache-dir pytest

# Prepare initial directory structure
RUN mkdir -p /home/user/projects/raw_data

# Create CSV files
RUN cat > /home/user/projects/raw_data/sales_2023.csv <<'EOF'
id,amount
1,100
EOF

RUN cat > /home/user/projects/raw_data/inventory_2022.csv <<'EOF'
sku,qty
A1,50
EOF

RUN cat > /home/user/projects/raw_data/finance_2023.csv <<'EOF'
quarter,profit
Q1,2000
EOF

# Empty file
RUN touch /home/user/projects/raw_data/broken.csv

# Fix permissions
RUN chmod -R a+rwX /home/user

# Environment settings
RUN chmod 755 /home/user
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Labels
LABEL Author="Apptainer exercise setup – data-pipeline prototype"
LABEL Description="Container that provides the clean starting state for the shell-based CSV moving exercise."