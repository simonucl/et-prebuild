FROM ubuntu:22.04

# Update package index and install Python tooling
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip

# Install pytest for the forthcoming tests
RUN pip3 install --no-cache-dir pytest

# Prepare initial filesystem state required by the exercise
# 1. Create the /home/user hierarchy
RUN mkdir -p /home/user/docs

# 2. Ensure the writer (the non-root user who will run inside the
#    container) can create new items inside /home/user/docs.
RUN chmod 777 /home/user/docs

# 3. Create the empty placeholder PDF
RUN touch /home/user/docs/manual_v1.2.pdf && \
    chmod 666 /home/user/docs/manual_v1.2.pdf

# Make absolutely sure the file is empty
RUN : > /home/user/docs/manual_v1.2.pdf

# Set permissions on /home/user
RUN chmod 755 /home/user

# Keep Python output unbuffered for nicer UX during automated runs
ENV PYTHONUNBUFFERED=1

# Labels
LABEL Author="GPT-created Apptainer definition for checksum task"