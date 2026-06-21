FROM ubuntu:22.04

# Install Python and pytest
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Create required directory structure and reference files
RUN mkdir -p /home/user/system_info

# timezone.conf – must be exactly "Etc/UTC\n"
RUN printf 'Etc/UTC\n' > /home/user/system_info/timezone.conf

# locale.conf – must be exactly "en_US.UTF-8\n"
RUN printf 'en_US.UTF-8\n' > /home/user/system_info/locale.conf

# Set sane permissions
RUN chmod 0755 /home/user && \
    chmod 0755 /home/user/system_info && \
    chmod 0644 /home/user/system_info/timezone.conf /home/user/system_info/locale.conf

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Runscript equivalent as default command
CMD ["echo", "Docker image for the Environment Manifest task. Start an interactive shell with: docker run -it <image> /bin/bash"]