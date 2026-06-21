# Converted from Apptainer def file
FROM ubuntu:22.04

# Install Python, pip, pytest
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create user home and sample file
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

RUN printf 'raw_image_01.jpg\nraw_image_02.jpg' > /home/user/sample_images.txt && \
    chmod 0666 /home/user/sample_images.txt

# Apply environment‑intended filesystem permission
RUN chmod 755 /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Labels
LABEL Author="Auto-generated for workflow setup task"

# Equivalent to %runscript
CMD sh -c "echo 'Container for workflow setup task. Use as base runtime image.'"