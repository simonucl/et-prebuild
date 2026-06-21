FROM ubuntu:22.04

# Set environment variables
ENV LC_ALL=C.UTF-8
ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# Update package index and install Python & pip
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grader
RUN pip3 install --no-cache-dir pytest

# Create initial filesystem state required by the FinOps assignment
RUN mkdir -p /home/user/data

# Create the cloudbilling.html file
RUN cat > /home/user/data/cloudbilling.html <<'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Cloud Billing Portal</title>
</head>
<body>
    <h1>Monthly Cost Breakdown</h1>
    <table id="cost-table">
        <thead>
            <tr><th>Service</th><th>Monthly Cost (USD)</th></tr>
        </thead>
        <tbody>
            <tr><td>EC2</td><td>$45.32</td></tr>
            <tr><td>S3</td><td>$12.05</td></tr>
            <tr><td>RDS</td><td>$33.10</td></tr>
        </tbody>
    </table>
</body>
</html>
EOF

# Set reasonable permissions so an unprivileged user can read/write
RUN chmod 755 /home/user && \
    chmod 755 /home/user/data && \
    chmod 644 /home/user/data/cloudbilling.html