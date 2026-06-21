FROM ubuntu:22.04

# Update package lists and install Python tooling
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest

# Create the initial directory structure and build log
RUN mkdir -p /home/user/build_logs

RUN cat <<'EOF' >/home/user/build_logs/build.log
[2023-07-14 10:23:45] INFO Uploaded artifact: commons-lang3-3.12.0.jar (size 290381 bytes)
[2023-07-14 10:23:46] INFO Uploaded artifact: myapp-1.0.0.tar.gz (size 1839201 bytes)
[2023-07-14 10:23:47] WARN Skipped artifact: guava-31.0.1.jar - already exists
[2023-07-14 10:23:48] INFO Uploaded artifact: guava-31.0.1.jar (size 2798096 bytes)
[2023-07-14 10:23:49] ERROR Failed to upload artifact: invalid-file.txt
some unrelated line
[2023-07-14 10:23:50] INFO Uploaded artifact: junit-4.13.2.jar (size 238947 bytes)
EOF

# Ensure the directory (and its contents) are writable by whichever user
# runs inside the container.
RUN chmod -R 777 /home/user/build_logs

RUN chmod 755 /home/user

# Labels
LABEL Author="CI-BuildEngineer"