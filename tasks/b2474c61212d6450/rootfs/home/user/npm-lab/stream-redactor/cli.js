#!/usr/bin/env node
"use strict";

const { redact } = require("./index.js");

let data = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", chunk => {
  data += chunk;
});
process.stdin.on("end", () => {
  process.stdout.write(redact(data));
});
