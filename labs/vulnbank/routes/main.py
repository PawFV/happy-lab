from flask import Blueprint, request, session

from db import get_db_connection
from templates import render

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render(
        "Welcome to SecBank",
        """
        <p>Your trusted partner for secure online banking.</p>
        <div class='card'>
            <h3>Services</h3>
            <p>Manage your accounts, read the latest bank news, and securely upload your identification documents.</p>
        </div>
        """,
    )


# VULN: SQL Injection in search
@bp.route("/search")
def search():
    q = request.args.get("q", "")
    results = ""
    if q:
        db = get_db_connection()
        # VULNERABLE: direct SQL injection
        query = f"SELECT * FROM posts WHERE title LIKE '%{q}%' OR content LIKE '%{q}%'"
        try:
            posts = db.execute(query).fetchall()
            for p in posts:
                results += f"<div class='card'><h3>{p['title']}</h3><p>{p['content']}</p></div>"
            if not posts:
                # VULNERABLE: reflected XSS
                results = f"<p>No results found for: {q}</p>"
        except Exception as e:
            results = f"<p class='danger'>SQL Error: {e}</p>"

    return render(
        "Search News",
        f"""
        <form method='GET'>
            <input name='q' value='{q}' placeholder='Search...'>
            <button type='submit'>Search</button>
        </form>
        {results}
        """,
    )


# VULN: Stored XSS in posts
@bp.route("/posts", methods=["GET", "POST"])
def posts():
    db = get_db_connection()

    if request.method == "POST" and "user_id" in session:
        title = request.form.get("title", "")
        content = request.form.get("content", "")
        # VULNERABLE: does not sanitize HTML/JS
        db.execute(
            "INSERT INTO posts (user_id, title, content) VALUES (%s, %s, %s)",
            (session["user_id"], title, content),
        )
        db.commit()

    all_posts = db.execute(
        "SELECT p.*, u.username FROM posts p JOIN users u ON p.user_id = u.id ORDER BY p.id DESC"
    ).fetchall()

    posts_html = ""
    for p in all_posts:
        # VULNERABLE: direct rendering without escape
        posts_html += f"""
        <div class='card'>
            <h3>{p['title']}</h3>
            <p>{p['content']}</p>
            <small>Posted by {p['username']} on {p['created_at']}</small>
        </div>"""

    form = ""
    if "user_id" in session:
        form = """
        <div class='card'>
            <h3>Post an Update</h3>
            <form method='POST'>
                <input name='title' placeholder='Title'>
                <textarea name='content' placeholder='Content' rows='3'></textarea>
                <button type='submit'>Publish</button>
            </form>
        </div>"""

    return render(
        "Bank News",
        f"""
        {form}
        {posts_html}
        """,
    )
