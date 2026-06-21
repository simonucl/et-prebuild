FROM ubuntu:22.04

# Help section
# Author: task-prep
# Description: Environment for Markdown-linter CI exercise

RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/experiments && \
    mkdir -p /home/user/tools

RUN cat > /home/user/experiments/README.md <<'EOF'
Experiment Tracking
===================
Some introduction
#Setup
Install instructions

#Results
accuracy: 0.95
EOF

RUN cat > /home/user/tools/md_lint.sh <<'EOF'
#!/usr/bin/env bash
# Very small ad-hoc Markdown linter used by the CI pipeline.
# Usage: ./md_lint.sh <markdown_file>

file="$1"
[ -f "$file" ] || { echo "File not found"; exit 1; }

errors=()

# Rule MD041 – first line must start with '# '
first_line="$(head -n 1 "$file")"
if [[ ! "$first_line" =~ ^#\  ]]; then
  errors+=("MD041 First line is not a top level header")
fi

# Rule MD022 – heading lines must be surrounded by blank lines
line_no=0
prev_blank=1
while IFS= read -r line || [ -n "$line" ]; do
  line_no=$((line_no+1))
  if [[ "$line" =~ ^# ]]; then
    if [[ $prev_blank -ne 1 ]]; then
      errors+=("MD022 Line $line_no heading not surrounded by blank line")
    fi
    prev_blank=0
  else
    if [[ -z "$line" ]]; then
      prev_blank=1
    else
      prev_blank=0
    fi
  fi
done < "$file"

printf "%s\n" "${errors[@]}"
    chmod 755 /home/user
EOF

RUN chmod 0755 /home/user/tools/md_lint.sh && \
    chmod -R a+rX /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8