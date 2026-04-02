const express = require("express");
const router = express.Router();

const { html } = require("../utils");

router.get("/", (req, res) => {
  res.send(
    html(
      "ShopTech",
      `
    <p>Welcome to <b>ShopTech</b>, your number one stop for electronics.</p>
    <div class='card'>
      <h3>Featured Products</h3>
      <ul>
        <li>Laptop Pro X</li>
        <li>Smartphone 14</li>
        <li>Wireless Earbuds</li>
      </ul>
    </div>
    `
    )
  );
});

// VULN: Reflected XSS
router.get("/search", (req, res) => {
  const q = req.query.q || "";
  // VULNERABLE: reflects unsanitized input
  res.send(
    html(
      "Catalog Search",
      `
    <form method="GET">
      <input name="q" value="${q}" placeholder="Search products...">
      <button type="submit">Search</button>
    </form>
    <p>Results for: ${q}</p>
  `
    )
  );
});

router.get("/merge", (req, res) => {
  res.send(
    html(
      "User Preferences",
      `
    <p>Update your display preferences.</p>
    <textarea id="payload" rows="5">{"theme": "dark"}</textarea>
    <button onclick="doMerge()">Save</button>
    <pre id="result" style="display: none; margin-top: 20px;"></pre>
    <script>
    async function doMerge() {
      const r = await fetch('/api/merge', {
        method: 'POST', headers: {'Content-Type':'application/json'},
        body: document.getElementById('payload').value
      });
      const resultEl = document.getElementById('result');
      resultEl.style.display = 'block';
      resultEl.textContent = JSON.stringify(await r.json(), null, 2);
    }
    </script>`
    )
  );
});

module.exports = router;
