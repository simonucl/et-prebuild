FROM ubuntu:22.04

# Install runtime dependencies
RUN set -e && \
    echo "---- Installing runtime dependencies ----" && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        locales \
        tzdata && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set UTF-8 locale
RUN echo "---- Setting UTF-8 locale ----" && \
    locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8

# Install pytest
RUN echo "---- Installing pytest ----" && \
    pip3 install --no-cache-dir pytest

# Create initial directory structure
RUN echo "---- Creating initial directory structure and source CSV files ----" && \
    mkdir -p /home/user/data && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/data

# Create sales_q1_2022.csv
RUN cat >/home/user/data/sales_q1_2022.csv <<'EOF'
Region,Product,Units,Unit_Price,Transaction_Date
East,Widget,10,25.50,2022-01-15
West,Gadget,5,99.99,2022-02-10
South,Widget,3,25.50,2022-03-05
EOF

# Create sales_q2_2022.csv
RUN cat >/home/user/data/sales_q2_2022.csv <<'EOF'
Region,Product,Units,Unit_Price,Transaction_Date
East,Gizmo,7,49.00,2022-04-12
North,Widget,6,25.50,2022-05-20
West,Gadget,2,99.99,2022-06-30
EOF

# Create sales_q3_2022.csv
RUN cat >/home/user/data/sales_q3_2022.csv <<'EOF'
Region,Product,Units,Unit_Price,Transaction_Date
South,Gizmo,4,49.00,2022-07-14
East,Widget,8,25.50,2022-08-11
North,Gadget,3,99.99,2022-09-29
EOF

# Create sales_q4_2022.csv
RUN cat >/home/user/data/sales_q4_2022.csv <<'EOF'
Region,Product,Units,Unit_Price,Transaction_Date
West,Widget,9,25.50,2022-10-17
South,Gizmo,5,49.00,2022-11-21
East,Gadget,1,99.99,2022-12-03
EOF

# Ensure all CSV files are world-readable
RUN chmod 0644 /home/user/data/sales_q*_2022.csv

# Set environment variables
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

WORKDIR /home/user

CMD ["echo", "This container provides the initial environment for the sales data analysis task."]