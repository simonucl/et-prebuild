# This container supplies the initial filesystem state for the “Generate an
# integrity-verification report by cutting and pasting specific columns” task.
# Key points:
# • Provides the two pre-populated snapshot TSV files under /home/user/data/.
# • Includes Python 3 and pytest for automated grading.

FROM ubuntu:22.04

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN useradd -m -s /bin/bash user

RUN mkdir -p /home/user/data/primary && \
    mkdir -p /home/user/data/backup

RUN cat > /home/user/data/primary/data_snapshot_20230914.tsv <<'EOF'
id	filename	sha256	bytes	mtime
1	img001.jpg	d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2	204800	2023-09-14T08:30:00Z
2	document.pdf	afafafafafafafafafafafafafafafafafafafafafafafafafafafafafafafaf	102400	2023-09-14T08:31:00Z
3	db_backup.sql.bz2	bbb111bbb111bbb111bbb111bbb111bbb111bbb111bbb111bbb111bbb111bbb1	512000	2023-09-14T08:32:00Z
4	logs.tar.gz	cccc222cccc222cccc222cccc222cccc222cccc222cccc222cccc222cccc222c	307200	2023-09-14T08:35:00Z
EOF

RUN cat > /home/user/data/backup/data_snapshot_20230914.tsv <<'EOF'
id	filename	sha256	bytes	mtime
1	img001.jpg	d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2	204800	2023-09-14T08:30:01Z
2	document.pdf	afafafafafafafafafafafafafafafafafafafafafafafafafafafafafafafaf	102400	2023-09-14T08:31:03Z
3	db_backup.sql.bz2	zzz333zzz333zzz333zzz333zzz333zzz333zzz333zzz333zzz333zzz333z	512000	2023-09-14T08:32:05Z
4	logs.tar.gz	cccc222cccc222cccc222cccc222cccc222cccc222cccc222cccc222cccc222c	307200	2023-09-14T08:35:07Z
EOF

RUN chmod 644 /home/user/data/primary/data_snapshot_20230914.tsv && \
    chmod 644 /home/user/data/backup/data_snapshot_20230914.tsv && \
    chown -R user:user /home/user && \
    chmod 755 /home/user

CMD ["/bin/bash"]