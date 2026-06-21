# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help section converted as comments
# Pre-supplied Nmap XML scan creation and Python/pytest installation

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/raw_scans

RUN cat >/home/user/raw_scans/nmap_scan1.xml <<'EOF'
<?xml version="1.0"?>
<!DOCTYPE nmaprun>
<nmaprun scanner="nmap" args="nmap -oX -" start="1234567890">
<host>
  <status state="up" reason="syn-ack"/>
  <address addr="192.168.1.10" addrtype="ipv4"/>
  <ports>
    <port protocol="tcp" portid="22">
      <state state="open" reason="syn-ack" />
      <service name="ssh" />
    </port>
    <port protocol="tcp" portid="80">
      <state state="open" reason="syn-ack" />
      <service name="http" />
    </port>
    <port protocol="tcp" portid="3306">
      <state state="closed" />
      <service name="mysql" />
    </port>
  </ports>
</host>
<host>
  <status state="up" reason="syn-ack"/>
  <address addr="192.168.1.11" addrtype="ipv4"/>
  <ports>
    <port protocol="tcp" portid="21">
      <state state="open" reason="syn-ack" />
      <service name="ftp" />
    </port>
    <port protocol="tcp" portid="139">
      <state state="open" reason="syn-ack" />
      <service name="netbios-ssn" />
    </port>
    <port protocol="tcp" portid="445">
      <state state="open" reason="syn-ack" />
      <service name="microsoft-ds" />
    </port>
  </ports>
</host>
</nmaprun>
EOF

RUN chmod 0644 /home/user/raw_scans/nmap_scan1.xml && \
    chmod 755 /home/user

ENV PATH="/usr/local/bin:${PATH}"