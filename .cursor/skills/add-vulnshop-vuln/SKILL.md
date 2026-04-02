---
name: add-vulnshop-vuln
description: Add a new intentional vulnerability to VulnShop (Express/Node.js). Use when the user wants to add command injection, SSRF, deserialization, path traversal, JWT manipulation, NoSQL injection, prototype pollution, or other Node.js-specific flaws.
---

# Add Vulnerability to VulnShop

## Prerequisites

- VulnShop app: `labs/vulnshop/index.js`
- Existing vulns are marked with `// VULN: [category] - [description]`

## Workflow

### Step 1: Identify the vulnerability type

Common Node.js attack vectors:
- NoSQL Injection, Prototype Pollution, Command Injection
- SSRF, Insecure Deserialization, Path Traversal
- JWT Manipulation, Unrestricted Upload, XSS

### Step 2: Create the route

Add in `labs/vulnshop/index.js` (or in `labs/vulnshop/src/routes/` if modularized).

**API endpoint template:**

```javascript
// VULN: [Category] - [Short description]
app.post("/api/vuln-endpoint", (req, res) => {
  // VULNERABLE: explanation of why this is insecure
  const userInput = req.body.param;
  // ... insecure logic ...
  res.json({ result });
});
```

**UI page template:**

```javascript
app.get("/vuln-page", (req, res) => {
  res.send(html("Feature Name", `
    <p>Description</p>
    <form><!-- interactive UI --></form>
    <p><small>Hint: [attack hint for learners]</small></p>
  `));
});
```

### Step 3: Add dependencies (if needed)

```bash
cd labs/vulnshop && pnpm add <package>
```

### Step 4: Document the vulnerability

Add an entry to `labs/vulnshop/vulns/VULNERABILITIES.md`:

```markdown
## [Category] - [Name]

- **Route**: `/api/endpoint`
- **Method**: GET/POST
- **Description**: What the vulnerability is
- **How to exploit**: curl command or step-by-step
- **Impact**: What an attacker gains
- **Flag**: `FLAG{...}` (if applicable)
```

### Step 5: Add a test

Add a test in `labs/vulnshop/tests/test_vulns.js`:

```javascript
const assert = require("assert");
const http = require("http");

// test vuln-name
// ...
```

### Step 6: Verify

- [ ] Route works and is exploitable
- [ ] `// VULN:` comment present on vulnerable code
- [ ] Hint visible in UI for learners
- [ ] Documented in VULNERABILITIES.md
- [ ] Test added and passing
