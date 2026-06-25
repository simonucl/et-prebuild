const assert = require("assert");
const { redact } = require("../index.js");

assert.strictEqual(redact("api_key=abc123 token=xyz"), "api_key=[REDACTED] token=[REDACTED]");
