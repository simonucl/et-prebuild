FROM ubuntu:22.04

# Labels
LABEL Author="OpenAI ChatGPT"
LABEL Description="Ubuntu 22.04 base with pytest and initial CSV data for the sales filtering task."

# Update package index and install Python + pip
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        gnupg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the verification suite
RUN pip3 install --no-cache-dir pytest

# Prepare initial filesystem state required by the assignment
RUN mkdir -p /home/user/data

# Create the CSV data file
RUN cat >/home/user/data/sales_2023_Q1.csv <<'CSVEOF'
OrderID,Date,Country,Product,Quantity,UnitPrice
1001,2023-01-05,USA,Laptop,2,750
1002,2023-01-06,Canada,Mouse,5,20
1003,2023-01-10,USA,Keyboard,3,30
1004,2023-02-01,USA,Monitor,1,200
1005,2023-02-05,Germany,Mouse,10,18
1006,2023-03-12,USA,Headphones,4,50
1007,2023-03-15,France,Laptop,1,800
CSVEOF

# Ensure non-root users can access the prepared data
RUN chmod -R a+rwX /home/user

# Environment variables
ENV PATH="$PATH:/home/user/.local/bin"

# Set working directory
WORKDIR /home/user

# Default command
CMD ["echo", "Sales data container ready. Execute your solution commands manually."]