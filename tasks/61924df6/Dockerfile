FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update -y && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    ln -sf /usr/bin/python3 /usr/bin/python

# Create initial project structure expected by the grading tests
RUN mkdir -p /home/user/project/src && \
    mkdir -p /home/user/project/logs

# Create main.py with the required metadata and TAB characters
RUN cat > /home/user/project/src/main.py <<'PYMAIN'
"""
Author: John Doe
Last Modified: 2023-05-12
"""

def main():	# contains one literal TAB before the comment
	print("Hello World")	# line begins with one literal TAB
PYMAIN

# Create utils.py with the required metadata and TAB characters
RUN cat > /home/user/project/src/utils.py <<'PYUTILS'
"""
Author: Jane Smith
Last Modified: 2023-05-11
"""

def helper():	# contains one literal TAB before the comment
	print("Utility")	# line begins with one literal TAB
PYUTILS

# Create db.py with the required metadata and TAB characters
RUN cat > /home/user/project/src/db.py <<'PYDB'
"""
Author: Alice Brown
Last Modified: 2023-05-10
"""

def connect():	# contains one literal TAB before the comment
	print("DB connect")	# line begins with one literal TAB
PYDB

# Ensure permissions allow the non-root runtime user to modify files
RUN chmod -R a+rwx /home/user

# Set environment variables
ENV PYTHONIOENCODING="utf-8"

# Set working directory
WORKDIR /home/user

CMD ["echo", "Container for the text-processing task. Use this image to run your solution."]