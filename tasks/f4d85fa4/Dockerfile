FROM ubuntu:22.04

# Help/label metadata
LABEL Author="You"
LABEL Description="Container for backup-creation task – includes pytest and initial raw files."

ENV DEBIAN_FRONTEND=noninteractive

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/vuln_scans/raw

RUN cat > /home/user/vuln_scans/raw/initial_network.nmap <<'EOF'
# Nmap 7.93 scan initiated Fri Sep 15 13:45:00 2023 as: nmap -A -T4 192.168.1.0/24
Host: 192.168.1.10 ()  Status: Up
PORT     STATE SERVICE     VERSION
22/tcp   open  ssh         OpenSSH 7.9p1 Ubuntu 10 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http        Apache httpd 2.4.29 ((Ubuntu))

# Nmap done at Fri Sep 15 13:45:30 2023 -- 256 IP addresses (1 host up) scanned in 30.00 seconds
EOF

RUN echo >> /home/user/vuln_scans/raw/initial_network.nmap

RUN cat > /home/user/vuln_scans/raw/ssh_bruteforce.hydra <<'EOF'
Hydra v9.1 (c) 2023 - Please do not use in unauthorised ways.
Target: 192.168.1.10 - ssh
[22][ssh] host: 192.168.1.10   login: root   password: toor
1 of 1 target successfully completed, 1 valid password found
EOF

RUN echo >> /home/user/vuln_scans/raw/ssh_bruteforce.hydra

RUN cat > /home/user/vuln_scans/raw/webdir_enum.gobuster <<'EOF'
===============================================================
Gobuster v3.3.0
===============================================================
/admin (Status: 301)
/login (Status: 200)
/config.php (Status: 403)
===============================================================
EOF

RUN echo >> /home/user/vuln_scans/raw/webdir_enum.gobuster

RUN chmod -R u+rwX,go+rX /home/user

RUN chmod 755 /home/user