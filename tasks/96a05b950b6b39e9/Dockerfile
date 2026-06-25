FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    bash \
    ca-certificates \
    python3 \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash user
WORKDIR /home/user/work

RUN mkdir -p /home/user/work/packet_sentinel/packet_sentinel/rules \
    && printf '%s\n' \
      '"""Packet Sentinel rule inspection helpers."""' \
      '' \
      '__version__ = "1.2.0"' \
      > /home/user/work/packet_sentinel/packet_sentinel/__init__.py
RUN printf '%s\n' \
      'from __future__ import annotations' \
      '' \
      'import argparse' \
      'from importlib.resources import files' \
      '' \
      '' \
      'def load_default_rules() -> str:' \
      '    return files("packet_sentinel.rules").joinpath("defaults.toml").read_text()' \
      '' \
      '' \
      'def main(argv: list[str] | None = None) -> int:' \
      '    parser = argparse.ArgumentParser(prog="packet-sentinel")' \
      '    parser.add_argument("--show-defaults", action="store_true")' \
      '    args = parser.parse_args(argv)' \
      '    if args.show_defaults:' \
      '        print(load_default_rules(), end="")' \
      '    return 0' \
      > /home/user/work/packet_sentinel/packet_sentinel/cli.py
RUN printf '%s\n' \
      '[limits]' \
      'max_payload_bytes = 4096' \
      'max_header_bytes = 1024' \
      '' \
      '[actions]' \
      'drop_malformed = true' \
      'log_unknown_protocols = true' \
      > /home/user/work/packet_sentinel/packet_sentinel/rules/defaults.toml
RUN : > /home/user/work/packet_sentinel/packet_sentinel/py.typed
RUN printf '%s\n' \
      '# Packet Sentinel' \
      '' \
      'Packet Sentinel is an internal example package used for wheel publication drills.' \
      > /home/user/work/packet_sentinel/README.md
RUN chown -R user:user /home/user/work

USER user
WORKDIR /home/user/work/packet_sentinel
