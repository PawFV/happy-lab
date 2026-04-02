from flask import render_template_string, session

BASE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>SecBank - {{ title }}</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; background: #f4f6f8; color: #333; }
        a { color: #0056b3; text-decoration: none; }
        a:hover { text-decoration: underline; }
        input, textarea { padding: 10px; margin: 5px 0; border: 1px solid #ccc; border-radius: 4px; width: 100%; box-sizing: border-box; }
        button { padding: 10px 20px; background: #0056b3; color: white; border: none; border-radius: 4px; cursor: pointer; margin: 5px 0; font-size: 16px; }
        button:hover { background: #004494; }
        .card { border: 1px solid #e1e4e8; padding: 20px; margin: 15px 0; border-radius: 8px; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        .danger { color: #d73a49; font-weight: bold; }
        .success { color: #28a745; font-weight: bold; }
        nav { border-bottom: 2px solid #0056b3; padding-bottom: 15px; margin-bottom: 30px; display: flex; gap: 20px; }
        nav a { font-weight: bold; font-size: 16px; }
        .flag { display: none; }
    </style>
</head>
<body>
    <nav>
        <a href="/">Home</a>
        <a href="/posts">News</a>
        <a href="/search">Search</a>
        <a href="/upload">Documents</a>
        <a href="/profile">Account</a>
        {% if session.get('user_id') %}
            <a href="/logout" class="danger">Logout ({{ session.get('username') }})</a>
        {% else %}
            <a href="/login">Login</a>
            <a href="/register">Register</a>
        {% endif %}
    </nav>
    <h1>{{ title }}</h1>
    {{ content | safe }}
</body>
</html>
"""


def render(title, content):
    return render_template_string(BASE_TEMPLATE, title=title, content=content)
