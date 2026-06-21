FROM ubuntu:22.04

# Labels
LABEL Author="Compliance-Task-Setup"
LABEL Purpose="Initial evidence set for symbolic-link audit task"

# Help: Container pre-configured with the starting evidence set for the
# symbolic-link compliance audit exercise.

#------------------------------------------------------------------
# Basic tooling – install pytest (plus pip if missing)
#------------------------------------------------------------------
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pip && \
    pip3 install --no-cache-dir pytest

#------------------------------------------------------------------
# Create required directory tree under /home/user/
#------------------------------------------------------------------
RUN mkdir -p /home/user/data/original && \
    mkdir -p /home/user/data/archive && \
    mkdir -p /home/user/data/links

#------------------------------------------------------------------
# Populate regular files with exact contents (including trailing NL)
#------------------------------------------------------------------
RUN printf 'Compliance Document 1\n' > /home/user/data/original/doc1.txt && \
    printf 'Compliance Document 2\n' > /home/user/data/original/doc2.txt && \
    printf 'Backup 1\n' > /home/user/data/archive/doc1_backup.txt && \
    printf 'Backup 2\n' > /home/user/data/archive/doc2_backup.txt

#------------------------------------------------------------------
# Create symbolic links (two valid, two intentionally broken)
#------------------------------------------------------------------
RUN ln -sf ../original/doc1.txt /home/user/data/links/doc1_link && \
    ln -sf ../original/nonexistent.txt /home/user/data/links/doc2_link && \
    ln -sf ../archive /home/user/data/links/archive_link && \
    ln -sf ../old /home/user/data/links/old_link

#------------------------------------------------------------------
# Reasonable default permissions
#------------------------------------------------------------------
RUN chmod -R 755 /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

WORKDIR /home/user