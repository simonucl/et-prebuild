FROM ubuntu:22.04

# Help / metadata
LABEL Author="Container setup for profiling hot-spots task"
LABEL Description="Provides initial state and dependencies for the performance profiling exercise."

ENV PATH=/usr/local/bin:$PATH

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        jq \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools
RUN python3 -m pip install --no-cache-dir pytest

RUN mkdir -p /home/user/app_profiling && \
    chmod 755 /home/user && \
    chmod 755 /home/user/app_profiling

RUN cat >/home/user/app_profiling/profile_schema.json <<'EOF'
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "array",
  "items": {
    "type": "object",
    "required": ["function", "calls", "avg_ms"],
    "additionalProperties": false,
    "properties": {
      "function": { "type": "string" },
      "calls":    { "type": "integer", "minimum": 0 },
      "avg_ms":   { "type": "number",  "minimum": 0 }
    }
  },
  "minItems": 1
}
EOF

RUN cat >/home/user/app_profiling/raw_profile.json <<'EOF'
[
  { "function": "core.init",        "calls": 1,   "avg_ms": 5.0  },
  { "function": "engine.render",    "calls": 90,  "avg_ms": 12.4 },
  { "function": "engine.update",    "calls": 90,  "avg_ms": 15.8 },
  { "function": "engine.physics",   "calls": 90,  "avg_ms": 7.1  },
  { "function": "core.cleanup",     "calls": 1,   "avg_ms": 3.2  }
]
EOF

RUN chmod 644 /home/user/app_profiling/profile_schema.json && \
    chmod 644 /home/user/app_profiling/raw_profile.json