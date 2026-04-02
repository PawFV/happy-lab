const express = require("express");
const router = express.Router();

const { users, messages, config } = require("../data");

// VULN: IDOR in messages
router.get("/api/messages/:username", (req, res) => {
  // VULNERABLE: does not check if current user has access
  const userMessages = messages.filter(
    (m) => m.to === req.params.username || m.from === req.params.username
  );
  res.json(userMessages);
});

// VULN: Info Disclosure
router.get("/api/config", (req, res) => {
  // VULNERABLE: exposes internal config
  res.json({
    ...config,
    env: process.env,
    nodeVersion: process.version,
    platform: process.platform,
    memoryUsage: process.memoryUsage(),
    flag: "FLAG{config_endpoint_exposed}",
  });
});

// VULN: List users with sensitive data
router.get("/api/users", (req, res) => {
  // VULNERABLE: exposes passwords and secrets
  const role = req.query.role;
  if (role) {
    const filtered = users.filter((u) => u.role === role);
    return res.json(filtered);
  }
  res.json(users);
});

// VULN: Prototype Pollution
router.post("/api/merge", (req, res) => {
  const target = { type: "default", priority: "low" };
  const source = req.body;

  // VULNERABLE: deep merge does not sanitize __proto__
  function deepMerge(target, source) {
    for (const key in source) {
      if (
        typeof source[key] === "object" &&
        source[key] !== null &&
        !Array.isArray(source[key])
      ) {
        if (!target[key]) target[key] = {};
        deepMerge(target[key], source[key]);
      } else {
        target[key] = source[key];
      }
    }
    return target;
  }

  const result = deepMerge(target, source);
  res.json({
    merged: result,
    polluted: {}.polluted || false,
    isAdmin: {}.isAdmin || false,
  });
});

module.exports = router;
