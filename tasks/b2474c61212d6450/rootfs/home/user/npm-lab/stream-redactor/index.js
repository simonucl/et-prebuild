"use strict";

const DEFAULT_PATTERNS = [
  /(api[_-]?key=)[A-Za-z0-9_-]+/gi,
  /(token=)[A-Za-z0-9._-]+/gi,
  /(password=)[^&\s]+/gi
];

function redact(input) {
  let output = String(input);
  for (const pattern of DEFAULT_PATTERNS) {
    output = output.replace(pattern, "$1[REDACTED]");
  }
  return output;
}

module.exports = { redact };
