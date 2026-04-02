---
name: add-vulnbank-vuln
description: Add a new intentional vulnerability to VulnBank (Flask). Use when the user wants to add a web vulnerability, create a new attack vector, or extend VulnBank with SQLi, XSS, CSRF, IDOR, or other OWASP flaws.
---

# Add Vulnerability to VulnBank

## Prerequisites

- VulnBank app: `labs/vulnbank/app.py`
- Existing vulns are marked with `# VULN: [category] - [description]`

## Workflow

### Step 1: Identify the vulnerability type

Common OWASP categories:
- SQL Injection, XSS (Reflected/Stored/DOM), CSRF, IDOR
- Broken Authentication, Broken Access Control
- Mass Assignment, Information Disclosure
- Insecure File Upload, Path Traversal, SSRF

### Step 2: Create the route

Add a new route in `labs/vulnbank/app.py` (or in `labs/vulnbank/app/routes/` if modularized).

**Template:**

```python
# VULN: [Category] - [Short description]
@app.route("/vuln-endpoint", methods=["GET", "POST"])
def vuln_name():
    # VULNERABLE: explanation of why this is insecure
    ...
    return render_template_string(BASE_TEMPLATE,
        title="Feature Name",
        content=f"""
        <div class='card'>
            <!-- UI for the feature -->
        </div>
        <p><small>Hint: [attack hint for learners]</small></p>
        """)
```

### Step 3: Add a template (if needed)

If the vuln has UI, add it inline via `render_template_string` (current pattern) or as a file in `labs/vulnbank/app/templates/`.

### Step 4: Document the vulnerability

Add an entry to `labs/vulnbank/vulns/VULNERABILITIES.md`:

```markdown
## [Category] - [Name]

- **Route**: `/endpoint`
- **Method**: GET/POST
- **Description**: What the vulnerability is
- **How to exploit**: Step-by-step attack
- **Impact**: What an attacker gains
- **Flag**: `FLAG{...}` (if applicable)
```

### Step 5: Add a test

Add a test in `labs/vulnbank/tests/test_vulns.py`:

```python
def test_vuln_name(client):
    response = client.get("/vuln-endpoint?param=payload")
    assert b"expected_output" in response.data
```

### Step 6: Verify

- [ ] Route works and is exploitable
- [ ] `# VULN:` comment present on vulnerable code
- [ ] Hint visible in UI for learners
- [ ] Documented in VULNERABILITIES.md
- [ ] Test added and passing
