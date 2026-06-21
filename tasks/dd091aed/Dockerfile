FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Task Preparer"
LABEL Description="Environment for CSV cleaning task with pytest installed"

RUN set -eux && \
    # Install Python and pytest
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    # Create the non-root user that the grading agent will run as
    groupadd -g 1000 user && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user && \
    # Prepare the initial dataset state
    mkdir -p /home/user/datasets/raw && \
    # Clean up apt cache to keep the image small
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create the CSV file with heredoc
RUN cat > /home/user/datasets/raw/weird_values.csv << 'EOF'
id,name,value
1,Alpha,10
2,Bravo,NULL
3,Charlie,30
2,Bravo,NULL
4,Delta,N/A
3,Charlie,30
5,Echo,50
EOF

# Ensure proper ownership for the grading user
RUN chown -R 1000:1000 /home/user && \
    chmod 755 /home/user

# Environment variables
ENV PYTHONUSERBASE=/home/user/.local
ENV PATH=$PYTHONUSERBASE/bin:$PATH

WORKDIR /home/user

CMD ["/bin/bash"]