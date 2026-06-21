FROM ubuntu:22.04

# Help documentation:
# This container seeds three Nessus-style CSV files under
# /home/user/scan_data/ for the penetration-testing post-processing task.
# The agent can merge, filter, summarise, and log findings without needing
# root privileges. Pytest is pre-installed so the grading harness can run
# its validation suite.

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/scan_data

RUN cat > /home/user/scan_data/segment_a.csv << 'EOF'
ip,port,service,version,vuln_status,cvss_score,cve
192.168.10.2,22,ssh,OpenSSH_7.2p2,no,0,
192.168.10.5,80,http,Apache 2.4.18,yes,7.5,CVE-2017-15710
192.168.10.7,443,https,nginx 1.10.3,no,0,
192.168.10.9,3306,mysql,5.7.29,yes,9.8,CVE-2020-14825
EOF

RUN cat > /home/user/scan_data/segment_b.csv << 'EOF'
ip,port,service,version,vuln_status,cvss_score,cve
192.168.20.4,21,ftp,vsftpd 3.0.3,no,0,
192.168.20.8,445,smb,Samba 4.3.11,yes,8.1,CVE-2017-7494
192.168.20.12,25,smtp,Postfix 3.1.0,no,0,
192.168.20.15,80,http,Apache 2.4.6,yes,6.5,CVE-2014-0226
EOF

RUN cat > /home/user/scan_data/segment_c.csv << 'EOF'
ip,port,service,version,vuln_status,cvss_score,cve
10.0.0.3,53,dns,BIND 9.10.3-P4,yes,7.8,CVE-2016-2776
10.0.0.5,22,ssh,OpenSSH_7.4,yes,5.3,CVE-2018-15473
10.0.0.8,3389,rdp,FreeRDP 2.0.0,no,0,
10.0.0.10,8080,http,Tomcat 9.0.31,yes,9.8,CVE-2020-1938
EOF

RUN chmod -R a+rX /home/user && \
    chmod 0777 /home/user

ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin

WORKDIR /home/user