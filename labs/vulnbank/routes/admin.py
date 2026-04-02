from flask import Blueprint, send_file
import os
import platform

from db import BACKUP_EXPORT_PATH, get_db_connection
from templates import render

bp = Blueprint("admin", __name__)


# VULN: Admin API without proper auth
@bp.route("/admin/users")
def admin_users():
    # VULNERABLE: only checks session, not admin role
    # Also: directly accessible without session due to logic error
    db = get_db_connection()
    users = db.execute("SELECT id, username, email, role FROM users").fetchall()

    html = "<table border='1' style='width:100%;border-collapse:collapse; background: white; margin-top: 20px;'>"
    html += "<tr><th style='padding:10px;'>ID</th><th style='padding:10px;'>Username</th><th style='padding:10px;'>Email</th><th style='padding:10px;'>Role</th></tr>"
    for u in users:
        html += f"<tr><td style='padding:10px;'>{u['id']}</td><td style='padding:10px;'>{u['username']}</td><td style='padding:10px;'>{u['email']}</td><td style='padding:10px;'>{u['role']}</td></tr>"
    html += "</table>"

    return render(
        "Admin Dashboard",
        f"""
        <p>User Management (Internal Use Only)</p>
        {html}
        """,
    )


# VULN: Information Disclosure
@bp.route("/debug")
def debug():
    from flask import current_app

    # VULNERABLE: exposes internal configuration
    return render(
        "System Status",
        f"""
        <div class='flag'>FLAG{{debug_endpoint_exposed}}</div>
        <pre style='background: #f4f4f4; padding: 15px; border: 1px solid #ddd; border-radius: 4px;'>
Python: {platform.python_version()}
OS: {platform.platform()}
Secret Key: {current_app.secret_key}
MySQL: {os.environ.get("MYSQL_HOST")}:{os.environ.get("MYSQL_PORT", "3306")} / {os.environ.get("MYSQL_DATABASE")}
Backup export: {BACKUP_EXPORT_PATH}
Working Dir: {os.getcwd()}
Env: {dict(os.environ)}
        </pre>
        """,
    )


# VULN: robots.txt reveals routes
@bp.route("/robots.txt")
def robots():
    return (
        """User-agent: *
Disallow: /admin/users
Disallow: /debug
Disallow: /backup
Disallow: /api/v1/internal
""",
        200,
        {"Content-Type": "text/plain"},
    )


@bp.route("/backup")
def backup():
    # VULNERABLE: DB backup accessible
    return send_file(
        BACKUP_EXPORT_PATH,
        as_attachment=True,
        download_name="database_backup.sql",
    )
