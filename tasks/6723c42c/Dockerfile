FROM ubuntu:22.04

# Author "Apptainer prep for log-archiving task"
# Description "Container image that seeds the filesystem with specific log files for the diagnostic-archive exercise."

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/app/logs/old && \
    mkdir -p /home/user/diag

RUN chmod 755 /home/user && \
    chmod -R 755 /home/user/app && \
    chmod 755 /home/user/diag

# serviceA.log 153 600 bytes, mtime ≈1 h ago (<2 days)
RUN dd if=/dev/zero bs=1024 count=150 of=/home/user/app/logs/serviceA.log && \
    touch -d "1 hour ago" /home/user/app/logs/serviceA.log

# serviceB.log 81 920 bytes, mtime ≈25 h ago (<2 days)
RUN dd if=/dev/zero bs=1024 count=80 of=/home/user/app/logs/serviceB.log && \
    touch -d "25 hours ago" /home/user/app/logs/serviceB.log

# serviceC.log 307 200 bytes, mtime ≈9 days ago (>7 days)
RUN dd if=/dev/zero bs=1024 count=300 of=/home/user/app/logs/old/serviceC.log && \
    touch -d "9 days ago" /home/user/app/logs/old/serviceC.log

# debug.txt – small helper file (<10 KiB)
RUN echo "Debug information (placeholder)" > /home/user/app/logs/debug.txt

# Set reasonable permissions on the files
RUN chmod 644 /home/user/app/logs/serviceA.log && \
    chmod 644 /home/user/app/logs/serviceB.log && \
    chmod 644 /home/user/app/logs/old/serviceC.log && \
    chmod 644 /home/user/app/logs/debug.txt

CMD echo "This container is intended for the diagnostic-archive exercise." && \
    echo "Open a shell with: docker exec -it <container> /bin/bash" && \
    echo "Then follow the task instructions."