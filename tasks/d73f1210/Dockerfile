FROM ubuntu:22.04

# Update package lists and install Python + pip
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip

# Install pytest for the forthcoming test-suite
RUN pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Prepare the required directory tree and seed data files
# ------------------------------------------------------------------
# Create user home directory if it does not yet exist
RUN mkdir -p /home/user

# Workflow structure
RUN mkdir -p /home/user/workflow/incoming && \
    mkdir -p /home/user/workflow/archive

# Seed the incoming *.dat files
RUN printf "JAN DATA\n" > /home/user/workflow/incoming/january.dat && \
    printf "FEB DATA\n" > /home/user/workflow/incoming/february.dat && \
    printf "MAR DATA\n" > /home/user/workflow/incoming/march.dat

# Seed the readme.txt file
RUN printf "Put data files here.\n" > /home/user/workflow/incoming/readme.txt

# Ensure everything is writeable by the (non-root) runtime user
RUN chmod -R a+rwx /home/user/workflow

# Set permissions on home directory
RUN chmod 755 /home/user

# Make sure Python user-installed binaries are found
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Default entrypoint: start an interactive shell
CMD ["/bin/bash"]