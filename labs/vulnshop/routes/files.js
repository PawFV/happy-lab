const express = require("express");
const path = require("path");
const http = require("http");
const router = express.Router();

const { html } = require("../utils");

// VULN: Path Traversal
router.get("/files", (req, res) => {
  const name = req.query.name;
  if (!name) {
    return res.send(
      html(
        "Digital Downloads",
        `
      <p>Download manuals and software: <code>/files?name=readme.txt</code></p>
    `
      )
    );
  }
  // VULNERABLE: path is not sanitized
  const filePath = path.join(__dirname, "..", "public", name);
  res.sendFile(filePath, (err) => {
    if (err) res.status(404).send(`Error: ${err.message}`);
  });
});

// VULN: SSRF
router.get("/fetch", (req, res) => {
  const url = req.query.url;
  if (!url) {
    return res.send(
      html(
        "Track Order",
        `
      <form method="GET">
        <input name="url" placeholder="Tracking API URL" value="http://api.tracking.local/status/12345">
        <button type="submit">Track</button>
      </form>
    `
      )
    );
  }

  // VULNERABLE: fetches any URL, including internal
  http
    .get(url, (response) => {
      let data = "";
      response.on("data", (chunk) => (data += chunk));
      response.on("end", () => {
        res.send(
          html(
            "Tracking Result",
            `
        <p>Tracking from: <code>${url}</code></p>
        <p>Status: ${response.statusCode}</p>
        <pre>${data}</pre>
      `
          )
        );
      });
    })
    .on("error", (err) => {
      res.send(html("Error", `<p>Error: ${err.message}</p>`));
    });
});

module.exports = router;
