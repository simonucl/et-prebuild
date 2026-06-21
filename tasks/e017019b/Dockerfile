FROM ubuntu:22.04

# Ensure non-interactive apt operations
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install Python + pip
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grading harness
RUN pip3 install --no-cache-dir pytest

# Create initial required directory and CSV for the student
RUN mkdir -p /home/user/scan_results && \
    chmod 755 /home/user && \
    chmod 755 /home/user/scan_results

# Create the raw_scan.csv file
RUN cat > /home/user/scan_results/raw_scan.csv <<'CSVEOF'
target_ip,hostname,port,service,cve_id,cvss_score,severity,description
192.168.1.10,webserver1,80,http,CVE-2021-1234,7.5,HIGH,Some description
192.168.1.11,db1,3306,mysql,CVE-2020-9999,5.3,MEDIUM,Some description
192.168.1.12,ftp1,21,ftp,CVE-2019-2222,9.8,CRITICAL,Some description
192.168.1.10,webserver1,443,https,CVE-2021-5678,4.3,LOW,Some description
192.168.1.13,app1,8080,http,CVE-2022-1111,8.0,HIGH,Some description
192.168.1.12,ftp1,21,ftp,CVE-2019-3333,6.1,MEDIUM,Some description
192.168.1.14,mail,25,smtp,CVE-2021-0001,10.0,CRITICAL,Some description
192.168.1.10,webserver1,80,http,CVE-2021-7777,9.0,CRITICAL,Some description
192.168.1.13,app1,8080,http,CVE-2022-2222,9.5,CRITICAL,Some description
192.168.1.11,db1,3306,mysql,CVE-2020-8888,7.0,HIGH,Some description
CSVEOF

# Guarantee file has LF newline termination and correct permissions
RUN printf '\n' >> /home/user/scan_results/raw_scan.csv && \
    chmod 644 /home/user/scan_results/raw_scan.csv

# Environment variables
ENV PYTHONIOENCODING=UTF-8

# Create symlink for python command
RUN ln -sf /usr/bin/python3 /usr/bin/python

WORKDIR /home/user

CMD ["/bin/bash"]