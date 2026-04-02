const { sessions } = require("./data");

function html(title, body) {
  return `<!DOCTYPE html>
<html><head><title>ShopTech - ${title}</title>
<style>
  body { font-family: 'Helvetica Neue', Arial, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 20px; background: #fafafa; color: #333; }
  a { color: #e67e22; text-decoration: none; }
  a:hover { text-decoration: underline; }
  input, textarea { padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 4px; width: 100%; box-sizing: border-box; }
  button { padding: 12px 24px; background: #e67e22; color: white; border: none; cursor: pointer; font-weight: bold; border-radius: 4px; }
  button:hover { background: #d35400; }
  .card { border: 1px solid #eee; padding: 20px; margin: 15px 0; border-radius: 8px; background: white; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
  pre { background: #f4f4f4; padding: 15px; overflow-x: auto; border: 1px solid #ddd; border-radius: 4px; }
  nav { border-bottom: 2px solid #e67e22; padding-bottom: 15px; margin-bottom: 30px; display: flex; gap: 20px; }
  nav a { font-weight: bold; }
  .flag { display: none; }
</style></head>
<body><nav>
  <a href="/">Store Front</a> <a href="/login">Account</a> <a href="/search">Catalog Search</a>
  <a href="/files">Downloads</a> <a href="/fetch">Track Order</a> <a href="/merge">Preferences</a>
</nav><h1>${title}</h1>${body}</body></html>`;
}

function getSession(req) {
  const token = req.headers["x-session-token"] || req.query.token;
  return sessions[token] || null;
}

module.exports = { html, getSession };
