FROM ubuntu:22.04

# Begin help/label information
LABEL Author="backup-admin"
LABEL Description="Container for the daily backup exercise – initial state only (pytest included)."
# End help/label information

RUN set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        tar \
        gzip \
        coreutils && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/data_alpha \
             /home/user/data_bravo \
             /home/user/data_charlie

RUN printf "alpha one\n"  > /home/user/data_alpha/file1.txt && \
    printf "alpha two\n"  > /home/user/data_alpha/file2.txt

RUN printf "bravo three\n" > /home/user/data_bravo/file3.txt && \
    printf "bravo four\n"  > /home/user/data_bravo/file4.txt

RUN printf "# Charlie Data\nSome content.\n" > /home/user/data_charlie/readme.md

RUN chmod -R 0777 /home/user

RUN chmod 755 /home/user