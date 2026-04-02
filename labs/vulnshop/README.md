# ShopTech (VulnShop)

An intentionally vulnerable Express.js application simulating an e-commerce platform.

## Vulnerabilities & Pentesting Instructions

### 1. NoSQL-style Injection (Login)

- **Where**: `/api/login` (JSON body)
- **Technique**: The login logic parses the JSON body and uses a custom comparison that mimics NoSQL query operators.
- **Tools**: `curl`, `Burp Suite`, `Postman`
- **Hint**: What happens if the `password` field is not a string but an object? Research MongoDB query operators like `$ne`, `$gt`, `$regex` and think about how they could be abused in a comparison.

### 2. Prototype Pollution

- **Where**: `/api/merge`
- **Technique**: A recursive deep merge function that doesn't sanitize special keys, allowing modification of the object prototype chain.
- **Tools**: `curl`, `Burp Suite`, browser dev console
- **Hint**: JavaScript objects inherit properties from `Object.prototype`. If you can write to `__proto__`, you can add properties that every object in the application will inherit. What properties might change the app's behavior?

### 3. Insecure Direct Object Reference (IDOR)

- **Where**: `/api/messages/:username`
- **Technique**: Accessing another user's resources by changing the identifier in the URL without proper authorization checks.
- **Tools**: `curl`, `Burp Suite`
- **Hint**: The endpoint takes a username in the URL path. Try requesting messages for usernames other than your own. Enumerate users first via other endpoints.

### 4. Server-Side Request Forgery (SSRF)

- **Where**: `/fetch?url=`
- **Technique**: The server makes HTTP requests on your behalf to arbitrary URLs, including internal services not exposed to the outside.
- **Tools**: `curl`, `Burp Suite`, `Collaborator`
- **Hint**: What internal services might be running on `localhost`? Try different ports. You can also use this to map the internal network by targeting other hosts.

### 5. Path Traversal

- **Where**: `/files?name=`
- **Technique**: The `name` parameter is used to read files from the server filesystem without proper path sanitization.
- **Tools**: `curl`, `Burp Suite`
- **Hint**: Use relative path sequences to escape the intended directory. Think about what sensitive files exist on a Linux system and how many directories up you need to go.

### 6. Reflected XSS

- **Where**: `/search?q=`
- **Technique**: The `q` parameter is reflected directly into the HTML response without output encoding.
- **Tools**: Browser, `Burp Suite`, `XSS Hunter`
- **Hint**: The search term appears in the page body. Inject HTML or JavaScript that will execute when the page renders. Try different encodings if basic payloads are blocked.

### 7. Information Disclosure

- **Where**: Multiple API endpoints
- **Technique**: Sensitive data exposed through API endpoints that lack access control.
- **Tools**: `curl`, `Burp Suite`, `dirb`, `gobuster`
- **Hint**: Enumerate the `/api/` path. Some endpoints return configuration details, environment variables, or full user records including secrets. Not everything requires authentication.
