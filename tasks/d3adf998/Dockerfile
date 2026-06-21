FROM ubuntu:22.04

# Labels
LABEL Author="frequency-utility-container"
LABEL Description="Initial state for the frequency counter task. Contains /home/user/dev-utils/words.txt and pytest installed."

# Set non-interactive frontend for apt
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install Python tooling
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        locales \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Generate a UTF-8 locale for Python / pytest
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && \
    locale-gen

# Install pytest for the test harness
RUN pip3 install --no-cache-dir pytest

# Create the home/user directory structure
RUN mkdir -p /home/user/dev-utils

# Create words.txt with the expected content
RUN cat > /home/user/dev-utils/words.txt <<'EOF'
apple
banana
apple
orange
banana
apple
grape
EOF

# Ensure correct permissions
RUN chmod 0755 /home/user/dev-utils && \
    chmod 0644 /home/user/dev-utils/words.txt && \
    chmod 755 /home/user

# Environment variables for locale
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV LANGUAGE=C.UTF-8

# Set working directory
WORKDIR /home/user

# Default command
CMD ["/bin/bash", "-c", "echo 'Container for the frequency-counter task.' && echo 'You can open a shell with: docker exec -it <container> /bin/bash'"]