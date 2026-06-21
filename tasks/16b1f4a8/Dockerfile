FROM ubuntu:22.04

# Update package index and install Python + pip
RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user

# Populate /home/user/config_changes.log
RUN cat > /home/user/config_changes.log <<'EOF'
2024-06-01 10:15:23 HOST=web01 USER=root ACTION=CREATE TYPE=FILE PATH=/etc/nginx/nginx.conf
2024-06-01 10:17:05 HOST=web01 USER=root ACTION=MODIFY TYPE=PERMISSION CMD=chmod 644 /etc/nginx/nginx.conf
2024-06-01 10:20:10 HOST=db01 USER=admin ACTION=MODIFY TYPE=CONTENT CMD=vim /etc/mysql/my.cnf
2024-06-01 10:21:22 HOST=web01 USER=root ACTION=MODIFY TYPE=PERMISSION CMD=chown root:root /etc/nginx/nginx.conf
2024-06-01 10:23:45 HOST=web01 USER=root ACTION=DELETE TYPE=FILE PATH=/tmp/test.tmp
2024-06-01 10:25:50 HOST=db01 USER=admin ACTION=MODIFY TYPE=PERMISSION CMD=chmod 600 /etc/mysql/my.cnf
EOF

RUN chmod 644 /home/user/config_changes.log && chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin