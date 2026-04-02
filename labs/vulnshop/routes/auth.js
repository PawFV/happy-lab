const express = require("express");
const router = express.Router();

const { users, sessions } = require("../data");
const { html } = require("../utils");

// VULN: NoSQL-style Injection
router.post("/api/login", (req, res) => {
  const { username, password } = req.body;

  // VULNERABLE: allows objects as password (NoSQL-style)
  const user = users.find((u) => {
    if (typeof password === "object" && password !== null) {
      if (password["$ne"] !== undefined)
        return u.username === username && u.password !== password["$ne"];
      if (password["$gt"] !== undefined)
        return u.username === username && u.password > password["$gt"];
      if (password["$regex"] !== undefined)
        return (
          u.username === username &&
          new RegExp(password["$regex"]).test(u.password)
        );
    }
    return u.username === username && u.password === password;
  });

  if (user) {
    const token = Math.random().toString(36).substring(2);
    sessions[token] = {
      userId: user.id,
      username: user.username,
      role: user.role,
    };
    res.json({
      success: true,
      token,
      user: { id: user.id, username: user.username, role: user.role },
    });
  } else {
    res.status(401).json({ error: "Invalid credentials" });
  }
});

router.get("/login", (req, res) => {
  res.send(
    html(
      "Account Login",
      `
    <form id="loginForm">
      <input id="user" placeholder="Username"><br>
      <input id="pass" type="password" placeholder="Password"><br>
      <button type="submit">Login</button>
    </form>
    <pre id="result" style="display: none; margin-top: 20px;"></pre>
    <script>
    document.getElementById('loginForm').onsubmit = async (e) => {
      e.preventDefault();
      const r = await fetch('/api/login', {
        method: 'POST', headers: {'Content-Type':'application/json'},
        body: JSON.stringify({username: document.getElementById('user').value, password: document.getElementById('pass').value})
      });
      const resultEl = document.getElementById('result');
      resultEl.style.display = 'block';
      resultEl.textContent = JSON.stringify(await r.json(), null, 2);
    };
    </script>`
    )
  );
});

module.exports = router;
