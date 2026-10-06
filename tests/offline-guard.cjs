"use strict";
const fs = require("node:fs");
function reject() {
  if (process.env.ASTACK_NETWORK_ATTEMPTS)
    fs.appendFileSync(
      process.env.ASTACK_NETWORK_ATTEMPTS,
      "network attempted\n",
    );
  throw new Error("Network disabled by handoff test tripwire");
}
for (const name of [
  "node:net",
  "node:tls",
  "node:http",
  "node:https",
  "node:dgram",
  "node:dns",
]) {
  const module = require(name);
  for (const key of [
    "connect",
    "createConnection",
    "request",
    "get",
    "createSocket",
    "lookup",
    "resolve",
    "resolve4",
    "resolve6",
  ])
    if (typeof module[key] === "function") module[key] = reject;
  if (module.promises)
    for (const key of ["lookup", "resolve", "resolve4", "resolve6"])
      if (typeof module.promises[key] === "function")
        module.promises[key] = reject;
}
require("node:net").Socket.prototype.connect = reject;
globalThis.fetch = reject;
