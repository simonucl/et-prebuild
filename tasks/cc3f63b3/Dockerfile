FROM ubuntu:22.04

# Labels
LABEL Author="Security-Scan-Setup"
LABEL Description="Environment prepared for security-oriented source code scan task."

# Post installation
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/security_scan/sample_code && \
    chmod 0777 /home/user/security_scan

# Create sample Python file app.py
RUN cat >/home/user/security_scan/sample_code/app.py <<'EOF'
# Sample app
user_input = input("Enter expression: ")
result = eval(user_input)  # insecure
print(result)
data = "print('hello')"
eval(data)
EOF

# Create sample Python file utils.py
RUN cat >/home/user/security_scan/sample_code/utils.py <<'EOF'
def calculate(expr):
    return eval(expr)  # insecure
EOF

# Ensure the source files are readable
RUN chmod -R 755 /home/user/security_scan/sample_code

# Set permissions and environment
RUN chmod 755 /home/user

ENV PATH="/usr/local/bin:/usr/bin:/bin"