/**
 * Vulnerable Node.js App — SecLab
 * INTENTIONALLY INSECURE — For use in isolated networks only
 *
 * Vulnerabilities: NoSQL Injection, Prototype Pollution,
 * Path Traversal, XSS, Insecure Deserialization, SSRF
 */

const express = require("express");
const path = require("path");
const fs = require("fs");

const { registerRoutes } = require("./routes");

const app = express();
const PORT = process.env.PORT || 3001;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

registerRoutes(app);

// Create public directory with test file
const publicDir = path.join(__dirname, "public");
if (!fs.existsSync(publicDir)) {
  fs.mkdirSync(publicDir, { recursive: true });
  fs.writeFileSync(
    path.join(publicDir, "readme.txt"),
    "FLAG{path_traversal_found}\nThis is a public test file.\n"
  );
}

if (require.main === module) {
  app.listen(PORT, "0.0.0.0", () => {
    console.log(`VulnNode running at http://0.0.0.0:${PORT}`);
  });
}

module.exports = app;
