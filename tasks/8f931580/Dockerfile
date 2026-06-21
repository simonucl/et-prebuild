FROM ubuntu:22.04

# Help / runscript notes
# Container for the 'critical remote-access services' task.
# You are inside the Apptainer image. Proceed with the exercise as instructed.

ENV PYTHONUNBUFFERED=1
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/scans

RUN cat << 'EOF' > /home/user/scans/full_scan.log
Starting Nmap 7.80 ( https://nmap.org ) at 2023-11-18 14:12 UTC
Nmap scan report for target1.local (192.168.0.5)
Host is up (0.00032s latency).
Not shown: 997 closed ports
PORT     STATE SERVICE     VERSION
22/tcp   open  ssh         OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http        Apache httpd 2.4.41 ((Ubuntu))
443/tcp  open  ssl/http    Apache httpd 2.4.41 ((Ubuntu))
| ssl-cert: Subject: commonName=target1.local
|_Not valid before: 2020-01-15T12:49:00
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Nmap scan report for 192.168.0.10
Host is up (0.0011s latency).
Not shown: 996 closed ports
PORT     STATE SERVICE VERSION
21/tcp   open  ftp     vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| -
|_-rw-r--r--   1 ftp      ftp          1234 Jan 01 2020 readme.txt
23/tcp   open  telnet  Linux telnetd
445/tcp  open  smb      Samba smbd 4.11.6 (workgroup: WORKGROUP)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Nmap done: 2 IP addresses (2 hosts up) scanned in 8.71 seconds
EOF

RUN chmod 755 /home && \
    chmod 755 /home/user && \
    chmod 755 /home/user/scans && \
    chmod 644 /home/user/scans/full_scan.log