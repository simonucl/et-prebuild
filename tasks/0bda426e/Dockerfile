FROM ubuntu:22.04

# Author Vulnerability-Report-Setup
# Description "Base image for the 'Generate a consolidated vulnerability report from provided Nmap XML data' task. Provides prerequisite scan data and pytest for validation."

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /home/user/scan_data && \
    mkdir -p /home/user/vuln_scan

RUN cat > /home/user/scan_data/initial_scan.xml <<'EOF'
<?xml version="1.0"?>
<nmaprun>
 <host>
  <address addr="192.168.56.10" addrtype="ipv4"/>
  <ports>
   <port protocol="tcp" portid="22">
    <state state="open"/>
    <service name="ssh" product="OpenSSH" version="7.2p2"/>
   </port>
   <port protocol="tcp" portid="80">
    <state state="open"/>
    <service name="http" product="Apache httpd" version="2.4.18"/>
   </port>
  </ports>
 </host>
 <host>
  <address addr="192.168.56.12" addrtype="ipv4"/>
  <ports>
   <port protocol="tcp" portid="21">
    <state state="open"/>
    <service name="ftp" product="vsftpd" version="3.0.3"/>
   </port>
   <port protocol="tcp" portid="445">
    <state state="open"/>
    <service name="microsoft-ds" product="Samba smbd" version="3.6.25"/>
   </port>
  </ports>
 </host>
 <host>
  <address addr="192.168.56.15" addrtype="ipv4"/>
  <ports>
   <port protocol="tcp" portid="3306">
    <state state="open"/>
    <service name="mysql" product="MySQL" version="5.5.49"/>
   </port>
  </ports>
 </host>
</nmaprun>
EOF

RUN cat > /home/user/scan_data/cve_mapping.csv <<'EOF'
service,version,cve_reference
OpenSSH,7.2p2,CVE-2016-6515
Apache httpd,2.4.18,CVE-2017-3167
vsftpd,3.0.3,CVE-2015-1419
Samba smbd,3.6.25,CVE-2017-7494
MySQL,5.5.49,CVE-2016-6662
EOF

RUN chmod 755 /home/user && \
    chmod 755 /home/user/scan_data && \
    chmod 755 /home/user/vuln_scan && \
    chmod 644 /home/user/scan_data/initial_scan.xml && \
    chmod 644 /home/user/scan_data/cve_mapping.csv