FROM ubuntu:22.04

# Help / description
# Author: Course Autograder
# Description: Initial environment for vulnerability-scan parsing task, includes pytest and predefined inventory file.

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip --no-install-recommends && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/scan_data && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/scan_data

RUN cat > /home/user/scan_data/vulnerable-services.ini <<'EOF'
[192.168.1.10-ssh]
port = 22
service = ssh
version = 7.8p1

[192.168.1.11-ssh]
port = 22
service = ssh
version = 8.4p1

[192.168.1.20-apache]
port = 80
service = apache
version = 2.4.48

[192.168.1.21-apache]
port = 80
service = apache
version = 2.4.53

[192.168.1.30-mysql]
port = 3306
service = mysql
version = 5.7.37

[192.168.1.31-mysql]
port = 3306
service = mysql
version = 8.0.32
EOF

RUN chmod 0666 /home/user/scan_data/vulnerable-services.ini

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN chmod 755 /home/user

LABEL Author="Course Autograder"
LABEL Description="Initial environment for vulnerability-scan parsing task, includes pytest and predefined inventory file."