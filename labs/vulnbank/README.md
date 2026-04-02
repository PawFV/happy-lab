# SecBank (VulnBank)

An intentionally vulnerable Flask application simulating a bank's online portal.

## Vulnerabilities & Pentesting Instructions

### 1. SQL Injection (Login)

- **Where**: `/login` form
- **Technique**: Authentication bypass via SQL injection. The query is built by string concatenation with no parameterized queries.
- **Tools**: Browser, `curl`, `Burp Suite`, `sqlmap`
- **Hint**: Think about how a SQL `WHERE` clause evaluates boolean logic. What happens if you make the condition always true?

### 2. SQL Injection (Search)

- **Where**: `/search` route, `q` parameter
- **Technique**: UNION-based SQL injection. The input goes directly into a `SELECT` query.
- **Tools**: `sqlmap`, `Burp Suite`, manual injection via browser
- **Hint**: First figure out how many columns the original query returns (try different column counts in a `UNION SELECT`). Then use that to extract data from other tables.

### 3. Cross-Site Scripting (XSS)

- **Reflected XSS**: `/search` — the `q` parameter is reflected in the response without encoding.
- **Stored XSS**: `/posts` — logged-in users can create posts whose content is rendered as raw HTML.
- **Technique**: Inject JavaScript that executes in a victim's browser context.
- **Tools**: Browser dev tools, `Burp Suite`, `XSS Hunter`
- **Hint**: Try different HTML tags and event handlers. Not all payloads need `<script>` tags.

### 4. Insecure Direct Object Reference (IDOR)

- **Where**: `/profile/<id>`
- **Technique**: Horizontal privilege escalation by manipulating the resource ID in the URL.
- **Tools**: Browser, `curl`, `Burp Suite Intruder`
- **Hint**: Log in as any user. Then iterate through different profile IDs. Some users have data you shouldn't be able to see.

### 5. Broken Access Control

- **Where**: `/admin/users`
- **Technique**: The endpoint exists but may lack proper authorization checks.
- **Tools**: Browser, `curl`, `dirb`, `gobuster`
- **Hint**: Try accessing admin routes directly without being logged in or without the admin role. Check `robots.txt` for clues.

### 6. Unrestricted File Upload

- **Where**: `/upload`
- **Technique**: Upload files with dangerous extensions or content types that the server accepts without validation.
- **Tools**: `curl`, `Burp Suite`
- **Hint**: What happens if you upload a file with a `.py`, `.php`, or `.html` extension? Does the server check anything beyond the filename?

### 7. Path Traversal

- **Where**: `/download?file=`
- **Technique**: Directory traversal using relative path sequences to escape the intended directory.
- **Tools**: Browser, `curl`, `Burp Suite`
- **Hint**: The `file` parameter is passed to the filesystem without sanitization. Think about `../` sequences and what files you could reach on the host.

### 8. Information Disclosure

- **Where**: Multiple endpoints
- **Technique**: Sensitive information exposed through debug endpoints, backup files, and configuration hints.
- **Tools**: Browser, `curl`, `dirb`, `gobuster`
- **Hint**: Enumerate the application thoroughly. Check common paths like `/debug`, `/backup`, `/robots.txt`. Developers often leave diagnostic endpoints exposed.

## Testing

To run the VulnBank test suite locally, you **must** have a real MySQL instance running, because tests validate SQL injection vulnerabilities using the actual database engine.

```bash
# Start MySQL in the background from the project root
cd ../../
docker compose up -d mysql

# Run pytest inside the vulnbank directory
cd labs/vulnbank
pytest tests/ -v
```